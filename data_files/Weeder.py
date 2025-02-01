import pandas as pd
import sqlite3

conn = sqlite3.connect("/Users/mitul/Desktop/spotify/main/data_files/spotify.db")
#cursor = conn.cursor()
# conn.execute("DELETE FROM times")
# conn.commit()
# cursor.execute('SELECT * FROM times')
# rows = cursor.fetchall()

# dele = {"Song": ["A"], "Artist": ["a"], "Listen History": ['b']}

#import sqlite3
#import ast

# Connect to the SQLite database
#conn = sqlite3.connect("your_database.db")
#cursor = conn.cursor()

# Fetch all rows from the table (assuming your table is 'your_table')
# cursor.execute('SELECT * FROM times')
# rows = cursor.fetchall()

# # Iterate through each row and process the listen history
# for row in rows:
#     #rowid = row[0]  # Get the row ID
#     song = row[0]  # Extract the song
#     artist = row[1]  # Extract the artist
#     listen_history_str = row[2]  # Extract the listen history string
    
#     # Step 1: Remove the extra quotes around each element (e.g., ""2"" -> "2")
#     cleaned_list_str = listen_history_str.replace('""', '"')
#     #print(cleaned_list_str)
#     # Step 2: Convert the cleaned string into an actual Python list
#     try:
#         cleaned_list_str = cleaned_list_str.strip('[]')

#         # Split the string by commas
#         listen_history_list = cleaned_list_str.split(',')

#         # Remove extra spaces or quotes from each element
#         listen_history_list = [item.strip().replace('"', '') for item in listen_history_list]
#     except:
#         #print(f"Error processing row {rowid}: {e}")
#         continue  # Skip if there's an error parsing
    
#     # Step 3: Filter out strings that have length 1 (those we don't want)
#     filtered_list = [item for item in listen_history_list if len(item) > 1]

#     # Step 4: Combine the valid elements into a single string
#     combined_history = "".join(filtered_list)
#     print(combined_history)
#     # Step 5: Print or update the database with the combined string back into the listen history column
#     #print(f"Row ID {rowid}: Song: {song}, Artist: {artist}, Combined Listen History: {combined_history}")
    
#     # Update the original 'listen history' column with the combined result
#     cursor.execute('UPDATE times SET "Listen History" = ? WHERE "Song" = ? AND "Artist" = ?', 
#                    (combined_history, song, artist))

# # Commit the changes to the database (if you updated the database)
# conn.commit()

# # Close the connection
# #conn.close()

# print("Data processed and updated successfully.")


# #conn.commit()
#     #print(type(row[2]))
# # Load data from the database
# #db = pd.read_sql("SELECT * FROM times", conn)
# # db.columns = db.columns.str.strip()
# # db = db.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

#LOOK AT THE FUCKING FILES BEFORE DOING THIS BULLSHIT

def times():
    db = pd.read_csv('times.csv')
    db = db.groupby("Song", as_index=False).agg({
        "Artist": 'first',
        "Listen History": 'max'
    })
    db.to_sql("times", conn, if_exists="replace", index=False)

def albums():
    db = pd.read_sql("SELECT * FROM albums", conn)
    # db.columns = db.columns.str.strip()
    #db = db.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Group by "Artist" and sum "Times Played"
    #db = db.drop_duplicates(keep='last')
    db = db.groupby("Album", as_index=False).agg({
        "Artist": "first",
        "Number of Songs": 'max'  # Sum up play counts
    })
    db.to_sql("albums", conn, if_exists="replace", index=False)
    # Write the cleaned data back to SQLite
    #db.to_csv("times", conn, if_exists="replace", index=False)
    db.to_csv("albums.csv", header=True, index=False)

def artists():
    db = pd.read_sql("SELECT * FROM artists", conn)
    db.columns = db.columns.str.strip()
    db = db.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # Group by "Artist" and sum "Times Played"
    #db = db.drop_duplicates(keep='last')
    db = db.groupby("Artist", as_index=False).agg({
        #"Artist": "first",
        "Songs Listened To": 'max'  # Sum up play counts
    })
    db.to_sql("artists", conn, if_exists="replace", index=False)
    # Write the cleaned data back to SQLite
    #db.to_csv("times", conn, if_exists="replace", index=False)
    db.to_csv("artists.csv", header=True, index=False)

def fix_images():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM main")
    data = cursor.fetchall()
    for row in data:
        old = row[3]
        # if 'url' not in old:
        #     cursor.execute('SELECT "Image_Info" FROM main WHERE "Album" = ?', (row[2],))
        #     old = cursor.fetchone()[0]
        # else:
        #     continue
        new = ""
        if "tps" in old[0:3]:
            new = "ht" + old
        else:
            new = "https:" + old 
        #index1 = old.find('url')
        #index2 = old.find(',', index1)
        #new = old[index1+5:index2]
        #print(new)
        cursor.execute('UPDATE main SET "Image_Info" = ? WHERE "Song Name" = ? AND "Artists" = ?', (new, row[0], row[1],))
    conn.commit()


#fix_images()
times()
conn.close()
