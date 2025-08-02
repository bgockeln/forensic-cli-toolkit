import sqlite3
from datetime import datetime, timedelta
import csv
import os #
import sys #

def analyze_bookmarks(db_path):
    
    # Check if file exists
    if not os.path.exists(db_path):
        print("Error: places.sqlite not found in ./browser_profile.")
        sys.exit(1)

    print("File found. Proceeding...")

    # Connect to SQLite DB and create a cursor to execute queries.
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to retrieve URLS, title, visit counts and last visit dates.
    query = """
    SELECT moz_bookmarks.title, moz_places.url, moz_places.visit_count, moz_places.last_visit_date
    FROM moz_bookmarks
    JOIN moz_places ON moz_bookmarks.fk = moz_places.id
    WHERE moz_bookmarks.type = 1
    ORDER BY moz_places.visit_count DESC
    """

    # Execute the SQL query.
    cursor.execute(query)

    # Creates the CSV file and writes the results into it.
    with open("bookmarks_export.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Visit Count", "Title", "URL"])

        # Loop through all results returned by the query.
        for row in cursor.fetchall():
            title = row[0]
            url = row[1]
            count = row[2]
            timestamp = row[3]
  
            # Convert Firefox timestamp to a datetime object.
            if timestamp: 
                ts = datetime(1970, 1, 1) + timedelta(microseconds=timestamp)
            else:
                ts = "N/A"
    
            # Write each row of actual browsing data to the CSV file.
            writer.writerow([ts, count, title, url])

    print("Analysis Complete")

    # Close DB conection.
    conn.close()
