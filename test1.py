from flask import Flask, request, jsonify, session
from enum import Enum
from typing import Optional, List
import csv
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session handling

# Enum for floor preference
class FloorPreference(Enum):
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"

# Data structure for user data
class UserData:
    def __init__(self, cst, location, descr, rooms, ppl, length, laundry, parking, gender, floor, pets):
        self.cst = cst
        self.location = location
        self.descr = descr
        self.rooms = rooms
        self.ppl = ppl
        self.length = length
        self.laundry = laundry
        self.parking = parking
        self.gender = gender
        self.floor = floor
        self.pets = pets

    def to_dict(self):
        return {
            "cst": self.cst,
            "location": self.location,
            "descr": self.descr,
            "rooms": self.rooms,
            "ppl": self.ppl,
            "length": self.length,
            "laundry": self.laundry,
            "parking": self.parking,
            "gender": self.gender,
            "floor": self.floor.value if self.floor else None,
            "pets": self.pets
        }

    def matches_filter(self, filters):
        for key, value in filters.items():
            if value is not None and getattr(self, key, None) != value:
                return False
        return True

def match_filter(filter1, filter2):
    for key, value in filter2.items():
        print("key")
        print(key)
        if value is not None and filter1[key] != value:
            return False
    return True

# Read user data from the CSV file
def read_user_data(filename: str) -> List[UserData]:
    user_data_list = []
    if not os.path.exists(filename):
        return user_data_list
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            
            user_data_list.append(UserData(
                cst=int(row['cst']) if row['cst'] else None,
                location=row['location'].lower() == 'true' if row['location'] else None,
                descr=row.get('descr'),
                rooms=int(row['rooms']) if row['rooms'] else None,
                ppl=int(row['ppl']) if row['ppl'] else None,
                length=row.get('length'),
                laundry=row['laundry'].lower() == 'true' if row['laundry'] else None,
                parking=row['parking'].lower() == 'true' if row['parking'] else None,
                gender=row.get('gender'),
                floor=FloorPreference[row['floor'].upper()] if (row.get('floor') and row['floor'].upper() in FloorPreference.__members__)    else None,
                pets=row['pets'].lower() == 'true' if row['pets'] else None
            ))
    return user_data_list

@app.route('/filters', methods=['POST'])
def set_filters():
    try:
        filters = request.get_json()

        # Validate and store filters in session
        session['filters'] = {
            'cst': int(filters['cst']) if 'cst' in filters and filters['cst'] else None,
            'location': filters['location'].lower() == 'true' if 'location' in filters else None,
            'rooms': int(filters['rooms']) if 'rooms' in filters and filters['rooms'] else None,
            'ppl': int(filters['ppl']) if 'ppl' in filters and filters['ppl'] else None,
            'length': filters.get('length'),
            'laundry': filters['laundry'].lower() == 'true' if 'laundry' in filters else None,
            'parking': filters['parking'].lower() == 'true' if 'parking' in filters else None,
            'gender': filters.get('gender'),
            'floor': filters['floor'].lower() if 'floor' in filters and filters['floor'].upper() in FloorPreference.__members__ else None,
            'pets': filters['pets'].lower() == 'true' if 'pets' in filters else None
        }
        return jsonify({"message": "Filters set successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/listings', methods=['GET'])
def get_listings():
    filename = 'nwhack25/user_data.csv'  # Path to your CSV file

    try:
        # Retrieve filters from session
        filters = session['filters']

        print("filter values")
        print(filters)

        if not filters:
            return jsonify({"message": "No filters set. Use POST /filters to set filters."}), 400

        # Read data from CSV and apply filters
        user_data_list = read_user_data(filename)
        filtered_data = [user.to_dict() for user in user_data_list if match_filter(user.to_dict(), filters)]


        return jsonify(filtered_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_post', methods=['POST'])
def add_post():
    filename = 'nwhack25/user_data.csv'

    data = request.get_json()
    try:
        # Parse request JSON

        # Validate and construct new user data
        new_user = {
            "cst": int(data['cst']),
            "location": data['location'].lower() == 'true',
            "descr": data.get('descr', ''),
            "rooms": int(data['rooms']) if 'rooms' in data else None,
            "ppl": int(data['ppl']) if 'ppl' in data else None,
            "length": data.get('length', ''),
            "laundry": data['laundry'].lower() == 'true' if 'laundry' in data else None,
            "parking": data['parking'].lower() == 'true' if 'parking' in data else None,
            "gender": data.get('gender', ''),
            "floor": data['floor'].upper() if 'floor' in data else None,
            "pets": data['pets'].lower() == 'true' if 'pets' in data else None
        }

        # Append to CSV
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=new_user.keys())
            if not file_exists:
                writer.writeheader()  # Write header if file is new
            writer.writerow(new_user)

        return jsonify({"message": "Post added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
