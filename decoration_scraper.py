import pandas as pd
import requests
from bs4 import BeautifulSoup
import re #RegEx
import time



#Path to save the exported file
save_path = r"mhrs_decorations.csv"

#Link to the base page with all the decorations
decos_page_link = "https://game8.co/games/Monster-Hunter-Rise/archives/325392"

def get_page_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

#Add another row to the end of Data Frame(df)
def append_to_df(data_row, df):
    length = len(df)
    df.loc[length] = data_row

columns_list = ["Name", "Skill", "Value"]
df = pd.DataFrame(columns = columns_list)

soup_decos = get_page_html(decos_page_link)

#Sunbreak / Master Rank
table_mr_lvl_1 = soup_decos.find_all("table")[2]
table_mr_lvl_2 = soup_decos.find_all("table")[3]
table_mr_lvl_3 = soup_decos.find_all("table")[4]
table_mr_lvl_4 = soup_decos.find_all("table")[5]
#table_rampage = soup_decos.find_all("table")[6]

#Base game
table_base_game_lvl_1 = soup_decos.find_all("table")[8]
table_base_game_lvl_2 = soup_decos.find_all("table")[9]
table_base_game_lvl_3 = soup_decos.find_all("table")[10]

#Tables list
tables_list = [table_mr_lvl_1, table_mr_lvl_2, table_mr_lvl_3, table_mr_lvl_4, table_base_game_lvl_1, table_base_game_lvl_2, table_base_game_lvl_3]

for i, links_table in enumerate(tables_list):
    rows = links_table.find_all("tr")
    for row in rows[1:]:
        link = row.find_all("td")[0].find("a")["href"]
        soup_decoration = get_page_html(link)
        decoration_table = soup_decoration.find_all("table")[0]
        
        decoration_name = decoration_table.find_all("th")[0].get_text().strip()

        skill_name = decoration_table.find("a").get_text().strip()
        
        skill_value = decoration_table.find_all("tr")[2].find_all("td")[0].get_text()
        skill_value = re.findall("[0-9]", skill_value)
        skill_value = skill_value[0].strip()

        data_row = {}
        data_row[columns_list[0]] = decoration_name
        data_row[columns_list[1]] = skill_name
        data_row[columns_list[2]] = skill_value

        append_to_df(data_row, df)
        print(f"Deco {decoration_name} added !\n")
        

df.to_csv(save_path)
print("   ___________________")
print("  /                  /")
print(" /   S U C C E S S  /")
print("/__________________/")
