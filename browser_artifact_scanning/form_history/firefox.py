# sqlite3 to interact with SQLite databases.# csv to create and or save the results in a csv file.
# os and datetime for path and timestamp handling.
# sys for a clean exit after the error message.
import sqlite3
import csv
from datetime import datetime, timedelta
import sys
import os

def analyze_form_history(db_path):
    
    # Check if file exists
    if not os.path.exists(db_path):
        print("Error: places sqlite not found in ./browser_profile.")
        sys.exit(1)

    print("File found. Proceeding...")

    # Connect to the SQLite Db and create a cursor to execute queries.
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to retrieve info
    query = """
    SELECT fieldname, value, timesUsed, firstUsed, lastUsed
    FROM moz_formhistory
    ORDER BY timesUsed DESC
    """

    # Execute the SQL query.
    cursor.execute(query)

    # Creates the CSV file and writes the results into it.
    with open("form_history.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Field Name", "Value", "Times Used", "First Used", "Last Used"])

        # Loop through all results returned by the query.
        for row in cursor.fetchall():
            fieldname = row[0]
            value = row[1]
            timesUsed = row[2]

            # Convert Firefox timestamps
            def convert_timestamp(microsec):
                if microsec:
                    return datetime(1970, 1, 1) + timedelta(microseconds=microsec)
                else:
                    return "N/A"

            firstUsed = convert_timestamp(row[3])
            lastUsed = convert_timestamp(row[4])

            # Write each row of actual form data to the CSV file.
            writer.writerow([fieldname, value, timesUsed, firstUsed, lastUsed])

    print("Analysis Complete")

    # Close DB connection
    conn.close()
