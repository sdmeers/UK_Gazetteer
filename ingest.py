
import pandas as pd
import sqlite3
import os

CSV_FILE = 'GBPN.csv'
DB_FILE = 'gazetteer.db'
TABLE_NAME = 'places'
CHUNK_SIZE = 10000  # Process 10,000 rows at a time

def create_database():
    """
    Reads data from the large CSV file in chunks and writes it to an SQLite database.
    """
    if os.path.exists(DB_FILE):
        print(f"Database file '{DB_FILE}' already exists. Deleting it to rebuild with new schema.")
        os.remove(DB_FILE)

    print(f"Creating SQLite database '{DB_FILE}' from '{CSV_FILE}'...")

    # Establish a connection to the SQLite database
    conn = sqlite3.connect(DB_FILE)

    # Use pandas to read the CSV in chunks
    chunk_iter = pd.read_csv(CSV_FILE, chunksize=CHUNK_SIZE, usecols=['PlaceName', 'Lat', 'Lng', 'HistCounty'], on_bad_lines='skip')

    for i, chunk in enumerate(chunk_iter):
        # Clean column names (remove leading/trailing spaces)
        chunk.columns = chunk.columns.str.strip()
        
        # Write the chunk to the SQLite table
        chunk.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
        print(f"Processed chunk {i+1}...")

    print("\nData ingestion complete.")

    # Create an index on the PlaceName column for faster lookups
    print("Creating indexes...")
    cursor = conn.cursor()
    cursor.execute(f"CREATE INDEX idx_placename ON {TABLE_NAME} (PlaceName);")
    cursor.execute(f"CREATE INDEX idx_histcounty ON {TABLE_NAME} (HistCounty);")
    conn.commit()
    print("Indexes created successfully.")

    # Close the connection
    conn.close()
    print(f"Database '{DB_FILE}' created and populated.")

if __name__ == "__main__":
    create_database()

