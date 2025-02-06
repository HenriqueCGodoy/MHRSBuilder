import pandas as pd
import requests
from bs4 import BeautifulSoup
import re #RegEx
import time


#Path to save the exported file
save_path = r"mhrs_mr_armors.csv"

#Path to the skills file
skills_file_path = r"mhrs_skills.csv"

#Link to the page of all Master Rank sets
armors_page_link = "https://game8.co/games/Monster-Hunter-Rise/archives/316580#hl_1"


#Use requests and BeautifulSoup libraries to extract the html code
#Returns the url's page html code
def get_page_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

#Reads the skills csv file and returns a list with the name of all skills
def fill_skillname_list():
    list = []
    skill_df = pd.read_csv(skills_file_path)
    counter = 0
    while(counter < len(skill_df)):
        list.append(skill_df["Name"].loc[counter])
        counter += 1
    return list
    

#Count the amount of each level slot and return a list
#The returned list is [number of level 1 slots, number of level 2 slots, number of level 3 slots, number of level 4 slots]
def jewel_count(list):
    lvl1 = 0
    lvl2 = 0
    lvl3 = 0
    lvl4 = 0
    for item in list:
        if(int(item) == 1):
            lvl1 += 1
        elif(int(item) == 2):
            lvl2 += 1
        elif(int(item) == 3):
            lvl3 += 1
        else:
            lvl4 += 1
    
    return [lvl1, lvl2, lvl3, lvl4]

#Add another row to the end of Data Frame(df)
def append_to_df(data_row, df):
    length = len(df)
    df.loc[length] = data_row

#Create the skills dictionary for appending on then row of the Data Frame(df)
#Returns a dictionary {Skill Name : Skill Value}
def create_skills_dict(skills_table, row_index):
    piece_name = skills_table.find_all('tr')[row_index].find_all('td')[0].get_text()
    skill_name = skills_table.find_all('tr')[row_index].find_all('td')[2].find_all('a')
    skill_value = skills_table.find_all('tr')[row_index].find_all('td')[2].find_all('div')
    
    #Get names of skills
    #Overrides the skill_name list to contain only the text (name) of each skill
    counter = 0
    for item in skill_name:
        skill_name[counter] = item.get_text()
        #Checks if the skill name exists. If not, stop the program
        if(skill_name[counter] not in skill_name_list):
            print(f"SKILL NAME ({skill_name[counter]}) NOT PRESENT IN SKILLS LIST")
            quit()
        counter += 1

    #Get value of skills
    #Overrides the skill_value list to contain only the text (skill value) of each skill
    str_value = ""
    counter = 0
    for item in skill_value:
        skill_value[counter] = item.get_text()
        str_value += skill_value[counter]
        counter += 1
    #Manual override for "Mizutsune Braces X" armor piece
    if(piece_name == "Mizutsune Braces X"):
        str_value += "1"
    #Manual Override for "Tigrex Coil X" armor piece
    if(piece_name == "Tigrex Coil X"):
        str_value += "2"
    #Extract only the digit of the "value string"(str_value) using RegEx and save into skill_value
    skill_value = re.findall("[0-9]", str_value)

    #Fill skills dictionary with pair {Skill Name : Skill Value}
    skill_dict = {}
    counter = 0
    for item in skill_name:
        skill_dict[item] = skill_value[counter]
        counter += 1
    
    return skill_dict

#Extracts the jewel slot level from a string (jewel_txt)
#Returns a list containing the jewel slot's levels in integers
def get_jewel_list(jewel_txt):
    #① - \u2460
    #② - \u2461
    #③ - \u2462
    #④ - \u2463
    jewel_list = []
    for item in jewel_txt:
        match(item):
            case "\u2460":
                jewel_list.append(1)
            case "\u2461":
                jewel_list.append(2)
            case "\u2462":
                jewel_list.append(3)
            case "\u2463":
                jewel_list.append(4)
    return jewel_list

#Get all the links from a table's rows of links (tr_list).
def get_links(tr_list):
    links_list = []
    for row in tr_list[0:len(tr_list)-1]:
        tds = row.find_all('td')
        for td in tds:
            links_list.append(td.find('a').get('href'))
    return links_list

