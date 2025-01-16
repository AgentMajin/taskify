# userID = None

import json, os, sys

# Use the absolute path to construct the storage file path
storage_file = os.path.join(os.path.dirname(__file__), "..", "context", "user_data.json")

def save_user_id(user_id):
    try:
        with open(storage_file, "w") as file:
            json.dump({"userID": user_id}, file)
    except IOError:
        print("Error writing to file")

def load_user_id():
    if os.path.exists(storage_file):
        with open(storage_file, "r") as file:
            data = json.load(file)
            return data.get("userID", None)
    return None
