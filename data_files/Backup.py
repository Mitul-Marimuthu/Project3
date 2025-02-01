import pandas as pd
import sqlite3

conn = sqlite3.connect("Users/mitul/Desktop/spotify/main/data_files/spotify.db")
main = pd.read_sql("SELECT * FROM main", conn)
artists = pd.read_sql("SELECT * FROM artists", conn)
albums = pd.read_sql("SELECT * FROM albums", conn)
times = pd.read_sql("SELECT * FROM times", conn)
main.to_csv("main.csv", index=False)
artists.to_csv("artists.csv", index=False)
albums.to_csv("albums.csv", index=False)
times.to_csv("times.csv", index=False)
conn.close()