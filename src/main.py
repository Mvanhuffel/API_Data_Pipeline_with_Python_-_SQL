import requests
import json

# Socrata Open Data API endpoint for the Citywide Payroll Data (Fiscal Year)
DATA_URL = "https://data.cityofnewyork.us/resource/k397-673e.json"

response = requests.get(DATA_URL)  # Add `, headers=headers` if using an App Token

# Check if the request was successful
if response.status_code == 200:
    # Load the response data into a Python list
    data = json.loads(response.text)
    
    # Print out the first few items from the dataset
    print(json.dumps(data[:5], indent=2))  # Adjust the slice as needed to see more or fewer items
else:
    print(f"Failed to retrieve data: {response.status_code}")

