from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

DB_FILE = 'gazetteer.db'
TABLE_NAME = 'places'

app = FastAPI()

class Place(BaseModel):
    placename: str
    lat: float
    lng: float
    histcounty: str

@app.get("/lookup", response_model=List[Place])
def lookup_placename(placename: str, county: Optional[str] = None):
    """
    Looks up a UK place name, with an optional county filter.
    Performs a case-insensitive but exact search.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Use '=' for exact, case-insensitive matching
        query = f"SELECT PlaceName, Lat, Lng, HistCounty FROM {TABLE_NAME} WHERE PlaceName = ? COLLATE NOCASE"
        params = [placename]

        # Add county filter if provided
        if county:
            query += " AND HistCounty = ? COLLATE NOCASE"
            params.append(county)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()

    except sqlite3.OperationalError as e:
        if "no such column" in str(e):
             raise HTTPException(status_code=500, detail=f"Database schema is outdated. Please re-run the ingest.py script.")
        else:
            raise HTTPException(status_code=500, detail=f"Database '{DB_FILE}' not found or other error. Please run the ingest.py script first.")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

    if not results:
        detail = f"Place name matching '{placename}' not found"
        if county:
            detail += f" in county '{county}'"
        raise HTTPException(status_code=404, detail=detail)

    # Convert rows to list of Place models
    places = [Place(placename=row['PlaceName'], lat=row['Lat'], lng=row['Lng'], histcounty=row['HistCounty']) for row in results]
    return places

@app.get("/")
def read_root():
    return {"message": "Welcome to the UK Place Name Gazetteer API. Use the /lookup endpoint to find coordinates."}