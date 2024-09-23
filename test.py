import requests
import json

# Define the API endpoint
api_url = "http://127.0.0.1:5000/process"

# Load the JSON data from a file
with open("test.json", 'r') as file:
    json_data = json.load(file)

# Make the API call with the JSON data
response = requests.post(api_url, json=json_data)

# Check if the request was successful
if response.status_code == 200:
    # Parse the updated JSON from the response
    updated_data = response.json()

    # Save the updated data as a new JSON file
    with open('new.json', 'w') as new_file:
        json.dump(updated_data, new_file, indent=4)
    print("File successfully saved as new.json")
else:
    print(f"Failed to get a valid response. Status code: {response.status_code}")
