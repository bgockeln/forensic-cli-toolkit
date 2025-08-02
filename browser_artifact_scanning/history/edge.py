# sqlite3 to interact with SQLite databases.
# datetime and timedelta to convert Firefoxes timestamps to human-readable dates.
# csv to create and or save the results as a csv file
import sqlite3
from datetime import datetime, timedelta
import csv
import os #
import sys #

def analyze_history(db_path):
    
    # Check if file exists
    if not os.path.exists(db_path):
        print("Error: places sqlite not found in ./browser_profile.")
        sys.exit(1)

    print("File found. Proceeding...")

    # Connect to SQLite DB and create a cursor to execute queries.
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to retrieve URLS, title, visit counts and last visit dates.
    query = """
    SELECT
        urls.title,
        COUNT(visits.id) AS real_visit_count,
        MAX(visits.visit_time) AS last_visit_time,
        urls.url
    FROM visits
    JOIN urls ON visits.url = urls.id
    GROUP BY urls.id
    ORDER BY real_visit_count DESC
    Limit 50;
    """

    # Execute the SQL query.
    cursor.execute(query)

    # Creates the CSV file and writes the results into it.
    with open("history_export.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerow(["Title", "Visit Count", "Last Visit Time", "URL"])

        # Loop through all results returned by the query.
        for row in cursor.fetchall():
            title = row[0]
            visit_count = row[1]
            timestamp = row[2]
            url = row[3]
  
            # Convert Firefox timestamp to a datetime object.
            if timestamp: 
                ts = datetime(1601, 1, 1) + timedelta(microseconds=timestamp)
            else:
                ts = "N/A"
            # Write each row of actual browsing data to the CSV file.
            writer.writerow([title, visit_count, ts, url])

    print("Analysis Complete")

    # Close DB conection.
    conn.close()
