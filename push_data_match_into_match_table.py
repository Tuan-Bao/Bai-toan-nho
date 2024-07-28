import csv
import sqlite3
import os
from datetime import datetime

# Thư mục chứa cở sở dữ liệu
db_dir = "D:\\Cào dữ liệu\\bài toán nhỏ\\My database"
db_path = os.path.join(db_dir, "premier_league.db")

# Tạo kết nối với cơ sở dữ liệu
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Tạo bảng match
c.execute   ("""CREATE TABLE IF NOT EXISTS match(
                id_match INTEGER PRIMARY KEY AUTOINCREMENT,
                id_season INTEGER NOT NULL,
                team_home_id INTEGER NOY NULL,
                team_away_id INTEGER NOT NULL,
                score TEXT,
                played_at DATETIME,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_season) REFERENCES season(id_season),
                FOREIGN KEY (team_home_id) REFERENCES team(id_team),
                FOREIGN KEY (team_away_id) REFERENCES team(id_team))""")

# Tạo trigger để tự động cập nhật modified_at
c.execute   ("""CREATE TRIGGER IF NOT EXISTS update_match_modified_at
                AFTER UPDATE ON match
                FOR EACH ROW
                BEGIN
                    UPDATE match SET modified_at = CURRENT_TIMESTAMP
                    WHERE id_match = OLD.id_match;
                END;""")

# Hàm lấy id_team từ tên đội bóng
def get_team_id(team_name):
    c.execute("SELECT id_team FROM team WHERE name = ?", [team_name])
    result = c.fetchone()
    return result[0]

# Hàm lấy id_season của mùa giải
def get_season_id(season):
    c.execute("SELECT id_season FROM season WHERE name = ?", [season])
    result = c.fetchone()
    return result[0]

# Đường dẫn đến file csv, thay đổi đường dẫn đổi file csv
csv_file = "D:\\Cào dữ liệu\\bài toán nhỏ\\csv\\Premier League\\2023.24\\results_of_each_match_in_season_2023.24.csv"
#
id_season = get_season_id("2023/24")

# Đọc dữ liệu từ file csv và chèn vào bảng match
with open(csv_file, "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        played_at = row[0]
        score = row[2]
        
        team_home = row[1]
        team_away = row[3]
        team_home_id = get_team_id(team_home)
        team_away_id = get_team_id(team_away)
        c.execute   ("""INSERT OR IGNORE INTO match(id_season, team_home_id, team_away_id, score, played_at)
                        VALUES (?, ?, ?, ? ,?)""", (id_season, team_home_id, team_away_id, score, played_at))

# Lưu các thay đổi và đóng kết nối
conn.commit()
conn.close()