# sqlite3 to interact with SQLite databases.
# datetime and timedelta to convert Firefoxes timestamps to human-readable dates.
# csv to create and or save the results as a csv file
import sqlite3
from datetime import datetime, timedelta
import csv
import os #
import sys #
# Path to the Firefox profile database.
db_path = "./browser_profile/places.sqlite"

# Check if file exists
if not os.path.exists("./browser_profile/places.sqlite"):
    print("Error: places sqlite not found in ./browser_profile.")
    sys.exit(1)

print("File found. Proceeding...")

# Connect to SQLite DB and create a cursor to execute queries.
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL query to retrieve URLS, title, visit counts and last visit dates.
query = """
SELECT url, title, visit_count, last_visit_date
FROM moz_places
ORDER BY last_visit_date DESC
Limit 50;
"""

# Execute the SQL query.
cursor.execute(query)

# Creates the CSV file and writes the results into it.
with open("history_export.csv", "w", newline="", encoding="utf-8") as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(["Timestamp", "Visit Count", "Title", "URL"])

  # Loop through all results returned by the query.
  for row in cursor.fetchall():
    url = row[0]
    title = row[1]
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

