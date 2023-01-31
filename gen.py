import secrets
import string
import csv
from pyboxen import boxen
import pyperclip


def generate_password(length: int = 20, chars: bool = True, nums: bool = True, puncs: bool = True):
    password_combination = ""

    if chars:
        password_combination += string.ascii_letters

    if nums:
        password_combination += string.digits

    if puncs:
        password_combination += string.punctuation

    combination_length = len(password_combination)
    new_password = ""

    for i in range(length):
        new_password += password_combination[secrets.randbelow(combination_length)]

    return new_password

def output_password(name, username, password):
    print(boxen(
                password,
                "",
                "1: Copy to clipboard",
                "2: Save password to .csv",
                "0: Exit",
                title="Generated password below:",
                subtitle="Select an option",
                subtitle_alignment="center",
                padding=1,
                margin=1,
                color="cyan"
                )
            )
    option = input("Input here: ")
    if option == "1":
        pyperclip.copy(password)
    elif option == "2":
        data = [name, username, password]
        file = open('login_storage.csv', 'a', newline='')
        writer = csv.writer(file)
        writer.writerow(data)
        file.close()
        return main_menu()
    elif option == "0":
        exit()

def settings():
    print(boxen(
                "1: Default settings",
                "2: Advanced settings",
                "3: Return to main menu",
                "0: Exit",
                title="Settings",
                subtitle="Select an option",
                subtitle_alignment="center",
                padding=1,
                margin=1,
                color="cyan"    
                )
            )   
    option2 = input("Input here: ")
    if option2 == "1":
        return generate_password()
    elif option2 == "2":
        length, chars, nums, puncs = adv_settings()
        return generate_password(length, chars, nums, puncs)
    elif option2 == "3":
        print("Return to main menu...")
        return main_menu()
    elif option2 == "0":
        exit()
        
def adv_settings():
    print(
        boxen(
            "How would you like to customize",
            "your password?",
            "",
            "       Current settings:",
            "",
            "Password length: 20",
            "Characters: Yes",
            "Numbers: Yes",
            "Symbols: Yes",
            title="Advanced settings",
            subtitle="Input below",
            subtitle_alignment="center",
            padding=1,
            margin=1,
            color="cyan"
            )
    )
    length = int(input("Password length: "))
    
    chars = input("Characters (Y/N): ")
    if chars == "Y":
        chars = True
    else:
        chars = False
        
    nums = input("Numbers (Y/N): ")
    if nums == "Y":
        nums = True
    else:
        nums = False
        
    puncs = input("Symbols (Y/N): ")
    if puncs == "Y":
        puncs = True
    else:
        puncs = False
    
    return length, chars, nums, puncs

def main_menu():
    print(
        boxen(
            "1: Generate password",
            "2: Add login",
            "0: Exit",
            title="Welcome to Simple Password Generator!",
            subtitle="Select an option",
            subtitle_alignment="center",
            padding=1,
            margin=1,
            color="cyan"
            )
    )

    option = input("Input here: ")

    if option == "1":
        name = ''
        username = ''
        password = settings()
        output_password(name, username, password)

    elif option == "2":
        print(
        boxen(
            "What would you like to name your login and username?",
            title="Add login",
            subtitle="Input below",
            subtitle_alignment="center",
            padding=1,
            margin=1,
            color="cyan"
            )
    )
        name = input("Name: ")
        username = input("Username: ")
        password = settings()
        output_password(name, username, password)
        
    elif option == "0":
        exit()

main_menu()