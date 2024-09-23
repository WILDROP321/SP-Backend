import requests
import json
from app import process_json

# Define the API endpoint
api_url = "http://52.66.37.220:5000/process"

# Load the JSON data from a file
with open("test.json", 'r') as file:
    json_data = json.load(file)

updated_data = process_json(json_data)

# Save the updated data as a new JSON file
with open('new.json', 'w') as new_file:
    json.dump(updated_data, new_file, indent=4)
print("File successfully saved as new.json")

