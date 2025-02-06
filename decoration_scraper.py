import pandas as pd
import requests
from bs4 import BeautifulSoup
import re #RegEx


#Path to save the exported file.
save_path = r"mhrs_decorations.csv"

#Link to the base page with all the decorations.
decos_page_link = "https://game8.co/games/Monster-Hunter-Rise/archives/325392"

#Use requests and BeautifulSoup libraries to extract the html code.
#Returns the url's page html code.
def get_page_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

#Add another row to the end of Data Frame(df).
def append_to_df(data_row, df):
    length = len(df)
    df.loc[length] = data_row

#List to store the columns of the Data Frame.
columns_list = ["Name", "Skill", "Value"]

#Create the data frame
df = pd.DataFrame(columns = columns_list)

#Get the html for the decoration's links page.
soup_decos = get_page_html(decos_page_link)

#Sunbreak / Master Rank decorations.
#Each table contains links of specific decorations.
table_mr_lvl_1 = soup_decos.find_all("table")[2]
table_mr_lvl_2 = soup_decos.find_all("table")[3]
table_mr_lvl_3 = soup_decos.find_all("table")[4]
table_mr_lvl_4 = soup_decos.find_all("table")[5]

#Rampage decorations are excluded, since they can only be attached to weapons, not armors.
#table_rampage = soup_decos.find_all("table")[6]

#Base game decorations.
#Each table contains links of specific decorations.
table_base_game_lvl_1 = soup_decos.find_all("table")[8]
table_base_game_lvl_2 = soup_decos.find_all("table")[9]
table_base_game_lvl_3 = soup_decos.find_all("table")[10]

#List containing all the tables for the base game and sunbreak decorations.
tables_list = [table_mr_lvl_1, table_mr_lvl_2, table_mr_lvl_3, table_mr_lvl_4, table_base_game_lvl_1, table_base_game_lvl_2, table_base_game_lvl_3]

#Loops through all the tables on tables_list.
for links_table in tables_list:
    #Extracts all the rows of the table.
    rows = links_table.find_all("tr")
    #Loops through all the rows of the table.
    for row in rows[1:]:
        #Get the link to the decoration page
        link = row.find_all("td")[0].find("a")["href"]
        #Get the decoration page html and find the info table
        soup_decoration = get_page_html(link)
        decoration_table = soup_decoration.find_all("table")[0]
        
        #Extract the decoration name
        decoration_name = decoration_table.find_all("th")[0].get_text().strip()
        #Extract the decoration skill name
        skill_name = decoration_table.find("a").get_text().strip()
        
        #Extract the decoration skill value/level
        skill_value = decoration_table.find_all("tr")[2].find_all("td")[0].get_text()
        skill_value = re.findall("[0-9]", skill_value)
        skill_value = skill_value[0].strip()

        #Create empty data row and fill with decoration name, skill name and skill value/level
        data_row = {}
        data_row[columns_list[0]] = decoration_name
        data_row[columns_list[1]] = skill_name
        data_row[columns_list[2]] = skill_value

        #Add data row to the data frame
        append_to_df(data_row, df)
        print(f"Deco {decoration_name} added !\n")

 
#Save the data frame as a .csv file
df.to_csv(save_path)
print("   ___________________")
print("  /                  /")
print(" /   S U C C E S S  /")
print("/__________________/")
