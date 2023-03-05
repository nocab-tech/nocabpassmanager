## This project is still very much WIP, I intend of implementing lots of features to ensure it is user friendly and seamless.
## Whilst this project is predominantly used for my learning. If this is of use to some people have my notes

from cryptography.fernet import Fernet ## Used to make Salt Key
from Crypto.Random import get_random_bytes ## Random Bytes
from Crypto.Protocol.KDF import PBKDF2 ## Brute Force Protection
from Crypto.Cipher import AES ## AES
from Crypto.Util.Padding import pad, unpad ## Padding of Data
import os ## Used to Clear Console
import time ## Used to tidy up the Quit Command
import customtkinter as ctk
from tkinter import filedialog


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

    def load_key(self, path): ## Loads a previously Created Salt Key.
        with open(path, 'r') as f:
            self.key = f.read()

    ### Password File Creation and Retrieval System.
    ## As long as you know the path of the password file this file can be stored and accessed from anywhere in the computer. (Or that is what is intended)

    def create_password_file(self, path, initial_values=None): ## Creates a Password File that will store all of the encrypted data/passwords.
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path): ## Loads a previously Created Password File.
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                encrypted_line = Fernet(self.key).decrypt(line.encode()).decode()
                site, username, password = encrypted_line.split(":")
                self.password_dict[site] = {'username': Fernet(self.key).decrypt(username.encode()).decode(), 'password': Fernet(self.key).decrypt(password.encode()).decode()}

    ### Password Creation and Retrieval System.

    def add_password(self, site, username, password): ## Logic used to add passwords to your Password File.
        self.password_dict[site] = {'username': username, 'password': password}

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt((site + ":" + username + ":" + password).encode())
                f.write(encrypted.decode() + "\n")

    def get_password(self, site): ## Logic Used to get a password in your Password File.
        return self.password_dict[site]
        

def main(): ## Main Program/ Password Manager.
    password = {
        "Example" : "12345678",
    }

    pm = password_manager()
    manager     = False
    key_loaded  = False
    file_loaded = False

    while manager is not True:

        while key_loaded is not True:
            print ("""Welcome to nocab's Password Manager! What Do you want to do?
            1. Create and new Key
            2. Load a Key
            q. Quit
            """)
            choice = input ("Enter a Value: ")

            if choice == "1":
                path = input("Enter a Path and Name for your New Key: ")
                pm.create_key(path)
                os.system("cls")
                key_loaded = True
                break

            elif choice == "2":
                path = input("Enter the Path and Name of your Key: ")
                pm.load_key(path)
                os.system("cls")
                key_loaded = True
                break
     
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
                

        while file_loaded is not True and key_loaded is True:
            print ("""Key Loaded!
            1. Create new Password File
            2. Load a Password File
            q. Quit
            """)
            choice = input ("Enter a Value: ")

            if choice == "1":
                path = input("Enter a Path and name for your New Password File: ")
                pm.create_password_file(path)
                os.system("cls")
                file_loaded = True
                break

            elif choice == "2":
                path = input("Enter the Path and name of your Key: ")
                pm.load_password_file(path)
                os.system("cls")
                file_loaded = True
                break
     
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
            print ("""Password File Chosen!
            1. Add a New Password
            2. Find a Password
            3. Load a New Key
            4. Load a New Password File
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
                site = input("What site are you looking for?: ")
                print(f"Password for {site} is {pm.get_password(site)}")
                break

            elif choice == "3":
                print ("Unloading Key")
                os.system("cls")
                key_loaded = False
                break

            elif choice == "4":
                print ("Unloading Password File")
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
