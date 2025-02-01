import pandas as pd
import sqlite3

conn = sqlite3.connect("Users/mitul/Desktop/spotify/main/data_files/spotify.db")
db = pd.read_sql("SELECT * FROM albums", conn)
# cursor = conn.cursor()
# cursor.execute('DELETE FROM main WHERE "Song Name" = ?', ('Big Sleep',))
# conn.commit()
db.to_csv("album_list.csv", index=False, header=True)
conn.close()