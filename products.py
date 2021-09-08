#!/usr/bin/env python
######################################################################
# Working with classes -- test-code.py.py --
# C:\Users\Alleg\Python\UW Course\Week 8\test-code.py
# Assignment 8 - Working with classes
# DJP -- 2021-09-02 -- Designed initial missing code and menus
# DJP -- 2021-09-03 -- Created custom exceptions and added some error handling
# DJP -- 2021-09-04 -- Compelted methods in FileProcessor class
# DJP -- 2021-09-05 -- Initial code for IO class. Revised view records method.
# DJP -- 2021-09-06 -- Total overhaul on add records function.
# DJP -- 2021-09-07 -- Tidying up
######################################################################
import os
import pickle
import sys

import pandas   as pd

# Script variables
master_data = []

# Custom exceptions
class FileEXTError(Exception):
    """Raised when a file with an invalid extension is entered."""
    def __str__(self):
        return "File must end in '.dat'.\nPlease re-enter the file name."

class FileNotFoundError(Exception):
    """Raised when a file cannot be found"""
    def __str__(self):
        return "Specified file not found."

class ValueError(Exception):
    """Raised when an invalid value is entered at a menu or choice prompt."""
    def __str__(self):
        return "The value entered is invalid."

class NameError(Exception):
    """Raised when item name contains no letters."""
    def __str__(self):
        return "Product name must include letters."

class PricingError(Exception):
    """Raised when value entered in price field is invalid."""
    def __str__(self):
        return "Invalid price entered.\nMust be float."

class RemoveError(Exception):
    """Raised when an issue is encountered during record removal."""
    def __str__(self):
        return "That value is invalid. Either the ID doesn't exist or " \
                "an unacceptable format was entered."


# Introduce primary data class
class Product:
    """Stores product data.

    Properties:
        :id: (integer) ID number for a given record.
        :name: (string) Product name.
        :price: (float) Standard product price.
        :description: (string) Optional description of the item.

    Methods:
        -- None --
    """

    # Define object properties
    def __init__(self, id, name, price, description):
        self.id = id
        self.name = name
        self.price = price
        self.description = description


class FileProcessor:
    """Processes data to and from data files.

    Properties:
        -- None --

    Methods:
        :read_data(master): -> Returns a list of product data.
        :save_data(master): -> Saves a list of product data.
    """

    def read_data(master):
        """Reads and decodes data from '.dat' file before returning into main loop.

        Parameters:
            :master: (list) Current working list of products.

        Returns:
            :new_master: (list) Data loaded from file.
        """
        # If there are already objects in the list confirm overwrite
        if len(master) > 0:
            choice = input("This will overwrite the working records!\n" \
                            "Do you wish to continue? (Y)es / (N)o || ").lower()

            if choice not in ("y", "yes"):
                return master

        # Get target file from user and confirm type.
        filename = input("Please enter the name of the file " \
                            "you wish to open. || ")

        try:
            if not filename.endswith(".dat"):
                raise FileEXTError()
        except Exception as x:
            throw_error(x)
            return master

        # Check if the file already exists and create if not
        exists = os.path.isfile("./" + filename)

        try:
            if not exists:
                raise FileNotFound()
        except Exception as x:
            throw_error(x)
            return master

        # Open file, load into a new list, and return into main loop
        filehandle = open(filename, "rb")
        new_master = pickle.load(filehandle)

        print("\n=== Data Loaded! ===")

        return new_master


    def save_data(master):
        """Encodes data to binary and saves to '.dat' file.

        Parameters:
            :master: (list) Current working list of products.

        Returns:
            -- Nothing --
        """
        # Start a loop to obtain a destination file name and validate extension
        need_file = True
        while need_file:
            filename = input("Please enter the name of the destination file. || ")

            try:
                if not filename.endswith(".dat"):
                    raise FileEXTError()
            except Exception as x:
                throw_error(x)
                continue

            need_file = False

        # Check if the file already exists and display warning if it does
        exists = os.path.isfile("./" + filename)

        if exists == True:
            print("\nThis will overwrite any file with the same name.\n")
            confirm = input("Continue? (Y)es / (N)o || ").lower()
        else:
            confirm = "yes"

        try:
            if confirm not in ("y", "yes"):
                if confirm not in ("n", "no"):
                    raise ValueError()
                    return
                else:
                    return

            # Write data to the file
            else:
                fhandle = open(filename, "wb")
                pickle.dump(master, fhandle)
                fhandle.close()

                print("\n=== Data Saved! ===")

        except Exception as x:
            throw_error(x)
            return


