import csv
import sqlite3
import os

# Thư mục chưa cơ sở dữ liệu
db_dir = "D:\\Cào dữ liệu\\bài toán nhỏ\\My database"
db_path = os.path.join(db_dir, "premier_league.db")

# Tạo kết nối với cơ sở dữ liệu
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Tạo bảng League
c.execute   ("""CREATE TABLE IF NOT EXISTS league (
                id_league INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                
            )""")
