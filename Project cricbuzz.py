import json

# Load JSON file
with open("sample_cricket_data.json", "r") as f:
    data = json.load(f)

# Print to confirm
print(json.dumps(data, indent=4))
