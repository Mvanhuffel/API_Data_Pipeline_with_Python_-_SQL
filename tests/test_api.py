import requests
import pandas as pd

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
    # Fetch data from API
    data = fetch_data(DATA_URL)

    # Convert to pandas DataFrame
    df = pd.DataFrame(data)

    # Display the first few rows of the dataframe
    print("Head of the DataFrame:")
    print(df.head())

    # DataFrame structure
    print("\nDataFrame Structure:")
    print(df.dtypes)

    # DataFrame description for numeric columns
    print("\nDataFrame Description:")
    print(df.describe())

    # DataFrame shape
    print("\nDataFrame Shape:")
    print(df.shape)

if __name__ == "__main__":
    main()