class IO:
    """Handles data interaction with user.

    Properties:
      -- None --

    Methods:
        :main_menu: -> Displays top-level menu and returns user choice.
        :add_record(master): -> Adds record and returns list of Products.
        :remove_record(master): -> Deletes record and returns a list of products.
        :view_records(master): -> View list of product records. Returns nothing.
    """

    def main_menu():
        """Display top-level options menu to the user.

        Parameters:
          -- None --

        Returns:
          :user_choice: (integer) Menu selection.
        """
        choosing = True
        while choosing:
            print("""
        Main Menu:
        1. Add Record
        2. Remove Record
        3. View Records
        4. Load Data
        5. Save Data
        6. Exit Program
        """)

            # Get user input and ensure it's a number then return to the loop
            user_choice = input("Enter your selection. || ")
            print("\n")

            try:
                if int(user_choice) in range(1, 7):
                    return int(user_choice)
            except:
                continue

    def add_record(master):
        """Add record to working data list.

        Parameters:
        :master: (list) Contains all product objects currently in memory.

        Returns:
        :master: (list) Contains all product objects currently in memory.
        """
        # Start add item loop
        adding = True
        while adding:

            #Gather user input
            product = input("Product Name: || ").strip().title()
            price = input("Enter Price: || ").strip()
            description = input("Product Description: || ").strip()

            # Data validation
            try:
                # Must have a name
                if len(product) == 0:
                    raise NameError()
                # Product cannot be all numbers
                if product.isnumeric():
                    raise NameError()
                # Must have a price
                if len(price) == 0:
                    raise PricingError()
                # Ensure price is a float.
                try:
                    price = round(float(price), 2)
                except:
                    print("Fail")
                    raise PricingError()

            except Exception as x:
                throw_error(x)
                continue

            # If empty, verify description field was left blank intentionally
            if len(description) == 0:
                blank = True
                while blank:
                    go_on = input("Description is blank. " \
                                    "Continue? (Y)es / (N)o || ").lower()

                    if go_on not in ("y", "yes"):
                        if go_on not in ("n", "no"):
                            continue
                        elif go_on in ("n", "no"):
                            description = input("Product Description: || ").strip()
                            if len(description) != 0:
                                blank = False
                    else:
                        break

            # Set new product ID
            try:
                new_id = master[-1].id + 1
            except:
                new_id = 1

            # Create new product object and append to working list
            new_item = Product(new_id, product, price, description)
            master.append(new_item)

            #Check if user wants to add another item
            do_it_again = input("Would you like to add another item? (Y)es / (N)o || ").lower()

            if do_it_again in ("y", "yes"):
                continue
            else:
                break

        # Return list with new record(s) to the main loop
        return master

    def remove_record(master):
        """Removes record from working list of product objects.

        Parameters:
        :master: (list) Contains all product objects currently in memory.

        Returns:
        :master: (list) Contains all product objects currently in memory.
        """

        # Get and validate user input
        to_remove = input("Enter the ID of the record you would like to remove. || ")

        try:
            try:
                to_remove = int(to_remove)
            except:
                raise RemoveError()
        except Exception as x:
            throw_error(x)
            return

        # Check to see if the entered ID exists
        try:
            try:
                current = master[to_remove - 1]
                print(current)
            except:
                raise RemoveError()
        except Exception as x:
            throw_error(x)
            return

        # Locate record in current list
        for i in master:
            if i.id == to_remove:
                name = i.name

        # Confirm and process removal
        confirm = input(f"Are you sure you wish to remove the record for - {name}? || ").lower()

        if confirm in ("y", "yes"):
            del master[to_remove - 1]
            return master
        else:
            return

    def view_records(master):
        """Present "pretty" list of all product records.

        Parameters:
        :master: (list) Contains all product objects currently in memory.

        Returns:
          -- Nothing --
        """
        # Load records into a list of dicts
        view_list = []

        if len(master) == 0:
            print("There are no records to display")
        else:
            for i in master:
                record = {
                        "ID" : i.id,
                        "Name" : i.name,
                        "Price" : i.price,
                        "Description" : i.description
                        }
                view_list.append(record)

            # "Pretty print" with pandas module
            df = pd.DataFrame(view_list)
            print(df.to_string(index=False))

def throw_error(error):
    """Error handling message.

    Parameters:
    :error: Exception object

    Returns:
    --Nothing--
    """

    # Print a pretty error
    print("\n========================================")
    print("There was an error! Oopsie!")
    print("----------------------------------------")
    print(error)
    print("========================================\n")


# Main operation loop
running = True
while running:

    #Start with the menu
    option = IO.main_menu()

    # Event handling (methods are self-descriptive)
    if option == 1:
        IO.add_record(master_data)
    elif option == 2:
        IO.remove_record(master_data)
    elif option == 3:
        IO.view_records(master_data)
    elif option == 4:
        master_data = FileProcessor.read_data(master_data)
    elif option == 5:
        FileProcessor.save_data(master_data)
    elif option == 6:
        exit = input("Would you like to exit? " \
                    "All unsaved progress will be lost! (Y)es / (N)o || ")

        if exit in ("y", "yes"):
            sys.exit()
        else:
            continue
######################################################################
#if __name__ == "__main__":
    #demo_data()

# test-code.py
