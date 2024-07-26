import csv
import sqlite3
import os

# Thư mục chứa cơ sở dữ liệu
db_dir = "D:\\Cào dữ liệu\\bài toán nhỏ\\My database"
db_path = os.path.join(db_dir, "premier_league.db")

# Tạo kết nối với cơ sở dữ liệu
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Tạo bảng season
c.execute   ("""CREATE TABLE IF NOT EXISTS season(
                id_season INTEGER PRIMARY KEY AUTOINCREMENT,
                id_league INTEGER NOT NULL,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_league) REFERENCES league(id_league))""")

# Tạo trigger để tự động cập nhật modified_at
c.execute   ("""CREATE TRIGGER IF NOT EXISTS update_season_modified_at
                AFTER UPDATE ON season
                FOR EACH ROW
                BEGIN
                    UPDATE season SET modified_at = CURRENT_TIMESTAMP
                    WHERE id_league = OLD.id_league;
                END;""")

# Đường dẫn đến file csv, thay đổi đường dẫn đổi file csv
csv_path = "D:\\Cào dữ liệu\\bài toán nhỏ\\csv\\Premier League\\2023.24\\season_2023.24.csv"

# Lấy id_league của Premier League
c.execute("SELECT id_league FROM league WHERE name = 'Premier League'")
league_id = c.fetchone()[0]

# Đọc dữ liệu từ file csv và chèn vào bảng season
with open(csv_path, "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        name = row[0]
    c.execute("INSERT OR IGNORE INTO season(id_league, name) VALUES (?, ?)", (league_id, name))

# Lưu các thay đổi và đóng kết nối
conn.commit()
conn.close()