## This project is still very much WIP, I intend of implementing lots of features to ensure it is user friendly and seamless.
## Whilst this project is predominantly used for my learning. If this is of use to some people have my notes

from cryptography.fernet import Fernet ## Used to make Salt Key
from Crypto.Protocol.KDF import PBKDF2 ## Brute Force Protection (Not Used Yet)
import os ## Used to Clear Console
import time ## Used to tidy up the Quit Command
import customtkinter as ctk ## Used for GUI (Not Used Yet)
import tkinter ## Used for GUI (Not Used Yet)

class password_manager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

### Salt Key Creation and Retrieval System.
## As long as you know the path of the Salt key it can be stored and accessed from anywhere in your system. (Or that is what is intended)

    def create_key(self, path): ## Creates a Salt Key that can be saved anywhere on computer or external drive. Required for Decryption of Passwords.
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path): ## Loads your Salt Key from anywhere on your computer.
        try:
            with open(path, 'rb') as f:
                self.key = f.read()
        except FileNotFoundError:
            return


### Password File Creation and Retrieval System.
## As long as you know the path of the password file this file can be stored and accessed from anywhere in the computer. (Or that is what is intended)

    def create_password_file(self, path, initial_values=None): ## Creates a Password File that will store all of the encrypted data/passwords.
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path): ## Loads your Password File containing all your encrypted data/passwords.
        self.password_file = path

        try:
            with open(path, 'r') as f:
                for line in f:
                    encrypted_site, encrypted_username, encrypted_password = line.split(":")
                    site = Fernet(self.key).decrypt(encrypted_site.encode()).decode()
                    username = Fernet(self.key).decrypt(encrypted_username.encode()).decode()
                    password = Fernet(self.key).decrypt(encrypted_password.encode()).decode()
                    self.password_dict[site] = {'username': username, 'password': password}
        except FileNotFoundError:
            return
        
    def save_password_file(self): ## Saves your Password File. Required for the Delete Password Function.
        with open(self.password_file, 'w') as f:
            for site, credentials in self.password_dict.items():
                encrypted_site = Fernet(self.key).encrypt(site.encode()).decode()
                encrypted_username = Fernet(self.key).encrypt(credentials['username'].encode()).decode()
                encrypted_password = Fernet(self.key).encrypt(credentials['password'].encode()).decode()
                f.write(f"{encrypted_site}:{encrypted_username}:{encrypted_password}\n")


### Password Creation and Retrieval System.
## I have not figured out how to add PBFDK2 Module to the logic to add protection to Dictionary Attacks and Rainbow Tables.

    def add_password(self, site, username, password): ## Adds a password to your Password File
        self.password_dict[site] = {'username': username, 'password': password}

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted_site = Fernet(self.key).encrypt(site.encode())
                encrypted_username = Fernet(self.key).encrypt(username.encode())
                encrypted_password = Fernet(self.key).encrypt(password.encode())
                f.write(encrypted_site.decode() + ":" + encrypted_username.decode() + ":" + encrypted_password.decode() + "\n")

    def get_password(self, site):
        try:
            return self.password_dict[site]
        except KeyError:
            print(f"{site} not found in password file.")
            return None
    
    def delete_password(self, site): ## Logic Used to delete a password in your Password File.
        if site in self.password_dict:
            del self.password_dict[site]
            self.save_password_file()

    def all_passwords(self):
        for site, credentials in self.password_dict.items():
            print(f"Site: {site}")
            print(f"Username: {credentials['username']}")
            print(f"Password: {credentials['password']}")
            print(f"----------------------------------------")
    
    

def main(): ## Main Program/ Password Manager.
    password = {
        "Example" : "12345678",
    }

    pm = password_manager()
    manager     = False
    key_loaded  = False
    file_loaded = False

## Non Compiled Password Manager
    while manager is not True:
        
        print ("Welcome to nocab's Password Manager! What Do you want to do?")
        while key_loaded is not True: ## Salt Key Load or Create
            print ("""
            1. Create and new Key
            2. Load a Key
            q. Quit
            """)
            choice = input ("Enter a Value: ")

            if choice == "1":
                path = input("Enter a Path and Name for your New Key: ")
                pm.create_key(path)
                os.system("cls")
                print ("Key Loaded!")
                key_loaded = True
                break

            elif choice == "2":
                path = input("Enter the Path and Name of your Key: ")
                pm.load_key(path)
                os.system("cls")
                if pm.key is not None:
                    print ("Key Loaded!")
                    key_loaded = True
                    break
                elif pm.key is None:
                    os.system("cls")
                    print(f"File not found: {path}. Please try again.")
                    continue
     
            elif choice == "q" or "Q":
                print ("Quitting. Goodbye!")
                time.sleep(3)
                os.system("cls")
                manager = True
                break

            else:
                print ("Invalid Selection!")
                os.system("cls")
                continue
                

        while file_loaded is not True and key_loaded is True: ## Password file Creation or Loading
            print ("""
            1. Create new Password File
            2. Load a Password File
            q. Quit
            """)
            choice = input ("Enter a Value: ")

            if choice == "1":
                path = input("Enter a Path and name for your New Password File: ")
                pm.create_password_file(path)
                os.system("cls")
                print ("Password File Chosen!")
                file_loaded = True
                break

            elif choice == "2":
                path = input("Enter the Path and Name of your Key: ")
                pm.load_key(path)
                os.system("cls")
                if pm.password_file is not None:
                    print ("Password File Chosen!")
                    file_loaded = True
                    break
                elif pm.password_file is None:
                    os.system("cls")
                    print(f"File not found: {path}. Please try again.")
                    continue
     
            elif choice == "q" or "Q":
                print ("Quitting. Goodbye!")
                time.sleep(3)
                manager = True
                os.system("cls")
                break  

            else:
                print ("Invalid Selection!")
                os.system("cls")
                continue

        while key_loaded and file_loaded is True:
            print ("""
            1. Add a New Password
            2. Find a Password
            3. Delete a Password
            4. Load a New Key
            5. Load a New Password File
            q. Quit
            """)
            choice = input ("Enter a Value: ")

            if choice == "1":
                site = input("Enter the Website: ")
                username = input("Enter your Username")
                password = input("Enter the Password: ")
                pm.add_password(site, username , password)
                break

            elif choice == "2":
                site = input("What site are you looking for? (Use * to Display All): ")
                if site == "*":
                    pm.all_passwords()
                else:    
                    print(f"Password for {site} is {pm.get_password(site)}")
                    break

            elif choice == "3":
                site = input("What site do you want to Delete?: ")
                pm.delete_password(site)

            elif choice == "4":
                print ("Unloading Key")
                time.sleep(0.5)
                os.system("cls")
                key_loaded = False
                break

            elif choice == "5":
                print ("Unloading Password File")
                time.sleep(0.5)
                os.system("cls")
                file_loaded = False
                break

            elif choice == "q" or "Q":
                print ("Quitting. Goodbye!")
                time.sleep(3)
                manager = True
                os.system("cls")
                break  

            else:
                print ("Invalid Selection!")
                continue



if __name__ == "__main__":
    main()
