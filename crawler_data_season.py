import requests
from bs4 import BeautifulSoup
import csv
import os

#
csv_dir = "D:\\Cào dữ liệu\\bài toán nhỏ\\csv\\Premier League\\2023.24"
#
csv_file = os.path.join(csv_dir, "season_2023.24.csv")

url_match_page = "https://footystats.org/england/premier-league/fixtures#"
#
crawl_season = "2023/24"
headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
respone_match_page = requests.get(url_match_page, headers=headers)
soup_match_page = BeautifulSoup(respone_match_page.content, "html.parser")

season_div = soup_match_page.find("div", class_="normalContentWidth cf").find("div", id="teamSummary").find("div", class_="league-details").find("div", class_="detail season")
season_dropdown = season_div.find("div", class_="drop-down-parent fl boldFont").find("ul", class_="drop-down").find_all("li")

hash_match_page = None
zzz_match_page = None
cur_match_page = None
zzzz_match_page = None

for each_season in season_dropdown:
    if each_season.text == crawl_season:
        hash_match_page = each_season.find("a")["data-hash"]
        zzz_match_page = each_season.find("a")["data-zzz"]
        cur_match_page = each_season.find("a")["data-z"]
        zzzz_match_page = each_season.find("a")["data-zzzz"]

payload_match_page = {
    "hash": hash_match_page,
    "zzz": zzz_match_page,
    "cur": cur_match_page,
    "zzzz": zzzz_match_page
}

requests_url_match_page_when_selecting_season = "https://footystats.org/ajax_league.php"
respone_match_page_when_selecting_season = requests.post(requests_url_match_page_when_selecting_season, data=payload_match_page)
soup_match_page_when_selecting_season = BeautifulSoup(respone_match_page_when_selecting_season.content, "html.parser")

season_div_in_match_page_when_selecting_season = soup_match_page_when_selecting_season.find("div", id="teamSummary").find("div", class_="league-details").find("div", class_="detail season")
season_in_match_page_when_selecting_season = season_div_in_match_page_when_selecting_season.find("div", class_="drop-down-parent fl boldFont").get_text().split()[0]

with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([season_in_match_page_when_selecting_season])
    