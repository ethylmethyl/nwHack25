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
            
            # Debugging: Print headers to verify
            print(f"CSV Headers: {reader.fieldnames}")
            
            for row in reader:
                print(f"Reading row: {row}")  # Debugging: see the rows being read

                if not any(row.values()):  # Skip empty rows
                    print("Skipping empty row.")
                    continue
                
                # Handle invalid location values
                try:
                    location = Location[row['location'].replace(' ', '_').upper()]  # Map to Enum
                except KeyError:
                    print(f"Invalid location value in row: {row['location']}")
                    continue

                # Handle optional fields
                floor = None
                if row['floor']:
                    try:
                        floor = FloorPreference[row['floor'].upper()]
                    except KeyError:
                        print(f"Invalid floor value in row: {row['floor']}")

                laundry = row['laundry'].lower() == 'true' if row['laundry'] else None
                parking = row['parking'].lower() == 'true' if row['parking'] else None
                pets = row['pets'].lower() == 'true' if row['pets'] else None
                rooms = int(row['rooms']) if row['rooms'] else None
                ppl = int(row['ppl']) if row['ppl'] else None
                length = row['length'] if row['length'] else None
                descr = row['descr'] if row['descr'] else None
                gender = row['gender'] if row['gender'] else None
                cst = int(row['cst'])  # Ensure cost is an integer

                # Create UserData instance and add it to the list
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

            print(f"Total records read: {len(user_data_list)}")  # Debugging: count of records
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return user_data_list
    
def sort_user_data(user_data_list: List[UserData], preferred_location: Location, ascending_cost: bool) -> List[UserData]:
    sorted_list = sorted(user_data_list, key=lambda user: (
        user.location == preferred_location,  # Primary: prioritize the preferred location
        user.location.value,  # Secondary: sort by location (alphabetically by enum value)
        user.cst if ascending_cost else -user.cst,  # Tertiary: sort by cost (ascending or descending based on preference)
        -lease_length_comparator(user.length)  # Quaternary: sort by lease length (longer is better)
    ), reverse=not ascending_cost)  # Reverse the order if cost is descending
    
    print(f"Sorted list length: {len(sorted_list)}")  # Debugging: see how many records are sorted
    return sorted_list

# Example usage
filename = 'nwhack25/user_data.csv'  # Ensure correct path to the CSV file
LUD1 = read_user_data_from_csv(filename)

# Check if any user data was read
if LUD1:
    print("User data has been read successfully.")
else:
    print("No user data found.")

# Sort and display results
# Proceed with sorting logic if data is found
if LUD1:
    preferred_location = Location.BROCK_COMMONS
    ascending_cost = False
    sorted_users = sort_user_data(LUD1, preferred_location, ascending_cost)

    # Output sorted results
    for user in sorted_users:
        print(user)
