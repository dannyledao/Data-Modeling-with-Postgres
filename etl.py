import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """
    Inserting artist and song record into song and artist tables
    cur (psycopg2.cursor): PostgresSQL database cursor
    filepath (str): A filepath to a song file
    """
    
    # open song file
    df = pd.read_json(filepath, lines =True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values.flatten().tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[
        [
            "artist_id",
            "artist_name",
            "artist_location",
            "artist_latitude",
            "artist_longitude",
        ]
    ].values.flatten().tolist()

    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Processes a log file.
    
   
    Inserting time and user records into time and user tables
    cur (psycopg2.cursor): PostgresSQL database cursor
    filepath (str): A filepath to a song file
    """
    
    
    
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df = df[df['page']=='Next Song'].copy()

    # convert timestamp column to datetime
    
    t= pd.to_datetime(df["ts"], unit='ms')   
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.dayofweek, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('time','hour','day','week','month','year','weekday')
    time_df = pd.DataFrame({k: v.values.flatten().tolist() for k,v in zip(column_labels,time_data)})

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e:
            print("Error: Inserting row for table: users")
            print(e)
    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables

            cur.execute(song_select, (row.song, row.artist, row.length))
            results = cur.fetchone()
        
            if results:
                songid, artistid = results
            else:
                songid, artistid = None, None

        # insert songplay record
            songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
            cur.execute(songplay_table_insert, songplay_data)
           
        
def process_data(cur, conn, filepath, func):
   
    """ Process all JSON files in data directory path in both song and log database.
        cur (psycopg2.cursor): PostgreSQL database cursor
        conn (psycopg2.connection): Establishing connection with sparkify database
        filepath (str): directory
        func (function): processing function
   """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """This class/method created to establish connection with database and process song and log data using methods above.
    The class will close the curse and connection with database once finish looping/processing through all JSON files.
 
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
