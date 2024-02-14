import requests
import pandas as pd
from sqlalchemy import create_engine

# Database configuration settings
DB_CONFIG = {
    'host': 'localhost',  
    'database': 'nycopendatadb',
    'user': 'postgres',  
    'password': 'PLACEHOLDER',  
    'port': '5432'
}

# Fetch data from the NYC Open Data API
DATA_URL = "https://data.cityofnewyork.us/resource/k397-673e.json"
response = requests.get(DATA_URL)

if response.status_code == 200:
    # Convert the data to a DataFrame
    data = response.json()
    df = pd.DataFrame(data)

    # Take a subset of this DataFrame, for example, the first 10 rows
    sample_df = df.head(10)

    # Database connection URL
    db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    engine = create_engine(db_url)

    # Insert the sample data into the database, into the 'sample_data' table of the 'test_db' schema
    sample_df.to_sql('sample_data', engine, schema='test_db', if_exists='append', index=False)
    print("Data inserted successfully.")
else:
    print(f"Failed to retrieve data: {response.status_code}")



