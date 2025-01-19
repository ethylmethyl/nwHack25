import os
import csv
from typing import NamedTuple, List, Optional
from enum import Enum

class FloorPreference(Enum):
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"

class UserData(NamedTuple):
    cst: int  # Cost (required integer)
    location: bool  # Location (True = on campus, False = off)
    descr: Optional[str]  # Description (optional string)
    rooms: Optional[int]  # Number of rooms (optional integer)
    ppl: Optional[int]  # Number of people (optional integer)
    length: Optional[str]  # Lease length (optional string)
    laundry: Optional[bool]  # Laundry available (optional boolean)
    parking: Optional[bool]  # Parking available (optional boolean)
    gender: Optional[str]  # Gender preference (optional string)
    floor: Optional[FloorPreference]  # Preferred floor (optional enum)
    pets: Optional[bool]  # Pets allowed (optional boolean)

def lease_length_comparator(length: Optional[str]) -> int:
    """Convert lease length to an integer representing the lease duration for sorting."""
    if not length:
        return 0  # No preference or no length
    length = length.lower()
    if "month" in length:
        return int(length.split()[0])
    elif "year" in length:
        return int(length.split()[0]) * 12  # Convert years to months
    elif "week" in length:
        return int(length.split()[0]) // 4  # Convert weeks to months (approx.)
    return 0

def read_user_data_from_csv(filename: str) -> List[UserData]:
    user_data_list = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not any(row.values()):  # Skip empty rows
                    continue

                floor = None
                if row.get('floor'):
                    try:
                        floor = FloorPreference[row['floor'].upper()]
                    except KeyError:
                        pass

                def parse_yes_no(value: str) -> Optional[bool]:
                    return value.lower() == 'yes' if value else None

                user_data_list.append(UserData(
                    cst=int(row['cst']) if row['cst'] and row['cst'].isdigit() else 0,
                    location=parse_yes_no(row['location']),
                    descr=row.get('descr', None),
                    rooms=int(row['rooms']) if row['rooms'] and row['rooms'].isdigit() else None,
                    ppl=int(row['ppl']) if row['ppl'] and row['ppl'].isdigit() else None,
                    length=row.get('length', None),
                    laundry=parse_yes_no(row.get('laundry')),
                    parking=parse_yes_no(row.get('parking')),
                    gender=row.get('gender', None),
                    floor=floor,
                    pets=parse_yes_no(row.get('pets')),
                ))
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except Exception as e:
        print(f"An error occurred: {e}")
    return user_data_list

def safe_getattr(obj, attr, default=None):
    """Safely get an attribute, returning a default if it doesn't exist or is None."""
    return getattr(obj, attr, default) if obj else default

def rank_and_sort_all_features(
    user_data_list: List[UserData],
    filters: Optional[dict] = None
) -> List[UserData]:
    """Rank and sort listings based on filters and sort order."""
    if not filters:
        filters = {}

    sort_order = [
        "cst", "location", "rooms", "length", "ppl",
        "laundry", "parking", "gender", "floor", "pets"
    ]
    sort_order = [key for key in filters if key in sort_order] + [key for key in sort_order if key not in filters]

    def calculate_fitness_score(user: UserData) -> int:
        return sum(1 for key, value in filters.items() if value is not None and safe_getattr(user, key) == value)

    def sort_key(user: UserData):
        fitness_score = calculate_fitness_score(user)
        key = [-fitness_score]  # Higher fitness comes first
        for field in sort_order:
            attribute = safe_getattr(user, field)
            if field == "length":
                attribute = lease_length_comparator(attribute)
        # Replace None values with a default for sorting
            if attribute is None:
                attribute = float('inf') if field == "cst" else -float('inf')
            key.append(attribute)
        return tuple(key)


    return sorted(user_data_list, key=sort_key, reverse=True)

def get_user_preferences() -> dict:
    def safe_int(value: str) -> Optional[int]:
        try:
            return int(value) if value else None
        except ValueError:
            return None

    def parse_yes_no(value: str) -> Optional[bool]:
        return value.lower() == 'yes' if value else None

    print("Enter your preferences (leave blank if no preference):")
    cst = safe_int(input("Max Cost: "))
    location = parse_yes_no(input("On Campus (yes/no): "))
    rooms = safe_int(input("Number of Rooms: "))
    ppl = safe_int(input("Number of People: "))
    length = input("Lease Length: ")
    laundry = parse_yes_no(input("Laundry in unit (yes/no): "))
    parking = parse_yes_no(input("Parking available (yes/no): "))
    gender = input("Gender Preference: ")
    floor = input("Floor Preference (bottom/middle/top): ").upper()
    pets = parse_yes_no(input("Pets Allowed (yes/no): "))

    return {
        "cst": cst,
        "location": location,
        "rooms": rooms,
        "ppl": ppl,
        "length": length,
        "laundry": laundry,
        "parking": parking,
        "gender": gender,
        "floor": FloorPreference[floor] if floor in FloorPreference.__members__ else None,
        "pets": pets,
    }

# Example Usage
filename = 'nwhack25/user_data.csv'
user_data_list = read_user_data_from_csv(filename)
user_preferences = get_user_preferences()
ranked_list = rank_and_sort_all_features(user_data_list, filters=user_preferences)

for user in ranked_list:
    print(user)

print("\nSorted Listings (All Listings, Most Fitting to Least Fitting):")
