# nocab Password Manager

## About
This project was started as way to practise and learn basic cryptography using Python as well as a way to learn how to use GitHub. This project currently (Version 0.0.2) uses Cryptography.Fernet Python Module. I intend to use PBKDF2 to add brute force protection as well as Customtkinter and tkinter to create a user friendly GUI to add ease of use and to learn those technologies too.

## How does it work?

It encrypts and decrypts user data so that it can only be read by the user of the program (hopefully). It currently uses 128bit Encryption with the future intentions of upgrading to a 256AES encryption. It creates 2 Files that can be stored sepearately to add a second external layer of security for your passwords or data. In the Future with the implementation of a GUI it will be easier to "browse" for these files.

## Basic Rundown of the main portions of the code

This code below is in charge of Creating a Salt key which will be used to create an 'irreversable' hash to add more security to your encryption.
```python
    def create_key(self, path): ## Creates a Salt Key that can be saved anywhere on computer or external drive. Required for Decryption of Passwords.
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
            
```

This code below is the logic used to take user inputs of Site, Username and Password, to be encrypted and appends the password file with the new data. You can see in encrypted_site for example that Fernet(self.key) uses the previously generated Salt Key to encrypt the user input and add it to the Password File.
```python
def add_password(self, site, username, password): ## Adds a password to your Password File
        self.password_dict[site] = {'username': username, 'password': password}

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted_site = Fernet(self.key).encrypt(site.encode())
                encrypted_username = Fernet(self.key).encrypt(username.encode())
                encrypted_password = Fernet(self.key).encrypt(password.encode())
                f.write(encrypted_site.decode() + ":" + encrypted_username.decode() + ":" + encrypted_password.decode() + "\n")
                
```
                
### The Challenge I still haven't Completed.

I had very 'ambitious' goals of encrypting site, username and password seperately and then re-encrypting them to hide the seperators in the password file. Whilst I am aware this is a useless feature it is something I wanted to do to challenge myself. I accomplished this goal however did not work out how to decrypt and read this data. I still intend on adding this in the future.

### Roadmap

- [x] Add Error Catching
- [x] Add Delete Password System
- [x] Add Show all Passwords System
- [] Add Login System
- [] Use Login Password along with salt to create Key
- [] Add a Modern GUI
- [] Use PBFDK2
- [] Maybe Host on Website
- [] 256AES Encryption
