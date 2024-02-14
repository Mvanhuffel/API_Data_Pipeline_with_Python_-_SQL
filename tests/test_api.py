import pandas as pd
import requests

# Socrata Open Data API endpoint for the Citywide Payroll Data (Fiscal Year)
DATA_URL = "https://data.cityofnewyork.us/resource/k397-673e.json"

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")

def main():
    data = fetch_data(DATA_URL)

    df = pd.DataFrame(data)

    # 1. Data profiling and summary
    print("\n1. Data profiling and summary:")
    print(df.info())

    # 2. Data quality checks
    print("\n2. Data quality checks:")

    # Checking for missing values
    print("\n3. Checking for missing values:")
    print(df.isnull().sum())

    # Checking for duplicate rows
    print("\n4. Checking for duplicate rows:")
    print(df.duplicated().sum())

    # 3. Data distribution and uniqueness
    print("\n5. Data distribution and uniqueness:")

    # Displaying the number of unique values in each column
    print(df.nunique())

    # 5. Data type analysis
    print("\n6. Data type analysis:")
    print(df.dtypes)

    # 6. Sample data extraction
    print("\n7. Sample data extraction:")
    print(df.sample(5))

    # 7. First few rows
    print("\n8. First few rows:")
    print(df.head())

    # 8. Shape
    print("\n9. Shape:")
    print(df.shape)

if __name__ == "__main__":
    main()








