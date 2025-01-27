import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

#Path to save the exported file
save_path = r"c:\Users\Godoy\OneDrive - Fatec Centro Paula Souza\mhrs_skills.csv"

#Link to the page with all the skills in the game
skills_page_link = "https://monsterhunterrise.wiki.fextralife.com/Skills"

def get_page_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

#Add another row to the end of Data Frame(df)
def append_to_df(data_row, df):
    length = len(df)
    df.loc[length] = data_row


columns_list = ["Name", "Max_Level"]
df = pd.DataFrame(columns = columns_list)

soup_skills = get_page_html(skills_page_link)
table_skills = soup_skills.find("table")
skill_rows = table_skills.find_all("tr")

#skills_list = {}

counter = 1
for item in skill_rows[1:]:
    name = skill_rows[counter].find_all("td")[0].get_text().strip()

    level = skill_rows[counter].find_all("td")[2].get_text()
    level = re.findall("[0-9]", level)
    level = level[0]

    data_row = {}
    data_row[columns_list[0]] = name
    data_row[columns_list[1]] = level

    append_to_df(data_row, df)
    print(f"Skill added ! {counter} / {len(skill_rows)-1}")
    counter += 1

#Correcting "Quick sheath" to "Quick Sheathe"
df.loc[53] = ["Quick Sheathe", 3]

print(df)
df.to_csv(save_path)
