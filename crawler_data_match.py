import requests
from bs4 import BeautifulSoup
import csv
import os

#
csv_dir = "D:\\Cào dữ liệu\\bài toán nhỏ\\csv\\Premier League\\2020.21"
#
csv_file = os.path.join(csv_dir, "results_of_each_match_in_season_2020.21.csv")

url_match_page = "https://footystats.org/england/premier-league/fixtures#"
#
crawl_season = "2020/21"
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

league_title = soup_match_page_when_selecting_season.find("div", class_="section cf").find("ul", id="pageCategory").find("li", class_="league lh14e").find("span").text.strip()
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    
    match_list_div = soup_match_page_when_selecting_season.find("div", class_="col-right col-lg-8 col-sm-12").find("div", id="matches-list")
    for data_game_each_week in match_list_div.find_all("div", class_="full-matches-table mt1e"):
        for each_game in data_game_each_week.find("div", class_="matches").find_all("ul"):
            data_time = each_game.find("li", class_="date convert-months time").find("span", class_="timezone-convert-match-month").text.strip()
            home = each_game.find("li", class_="match-info row cf fl rfnone").find("a", class_="team home fl").find("span", class_="hover-modal-parent hover-modal-ajax-team").text.strip()
            away = each_game.find("li", class_="match-info row cf fl rfnone").find("a", class_="team away fl").find("span", class_="hover-modal-parent hover-modal-ajax-team").text.strip()
            score = each_game.find("li", class_="match-info row cf fl rfnone").find("a", class_="h2h-link pr fl").find("span", class_="bold ft-score").text.strip()
            writer.writerow([data_time, home, score, away])