#Find and filter all the tables from a given armor set page (set_page_link).
#Get the table containing the name, the skills and the jewel slots (name_skill_jewel_table)...
#And get the table containing the defense (defense_table)...
#And get the table containing the the elemental resistances (resistances_table).
def find_tables(set_page_link):
    #Flags to know if the tables were found (found_name_skill_jewel, found_defense, found_resistances)
    found_name_skill_jewel = False
    found_defense = False
    found_resistances = False
    soup_set = get_page_html(set_page_link)
    tables_list = soup_set.find_all('table')
    for table in tables_list:
        #Checks if the table has a header,
        #If not, the current test table isn't any of the tables needed...
        #And continue to the next iteration.
        try:
            table_test = table.find_all('tr')[0].find_all('th')[1]
        except IndexError:
            continue
        
        #Tests for both name_skill_jewel and defense tables first
        try:
            #Checks if the table containing name, skills and jewel slots has not been found...
            #And if the current test table has the text "Slots".
            #If the table contains the text, the current test table is the correct one...
            #And continue to the next iteration after setting its reference to the variable.
            if not found_name_skill_jewel and table_test.get_text() == "Slots":
                name_skill_jewel_table = table
                found_name_skill_jewel = True
                continue

            #Checks if the table containing the defense has not been found...
            #And if the current test table has the text "Base Defense".
            #If the table contains the text, the current test table is the correct one...
            #And continue to the next iteration after setting its reference to the variable
            if not found_defense and table_test.get_text() == "Base Defense":
                defense_table = table
                found_defense = True
                continue
        except IndexError:
            #Ignores any errors that might appear when testing the wrong tables
            pass
        
        #Tests for elemental resistances table
        try:
            #Checks if the table containing the elemental resistances has not been found...
            #And if the current test table has the text "Fire Symbol (MH Rise).png" on its image alt tag.
            #If the table contains the text, the current test table is the correct one...
            #And continue to the next iteration after setting its reference to the variable.
            if not found_resistances and table_test.find_all('img', alt=True)[0]['alt'] == "Fire Symbol (MH Rise).png":
                resistances_table = table
                found_resistances = True
                continue
        except IndexError:
            #Ignores any errors that might appear when testing the wrong tables
            pass

        #Breaks the loop when all tables are found
        if found_resistances and found_defense and found_name_skill_jewel:
            break

    #Returns a list containing the correct tables
    return [name_skill_jewel_table, defense_table, resistances_table]

#Creates a new data row.
#Receives the rank of the armor (low, high, master)...
#And the current iteration on main loop, to identify the correct row to extract the information...
#And a list of the relevant tables: (name, skill, jewel) table, defense table and elemental resistances table.
def create_data_row(rank, iteration, tables):
    name_skill_jewel_table = tables[0]
    defense_table = tables[1]
    resistances_table = tables[2]

    #Create empty data row.
    data_row = {}

    #Check if the set has no more pieces.
    if(iteration >= len(name_skill_jewel_table.find_all('tr'))-1):
        #Current iteraction of armor set doesn't have more pieces...
        #And the main iteration needs to be stopped.
        return 1
    
    #Get the alt text of the piece icon to define its type (head, torso, arm, waist or leg).
    type_alt_txt = name_skill_jewel_table.find_all('tr')[iteration+1].find_all('td')[0].find('img', alt = True)['alt']
    match(type_alt_txt):
        case "Head Image":
            type = 0
        case "Torso Image":
            type = 1
        case "Arms Image":
            type = 2
        case "Waist Image":
            type = 3
        case "Legs Image":
            type = 4
        case _:
            type = 5
    
    if(type == 5):
        #Something went wrong identifying the type of the armor piece
        return 2

    #Add type and rank to data row
    data_row["Type"] = type
    print(f"Type OK: {type}")
    data_row["Rank"] = rank
    print(f"Rank OK: {rank}")

    #Get name and add to data row
    name = name_skill_jewel_table.find_all('tr')[iteration+1].find_all('td')[0].get_text()
    data_row["Name"] = name
    print(f"Name OK: {name}")

    #get defense and add to data row
    defense = defense_table.find_all('tr')[iteration+1].find_all('td')[1].get_text()
    data_row["Defense"] = defense
    print(f"Defense OK: {defense}")

    #get jewels string and converts into integers based on the level of the slots
    jewel_list = get_jewel_list(name_skill_jewel_table.find_all('tr')[iteration+1].find_all('td')[1].get_text())

    #Counts the amount of slots of each rarity on the armor piece
    jewel_list = jewel_count(jewel_list)
    
    #Add jewels count to data row
    count = 0
    while(count<4):
        data_row[columns_list[count+4]] = jewel_list[count]
        count += 1
    print(f"Jewels OK: {jewel_list}")

    #Extract the elemental resistances of the piece
    res_list = []
    for i in range(1, 6):
        res_list.append(resistances_table.find_all('tr')[iteration+1].find_all('td')[i].get_text())
    
    #Add the elemental resistances to the data row
    count = 0
    while(count<5):
        data_row[columns_list[count+8]] = res_list[count]
        count += 1
    print(f"Resistances OK: {res_list}")

    #Creates the skill dictionary {Skill name : skill value}
    skill_dict = create_skills_dict(name_skill_jewel_table, iteration+1)

    #Add the skills value to the corresponding skills columns of the data row
    for skill in skill_dict:
        data_row[skill] = skill_dict[skill]
    print(f"Skills OK: {skill_dict}")

    #returns the data row of the piece
    return data_row


