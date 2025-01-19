import os
import csv
from typing import NamedTuple, List, Optional
from enum import Enum

class Location(Enum):
    BROCK_COMMONS = "Brock Commons"
    EXCHANGE = "Exchange"
    FAIRVIEW_CRESCENT = "Fairview Crescent"
    FRASER_HALL = "Fraser Hall"
    GREEN_COLLEGE = "Green College"
    IONA_HOUSE = "Iona House"
    MARINE_DRIVE = "Marine Drive"
    PONDEROSA_COMMONS = "Ponderosa Commons"
    ST_JOHNS_COLLEGE = "St. John’s College"
    TESHXWHELELMS_TEKWAƛKEʔAʔL = "tə šxʷhəleləm̓s tə k̓ʷaƛ̓kʷəʔaʔɬ"
    WESBROOK_VILLAGE = "Wesbrook Village"
    KITSILANO = "Kitsilano"
    RICHMOND = "Richmond"
    WEST_POINT_GREY = "West Point Grey"

class FloorPreference(Enum):
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"

class UserData(NamedTuple):
    cst: int  # Cost (required integer)
    location: Location  # Location (Enum)
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
        months = int(length.split()[0])
        return months
    elif "year" in length:
        years = int(length.split()[0])
        return years * 12  # Convert years to months for comparison
    return 0

def read_user_data_from_csv(filename: str) -> List[UserData]:
    user_data_list = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not any(row.values()):  # Skip empty rows
                    continue
                
                # Handle invalid location values
                try:
                    location = Location[row['location'].replace(' ', '_').upper()]  # Map to Enum
                except KeyError:
                    continue

                floor = None
                if row['floor']:
                    try:
                        floor = FloorPreference[row['floor'].upper()]
                    except KeyError:
                        pass

                laundry = row['laundry'].lower() == 'true' if row['laundry'] else None
                parking = row['parking'].lower() == 'true' if row['parking'] else None
                pets = row['pets'].lower() == 'true' if row['pets'] else None
                rooms = int(row['rooms']) if row['rooms'] and row['rooms'].isdigit() else None
                ppl = int(row['ppl']) if row['ppl'] and row['ppl'].isdigit() else None
                length = row['length'] if row['length'] else None
                descr = row['descr'] if row['descr'] else None
                gender = row['gender'] if row['gender'] else None
                cst = int(row['cst']) if row['cst'] and row['cst'].isdigit() else None

                user_data_list.append(UserData(
                    cst=cst,
                    location=location,
                    descr=descr,
                    rooms=rooms,
                    ppl=ppl,
                    length=length,
                    laundry=laundry,
                    parking=parking,
                    gender=gender,
                    floor=floor,
                    pets=pets
                ))
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except Exception as e:
        print(f"An error occurred: {e}")
    return user_data_list
    
from typing import List, Dict

def filter_and_sort_listings(
    user_data_list: List[UserData], 
    filters: Dict[str, any] = None, 
    sort_preferences: List[str] = None, 
    ascending: bool = True
) -> List[UserData]:
    """
    Filter and sort listings based on user preferences.

    Args:
        user_data_list (List[UserData]): List of user data entries.
        filters (Dict[str, any]): A dictionary of filters. Keys are field names and values are desired values.
        sort_preferences (List[str]): List of fields to sort by in order of priority.
        ascending (bool): Sort order. True for ascending, False for descending.

    Returns:
        List[UserData]: Filtered and sorted list of UserData entries.
    """
    if filters:
        # Apply filters
        for key, value in filters.items():
            if value is not None:
                user_data_list = [user for user in user_data_list if getattr(user, key, None) == value]

    if not sort_preferences:
        # Default to cost if no sorting preferences are provided
        sort_preferences = ['cst']

    # Sorting logic
    def sort_key(user: UserData):
        key = []
        for field in sort_preferences:
            attribute = getattr(user, field, None)
            if field == 'length':
                attribute = lease_length_comparator(attribute)  # Special handling for lease length
            key.append(attribute if ascending else -attribute if isinstance(attribute, (int, float)) else attribute)
        return tuple(key)

    return sorted(user_data_list, key=sort_key)

def get_user_preferences() -> Dict[str, any]:
    def safe_int(value: str) -> Optional[int]:
        try:
            return int(value) if value else None
        except ValueError:
            return None

    print("Enter your preferences (leave blank if no preference):")
    cst = safe_int(input("Max Cost: "))
    location = input("Preferred Location: ")
    rooms = safe_int(input("Number of Rooms: "))
    ppl = safe_int(input("Number of People: "))
    length = input("Lease Length: ")
    laundry = input("Laundry (true/false): ")
    parking = input("Parking (true/false): ")
    gender = input("Gender Preference: ")
    floor = input("Floor Preference (bottom/middle/top): ")
    pets = input("Pets Allowed (true/false): ")

    return {
        "cst": cst,
        "location": Location[location.replace(' ', '_').upper()] if location else None,
        "rooms": rooms,
        "ppl": ppl,
        "length": length if length else None,
        "laundry": laundry.lower() == 'true' if laundry else None,
        "parking": parking.lower() == 'true' if parking else None,
        "gender": gender if gender else None,
        "floor": FloorPreference[floor.upper()] if floor else None,
        "pets": pets.lower() == 'true' if pets else None,
    }

def safe_getattr(obj, attr, default=None):
    """
    Safely get an attribute, returning a default if it doesn't exist or is None.
    """
    return getattr(obj, attr, default) if obj else default

def rank_and_sort_all_features(
    user_data_list: List[UserData],
    filters: Dict[str, any] = None
) -> List[UserData]:
    """
    Rank and sort listings based on all features, prioritizing cost, location, and user-defined preferences.
    Displays all listings, regardless of matching filters.
    """
    if not filters:
        filters = {}

    # Define the order of importance for sorting
    sort_order = [
        "cst", "location", "rooms", "length", "ppl",
        "laundry", "parking", "gender", "floor", "pets"
    ]

    sort_order = [key for key in filters if key in sort_order] + [key for key in sort_order if key not in filters]
    location_priority = {loc: i for i, loc in enumerate(Location)}

    def calculate_fitness_score(user: UserData) -> int:
        score = 0
        for key, value in filters.items():
            if value is not None and safe_getattr(user, key) == value:
                score += 1
        return score

    def sort_key(user: UserData):
        fitness_score = calculate_fitness_score(user)
        key = [-fitness_score]
        for field in sort_order:
            attribute = safe_getattr(user, field)
            if field == "length":
                attribute = lease_length_comparator(attribute)
            elif field == "location" and attribute:
                attribute = location_priority.get(attribute, float("inf"))
            key.append(attribute if isinstance(attribute, (int, float)) else str(attribute))
        return tuple(key)

    return sorted(user_data_list, key=sort_key, reverse=True)

# Example Usage
filename = 'nwhack25/user_data.csv'
user_data_list = read_user_data_from_csv(filename)
user_preferences = get_user_preferences()
ranked_list = rank_and_sort_all_features(user_data_list, filters=user_preferences)

print("\nSorted Listings (All Listings, Most Fitting to Least Fitting):")
for user in ranked_list:
    print(user)

