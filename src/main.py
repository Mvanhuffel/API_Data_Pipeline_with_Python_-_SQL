import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB
import json  # Import the json module
from config.db_config import DB_CONFIG  # Make sure this import matches the location of your config file

# Fetch data from the NYC Open Data API
DATA_URL = "https://data.cityofnewyork.us/resource/k397-673e.json"
response = requests.get(DATA_URL)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    df['data'] = df.apply(lambda x: json.dumps(x.to_dict()), axis=1)

    # Database connection URL
    db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    engine = create_engine(db_url)

    # Insert the data into the 'staging_payroll_data' table of the 'test_db' schema
    df[['data']].to_sql('staging_payroll_data', engine, schema='test_db', if_exists='append', index=False, dtype={'data': JSONB})
    print("Data inserted successfully.")
else:
    print(f"Failed to retrieve data: {response.status_code}")






