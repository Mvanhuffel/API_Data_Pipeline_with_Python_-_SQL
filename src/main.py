import requests
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.sql import bindparam
from config.db_config import DB_CONFIG

# Function to insert data and return inserted IDs for foreign key relationships
def insert_and_return_id(df, table_name, engine, return_column, match_column):
    inserted_ids = []
    with engine.connect() as conn:
        for _, row in df.iterrows():
            # Create a list of bindparam objects for each column
            bindings = [bindparam(col, value=row[col]) for col in row.index]

            # Prepare the SQL statement with named placeholders, including the schema name
            stmt = text(f"""
                INSERT INTO payroll_data.{table_name} ({', '.join(row.index)})
                VALUES ({', '.join([f':{col}' for col in row.index])})
                ON CONFLICT ({match_column}) DO UPDATE
                SET {match_column} = EXCLUDED.{match_column}
                RETURNING {return_column};
            """).bindparams(*bindings)

            # Execute the statement
            result = conn.execute(stmt)
            inserted_ids.append(result.fetchone()[0])
    return inserted_ids

# Fetch data from the API
DATA_URL = "https://data.cityofnewyork.us/resource/k397-673e.json"
response = requests.get(DATA_URL)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)

    # Drop rows where 'mid_init' is NaN
    df.dropna(subset=['mid_init'], inplace=True)

    # Convert columns to appropriate data types
    df['fiscal_year'] = pd.to_numeric(df['fiscal_year'], errors='coerce').astype('Int64')
    df['payroll_number'] = pd.to_numeric(df['payroll_number'], errors='coerce').astype('Int64')
    numeric_columns = ['base_salary', 'regular_hours', 'regular_gross_paid', 'ot_hours', 'total_ot_paid', 'total_other_pay']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Database connection
    db_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    engine = create_engine(db_url)

    # Insert into 'agencies'
    agencies_df = df[['agency_name', 'payroll_number']].drop_duplicates()
    df['agency_id'] = insert_and_return_id(agencies_df, 'agencies', engine, 'agency_id', 'agency_name')

    # Insert into 'employees'
    employees_df = df[['last_name', 'first_name', 'mid_init', 'agency_start_date']].drop_duplicates()
    df['employee_id'] = insert_and_return_id(employees_df, 'employees', engine, 'employee_id', 'last_name')

    # Insert into 'positions'
    positions_df = df[['title_description', 'pay_basis']].drop_duplicates()
    df['title_id'] = insert_and_return_id(positions_df, 'positions', engine, 'title_id', 'title_description')

    # Insert into 'work_locations'
    locations_df = df[['work_location_borough']].drop_duplicates()
    df['location_id'] = insert_and_return_id(locations_df, 'work_locations', engine, 'location_id', 'work_location_borough')

    # Insert into 'payroll'
    payroll_df = df[['employee_id', 'agency_id', 'title_id', 'location_id', 'fiscal_year', 'leave_status_as_of_june_30', 'base_salary', 'regular_hours', 'regular_gross_paid', 'ot_hours', 'total_ot_paid', 'total_other_pay']]
    payroll_df.to_sql('payroll', engine, schema='payroll_data', if_exists='append', index=False) # Ensure schema is correct
else:
    print(f"Failed to retrieve data: {response.status_code}")




