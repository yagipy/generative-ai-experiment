# poetry run python init_sqlite.py
import glob
import os
import subprocess

CSV_DIR = "./data"
FB_FILE = "./sample.db"

if os.path.exists(FB_FILE):
    os.remove(FB_FILE)

csv_file_paths = glob.glob(f"{CSV_DIR}/*.csv")
for csv_file_path in csv_file_paths:
    basename = os.path.basename(csv_file_path)
    table = basename.rstrip(".csv")

    print(f"loading {csv_file_path} to {table}...")
    subprocess.run(["sqlite3", "-separator", ",", FB_FILE, f".import {csv_file_path} {table}"])
    subprocess.run(["sqlite3", FB_FILE, f"select count(*) from {table}"])