#List to the name of all skills in the game
skill_name_list = fill_skillname_list()

#List to store the columns of the Data Frame
columns_list = ["Type", "Rank", "Name", "Defense", "Lvl1 Gem", "Lvl2 Gem", "Lvl3 Gem", "Lvl4 Gem", "Fire Res", "Water Res", "Thunder Res", "Ice Res", "Dragon Res"] + skill_name_list

#Main function
def main():
    #Create  Data Frame
    df = pd.DataFrame(columns = columns_list)

    t1 = time.time()
    #Get html of armor set's links page
    soup_armors = get_page_html(armors_page_link)
    t1 = time.time() - t1
    print(f"Soup armors page: {t1}")

    t2 = time.time()
    #Links of master rank armor sets
    master_rank_links = get_links(soup_armors.find_all('table')[0].find_all('tr'))
    print(f"Master Rank Links: {len(master_rank_links)}")
    
    #Unused links, because the program only extracts the info from master rank armors
    high_rank_links = get_links(soup_armors.find_all('table')[1].find_all('tr'))
    low_rank_links = get_links(soup_armors.find_all('table')[2].find_all('tr'))
    
    t2 = time.time() - t2
    print(f"Time to get all links in lists: {t2}")

    #Loop through all the links
    total_pieces_count = 1
    for link in master_rank_links:
        tl = time.time()
        t3 = time.time()
        #Get a list of tables on the armor page.
        tables = find_tables(link)
        t3 = time.time() - t3
        print(f"Time to get tables from page: {t3}")
        #Loop through all the armor pieces in the set. Max of 5 pieces, Min of 1 piece.
        count = 0
        while(count < 5):
            t4 = time.time()
            #Create a new data row
            data_row = create_data_row("master", count, tables)
            t4 = time.time() - t4
            print(f"Time to create data row: {t4}")
            #If a set has less than 5 pieces, stop this loop iteration early and go to the next armor set.
            if data_row == 1:
                print(f"Set finished: num {total_pieces_count}\n")
                break
            #If something went wrong trying to identify the piece type, stop the program
            if data_row == 2:
                print(f"Mismatch piece type: num {total_pieces_count}\n")
                quit()
            #Add the data row to the data frame
            append_to_df(data_row, df)
            print(f"Piece num {total_pieces_count} was appended to DF")
            print("\n-----------------------------------------------------------------------------------------------------------\n")
            count += 1
            total_pieces_count += 1
        tl = time.time() - tl
        print(f"Main loop time: {tl}")
        print("\n\n |||||||||||||||||||||||||||||||||||||||||||||||||  Set added  ||||||||||||||||||||||||||||||||||||||||||||||||||||\n\n")

    #Replaces NA/NaN with zeros
    df.fillna(0, inplace=True)
    print(df)
    #Save the data frame as a .csv file
    df.to_csv(save_path)
    

if __name__ == "__main__":
    main()
    



