# [Data Engineering] Data-Modeling-with-Postgres

# **Introduction**

*1.	Background:*
    
   A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.

*2.	Challenge:*
   
   Currently, there is no easy way to query their data. Songs and user activity data are stored seperately in JASON files format.  

*3.	Goal:*
    
   Create a PostgreSQL database schema and ETL pipeline to optimize queries that can join both tables.
   
   Test database and ETL pipeline by running queries

# Project Description

1.	Define fact and dimension tables for a star schema for a particular analytic focus.

2.	Write an ETL pipeline that transfers data from files in two local directories files into these tables in PostgreSQL using Python and SQL.


## Required Python Libraries/Installation

    1.	Python 3

    2.	Psycopg2 and pandas

    3.	PostgreSQL database on localhost

## Running Python Scripts

1.	At terminal: 
       
        •	python create_tables.py
        •	Python etl.py

2.	At Jupyter Notebook:
        
        •	etl.ipynb
        •	test.ipynb

## Project Files:

1.	**data/song_data**: consists a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

        song_data/A/B/C/TRABCEI128F424C983.json
        song_data/A/A/B/TRAABJL12903CDCF1A.json

  And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

         {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

2.	**Data/log_data**:  consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations. For example, here are filepaths to two files in this dataset.

        log_data/2018/11/2018-11-12-events.json
        log_data/2018/11/2018-11-13-events.json
 
  Below is an example of what the data in a log file, 2018-11-12-events.json, looks like.

 
3.	**test.ipynb**: displays the first few rows of each table to check database.

4.	**create_tables.py**: drops and creates your tables. Run this file to reset the tables before each time running ETL scripts.

5.	**etl.ipynb**: reads and processes a single file from song_data and log_data and loads the data into the tables. This notebook contains detailed instructions on the ETL process for each of the tables.

6.	**etl.py**:  reads and processes files from song_data and log_data and loads them into the  tables. 

7.	**sql_queries.py**: contains all sql queries, and is imported into the last three files above.

8.	**README.md**: provides discussion of the project.

# APPROACH TO PROJECT:

## DATABASE SCHEMA:
  I created below star schema that normalizes two big data sets which includes a fact table and 4 dimension tables:
 
 ![alt text](https://github.com/dannyledao/Data-Modeling-with-Postgres/blob/567448a37012706b0d6f034f651c92c59218dffc/schema%20table.PNG)
## PROJECT STEPS:

1.	Create tables in *sql_queries.py* and run *create_tables.py* to create database and tables.

2.	Run *test.ipynb* to confirm the creation of tables with correct columns. Restart kernel to close connection to the database after running this notebook.

3.	Built ETL process in *etl.ipynb* notebook to develop ETL processes for each table. After running ETL process, run *test.ipynb* to confirm that records were successfully inserted into each table. Re-run *create_tables.py* to reset tables before each time running *etl.ipynb*

      a.	Songs table: 
        
        •	Use pandas.read_json fuction to read in song metadata file. 
        
        •	Select all fields listed as columns in the dimension table:  song_table_create  in the schema below. 
        
        •	Add insert query to song_table to PostgreSQL
        
        •	Iterate the process by looping through all song json files.

      b.	Artists table

        •	Use pandas.read_json function to read in song metadata file.

        •	Select all fields listed as columns in the dimension table:  artist_table_create  in the schema below. 

        •	Add insert query to artist_table to PostgreSQL

        •	Iterate the process by looping through all song json files.

     c.	Time table
        
        •	Use pandas.read_json to read in user activity log data

        •	Use NextSong function to filter records

        •	Convert start_time’s timestamp values to date time using pandas. 

        •	Select all fields listed as columns in the dimension table:  time_table_create  in the schema below. 
        
        •	Add insert query to time_table to PostgreSQL
        
        •	Iterate the process by looping through all log json files.
      
      d.	 Similar steps are performed for user table
      
      e.	Songplay table

        •	Use pandas.read_json to read in user activity log data

        •	Use NextSong function to filter records

        •	Select all fields listed as columns in the dimension table:  songplay_table_create  in the schema below. 

        •	Since song_id and artist_id are not included in user activity log data, use SQL query to get this data from song table and artist table created above or from song data file.

        •	Iterate the process by looping through all log json files.


4.	Built ETL Pipeline in etl.py to process the entire datasets. Run create_tables.py before running etl.py to reset tables. Run test.ipynb to confirm records were successfully inserted to each table


