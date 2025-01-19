import os
import csv
from typing import NamedTuple
from typing import Optional
from enum import Enum

# Enum for locations
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

# Enum for floor preference
class Floor(Enum):
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"

# Data structure to hold user data
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
    floor: Optional[Floor]  # Preferred floor (optional enum)
    pets: Optional[bool]  # Pets allowed (optional boolean)

def create_and_append_post_to_csv(filename: str):
    # Ensure the directory exists before trying to write the file
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Directory '{directory}' created.")
        except Exception as e:
            print(f"An error occurred while creating the directory: {e}")
            return

    # Gather input from user for the new post
    print("Enter the details for the new post:")

    # Get basic data for the post
    cst = int(input("Cost (in integer): "))
    
    # Handle location input with validation
    location = input("Location (choose from: 'Brock Commons', 'Exchange', 'Fairview Crescent', 'Fraser Hall', 'Green College', 'Iona House', 'Marine Drive', 'Ponderosa Commons', 'St. John’s College', 'tə šxʷhəleləm̓s tə k̓ʷaƛ̓kʷəʔaʔɬ', 'Wesbrook Village', 'Kitsilano', 'Richmond', 'West Point Grey'): ")
    #try:
        #location = Location[location_input.replace(' ', '_').upper()]  # Map to Enum
    #except KeyError:
        #print(f"Invalid location '{location_input}'! Please try again.")
        #return

    descr = input("Description (optional): ") or None
    rooms = input("Number of rooms (optional): ")
    rooms = int(rooms) if rooms else None
    ppl = input("Number of people (optional): ")
    ppl = int(ppl) if ppl else None
    length = input("Lease length (optional, e.g., '6 months', '1 year'): ") or None
    laundry = input("Laundry available? (yes/no): ").lower() == 'yes' if input else None
    parking = input("Parking available? (yes/no): ").lower() == 'yes' if input else None
    gender = input("Gender preference (optional): ") or None
    
    floor_str = input("Floor (choose from: 'bottom', 'middle', 'top', or leave empty: ").strip().lower()
    floor = Floor[floor_str.upper()] if floor_str else None
    
    pets = input("Pets allowed? (yes/no): ").lower() == 'yes' if input else None

    # Create the new post data as UserData instance
    new_user_data = UserData(
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
    )

    # Append the new data to the CSV file
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=UserData._fields)
            # If file is empty, write the header
            if csvfile.tell() == 0:
                writer.writeheader()
            # Convert the UserData instance to a dictionary and write the new row
            writer.writerow(new_user_data._asdict())
        print("New post successfully added to the CSV file.")
    except Exception as e:
        print(f"An error occurred while appending to the CSV: {e}")

# Example usage of create_and_append_post_to_csv function
filename = 'nwhack25/user_data.csv'  # Ensure the correct path to the CSV file
create_and_append_post_to_csv(filename)
