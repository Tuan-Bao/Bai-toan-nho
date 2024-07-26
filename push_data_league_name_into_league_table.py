import csv
import sqlite3
import os

# Thư mục chứa cơ sở dữ liệu
db_dir = "D:\\Cào dữ liệu\\bài toán nhỏ\\My database"
db_path = os.path.join(db_dir, "premier_league.db")

# Tạo kết nối với cơ sở dữ liệu
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Tạo bảng league
c.execute   ("""CREATE TABLE IF NOT EXISTS league (
                id_league INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

# Tạo trigger để tự động cập nhật modified_at
c.execute   ("""CREATE TRIGGER IF NOT EXISTS update_league_modified_at
                AFTER UPDATE ON league
                FOR EACH ROW
                BEGIN
                    UPDATE league SET modified_at = CURRENT_TIMESTAMP
                    WHERE id_league = OLD.id_league;
                END;""")

# Đường dẫn đến file csv
csv_path = "D:\\Cào dữ liệu\\bài toán nhỏ\\csv\\Premier League\\league name\\league_name.csv"

# Đọc dữ liệu từ file csv và chèn vào bảng league
with open(csv_path, "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        name = row[0]
        code = name[:3].upper()
    c.execute("INSERT OR IGNORE INTO league (name, code) VALUES (?, ?)", (name, code))

# Lưu các thay đổi và đóng kết nối
conn.commit()
conn.close()