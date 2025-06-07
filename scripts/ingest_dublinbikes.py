import os, requests, duckdb, pathlib, datetime
import pandas as pd

DB_FILE = os.getenv("DB_FILE", "warehouse.duckdb")

API_URL = "https://api.cyclocity.fr/contracts/dublin/gbfs/v2"
FEEDS = {
    "station_information": "station_information.json",
    "station_status": "station_status.json"
}

def fetch(feed_endpoint):
    url = f"{API_URL}/{feed_endpoint}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["data"]["stations"]

def main(db_path):
    conn = duckdb.connect(db_path)
    for name, endpoint in FEEDS.items():
        records = fetch(endpoint)
        df = pd.DataFrame(records)
        
        # Drop existing table
        conn.execute(f"DROP TABLE IF EXISTS raw__{name}")
        
        # Create table from DataFrame
        conn.execute(f"CREATE TABLE raw__{name} AS SELECT * FROM df")
    
    conn.close()
    print(f"[{datetime.datetime.now()}] Ingested {len(FEEDS)} feeds into {db_path}")


if __name__ == "__main__":
    main(DB_FILE)