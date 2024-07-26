import csv
import sqlite3
import os

# Tên thư mục chứa cơ sở dữ liệu
db_dir = "D:\\Cào dữ liệu\\bài toán nhỏ\\My database"
db_path = os.path.join(db_dir, "premier_league.db")

# Tạo kết nối cơ sở dữ liệu
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Tạo bảng team
c.execute   ("""CREATE TABLE IF NOT EXISTS team(
                id_team INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

# Tạo trigger để tự động cập nhật modified_at
c.execute   ("""CREATE TRIGGER IF NOT EXISTS update_team_modified_at
                AFTER UPDATE ON team
                FOR EACH ROW
                BEGIN
                    UPDATE team SET modified_at = CURRENT_TIMESTAMP
                    WHERE id_team = OLD.id_team;
                END;""")

# Đường dẫn đến file csv, thay đổi đường dẫn để đổi file csv
csv_path = "D:\\Cào dữ liệu\\bài toán nhỏ\\csv\\Premier League\\2023.24\\teams_played_in_season_2023.24.csv"

# Đọc dữ liệu từ file csv và đưa vào bảng team
with open(csv_path, "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        team_name  = row[0]
        num_words = len(team_name.split())
        if num_words > 1:
            team_code = "".join(word[0] for word in team_name.split()[:num_words]).upper()
        else:
            team_code = team_name[:3].upper()
        c.execute("INSERT OR IGNORE INTO team (name, code) VALUES (?, ?)", (team_name, team_code))
        
# Lưu các thay đổi và đóng kết nối
conn.commit()
conn.close()