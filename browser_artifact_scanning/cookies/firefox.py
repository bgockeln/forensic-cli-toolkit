import sqlite3
from datetime import datetime, timedelta
import csv
import os #
import sys #

def analyze_cookies(db_path):
    
    # Check if file exists
    if not os.path.exists(db_path):
        print("Error: cookies.sqlite not found in ./browser_profile.")
        sys.exit(1)

    print("File found. Proceeding...")

    # Connect to SQLite DB and create a cursor to execute queries.
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to retrieve URLS, title, visit counts and last visit dates.
    query = """
    SELECT host, name, value, expiry, lastAccessed, creationTime, isSecure, isHttpOnly, sameSite
    FROM moz_cookies
    ORDER BY lastAccessed DESC
    """

    # Execute the SQL query.
    cursor.execute(query)

    # Creates the CSV file and writes the results into it.
    with open("cookies_export.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Host", "Name", "Value", "Expiry", "Last Accessed", "Creation Time", "Is Secure", "Is Http Only", "Same Site"])

        # Loop through all results returned by the query.
        for row in cursor.fetchall():
            host = row[0]
            name = row[1]
            value = row[2]
            expiry = row[3]
            lastAccessed = row[4]
            creationTime = row [5]
            isSecure = row [6]
            isHttpOnly = row [7]
            sameSite = row [8]
  
            # Convert Firefox timestamp to a datetime object.
            if lastAccessed:
                lastAccessedTime = datetime(1970, 1, 1) + timedelta(microseconds=lastAccessed)
            if creationTime: 
                creationTimeFormatted = datetime(1970, 1, 1) + timedelta(microseconds=creationTime)
            else:
                creationTimeFormatted = "N/A"
    
            # Write each row of actual browsing data to the CSV file.
            writer.writerow([host, name, value, expiry, value, lastAccessed, creationTime, isSecure, isHttpOnly, sameSite])

    print("Analysis Complete")

    # Close DB conection.
    conn.close()