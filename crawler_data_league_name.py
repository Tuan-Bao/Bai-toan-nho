import requests
from bs4 import BeautifulSoup
import csv
import os

#
csv_dir = "D:\\Cào dữ liệu\\bài toán nhỏ\\csv\\Premier League\\league name"
#
csv_file = os.path.join(csv_dir, "league_name.csv")

url_match_page = "https://footystats.org/england/premier-league/fixtures#"
headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
respone_match_page = requests.get(url_match_page, headers=headers)
soup_match_page = BeautifulSoup(respone_match_page.content, "html.parser")

league_name_div = soup_match_page.find("div", id="leagueContent").find("div", class_="section cf")
league_name = league_name_div.find("ul", id="pageCategory").find("li", class_="league lh14e").find("span").text.strip()

with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([league_name])