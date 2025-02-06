import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

#Path to save the exported file.
save_path = r"mhrs_skills.csv"

#Link to the page with all the skills in the game
skills_page_link = "https://monsterhunterrise.wiki.fextralife.com/Skills"

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
columns_list = ["Name", "Max_Level"]

#Create the data frame
df = pd.DataFrame(columns = columns_list)

#Get the html for the skills links page.
soup_skills = get_page_html(skills_page_link)
#Get the skills table.
table_skills = soup_skills.find("table")
#Get all the rows of the skills table.
skill_rows = table_skills.find_all("tr")

#Loops through the skills
counter = 1
for item in skill_rows[1:]:
    #Extract the skill's name.
    name = skill_rows[counter].find_all("td")[0].get_text().strip()

    #Extract the skill's level text
    level = skill_rows[counter].find_all("td")[2].get_text()
    #Use RegEx to extract the skill number from the string.
    level = re.findall("[0-9]", level)
    #Correct the list to a single value on the variable.
    level = level[0]

    #create empty data row
    data_row = {}
    #Fill data row with skill name and level
    data_row[columns_list[0]] = name
    data_row[columns_list[1]] = level

    #Add data row to dataframe
    append_to_df(data_row, df)
    print(f"Skill added ! {counter} / {len(skill_rows)-1}")
    counter += 1

#Correcting "Quick sheath" to "Quick Sheathe"
df.loc[53] = ["Quick Sheathe", 3]

print(df)
#Save the data frame as a .csv file
df.to_csv(save_path)
