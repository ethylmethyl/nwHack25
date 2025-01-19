import os
import csv
from typing import NamedTuple
from typing import Optional
from enum import Enum

# Enum for floor preference
class Floor(Enum):
    BOTTOM = "bottom"
    MIDDLE = "middle"
    TOP = "top"

# Data structure to hold user data
class UserData(NamedTuple):
    cst: int  # Cost (required integer)
    location: bool  # Location (True is on Campus False, off)
    descr: Optional[str]  # Description (optional string)
    rooms: Optional[int]  # Number of rooms (optional integer)
    ppl: Optional[int]  # Number of people (optional integer)
    length: Optional[str]  # Lease length (optional string)
    laundry: Optional[bool]  # Laundry available (optional boolean)
    parking: Optional[bool]  # Parking available (optional boolean)
    gender: Optional[str]  # Gender preference (optional string)
    floor: Optional[str]  # Preferred floor (optional enum)
    pets: Optional[bool]  # Pets allowed (optional boolean)

def get_integer_input(prompt, min_value=None, max_value=None):
    """
    Prompts the user for integer input and ensures valid input within the given range.

    Args:
        prompt: The message to display to the user.
        min_value: Minimum allowed value (optional).
        max_value: Maximum allowed value (optional).

    Returns:
        The integer entered by the user, or None if the input is empty or interrupted.
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:  # Handle empty input for optional fields
                return None
            value = int(user_input)
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"Invalid input. Please enter an integer between {min_value} and {max_value}.")
            else:
                return value
        except KeyboardInterrupt:
            print("Input cancelled.")
            return None  # Indicate cancellation with None
        except ValueError:
            print("Invalid input. Please enter an integer.")


def get_yes_no_input(prompt):
    """
    Prompts the user for a yes/no answer and ensures valid input.

    Args:
        prompt: The message to display to the user.

    Returns:
        True for "yes", False for "no", or None if the input is empty.
    """
    while True:
        user_input = input(prompt).strip().lower()
        if not user_input:  # Handle empty input for optional fields
            return None
        if user_input == "yes":
            return True
        elif user_input == "no":
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def get_valid_floor_input(prompt):
    """
    Prompts the user for floor preference and ensures it's valid.

    Args:
        prompt: The message to display to the user.

    Returns:
        The chosen floor as a string, or None if the input is empty or invalid.
    """
    valid_floors = ["bottom", "middle", "top"] 
    while True:
        user_input = input(prompt).strip().lower()
        if not user_input:  # Handle empty input
            return None
        if user_input in valid_floors:
            return user_input
        else:
            print(f"Invalid floor preference. Please choose from: {', '.join(valid_floors)} or leave empty.")

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
    cst = get_integer_input("Cost (per/month in dollars): ")

    location = get_yes_no_input("On Campus? (yes/no): ")
    rooms = get_integer_input("Number of rooms (optional): ", 1, 100) 
    ppl = get_integer_input("Number of tenants (optional): ", 1, 100) 

    length = input("Lease length (optional, e.g., '6 months', '1 year'): ") or None
    laundry = get_yes_no_input("Laundry in unit available? (yes/no): ")
    parking = get_yes_no_input("Parking available? (yes/no): ")
    gender = input("Gender preference (optional): ") or None

    floor_str = get_valid_floor_input("Floor (choose from: 'bottom', 'middle', 'top', or leave empty: ") 
    floor = floor_str

    pets = get_yes_no_input("Pets allowed? (yes/no): ")

    descr = input("Description (optional): ")  # Get user input for the description

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
