import secrets
import string
import csv
from pyboxen import boxen
import pyperclip
import zmq
from prettytable import from_csv
import pandas as pd
import webbrowser
import validators


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


def password_strength(password):
    context = zmq.Context()

    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    socket.send_string(password)

    message = socket.recv()

    return message.decode()


def output_password(name, url, username, password):
    print(boxen(
        password,
        "",
        "1: Copy to clipboard",
        "2: Save password to .csv",
        "3: Check password strength",
        "4: Return to main menu",
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
        output_password(name, url, username, password)
    elif option == "2":
        df = pd.read_csv('login_storage.csv')
        row_number = len(df.index) + 1
        data = [row_number, name, url, username, password]
        file = open('login_storage.csv', 'a', newline='')
        writer = csv.writer(file)
        writer.writerow(data)
        file.close()
        output_password(name, url, username, password)
    elif option == "3":
        password_score = password_strength(password)
        print(password_score)
        output_password(name, url, username, password)
    elif option == "4":
        main_menu()
    elif option == "0":
        print(boxen(
            "Are you sure you want to exit? (Y/N)",
            title="Exit",
            subtitle="Input below",
            subtitle_alignment="center",
            padding=1,
            margin=1,
            color="cyan"
        )
        )
        answer = input("Input here: ")
        if answer == "Y":
            exit()
        elif answer == "N":
            output_password(name, url, username, password)


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
        main_menu()
    elif option2 == "0":
        print(boxen(
            "Are you sure you want to exit? (Y/N)",
            title="Exit",
            subtitle="Input below",
            subtitle_alignment="center",
            padding=1,
            margin=1,
            color="cyan"
        )
        )
        answer = input("Input here: ")
        if answer == "Y":
            exit()
        elif answer == "N":
            settings()


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
    while True:
        length = int(input("Password length: "))
        if length < 0:
            print("Length cannot be less than 0, please try again.")
            continue
        else:
            break

    while True:
        chars = input("Characters (Y/N): ")
        if chars == "Y":
            chars = True
            break
        elif chars == "N":
            chars = False
            break
        else:
            print("Invalid response, please try again.")
            continue

    while True:
        nums = input("Numbers (Y/N): ")
        if nums == "Y":
            nums = True
            break
        elif nums == "N":
            nums = False
            break
        else:
            print("Invalid response, please try again.")
            continue

    while True:
        puncs = input("Symbols (Y/N): ")
        if puncs == "Y":
            puncs = True
            break
        elif puncs == "N":
            puncs = False
            break
        else:
            print("Invalid response, please try again.")
            continue

    return length, chars, nums, puncs


def displayCSV():
    with open('login_storage.csv', "r") as fp:
        x = from_csv(fp)
    print(x)
    print(
        boxen(
            "1: Open URL to specific login (Copy password to clipboard)",
            "2: Return to main menu",
            "0: Exit",
            subtitle="Select an option",
            subtitle_alignment="center",
            padding=1,
            margin=1,
            color="cyan"
        )
    )
    option = input("Input here: ")
    if option == "1":
        row = input("Row number: ")
        openURL(row)
    elif option == "2":
        main_menu()
    elif option == "0":
        exit()


def openURL(number):
    num = number
    with open('login_storage.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            x = row[0]
            y = row[2]
            z = row[4]
            if x == num:
                if y == '':
                    print("No URL to open.")
                    exit()
                if not (validators.url(y)):
                    print("URL is not valid")
                pyperclip.copy(z)
                webbrowser.open(y)


def main_menu():
    print(
        boxen(
            "1: Generate password",
            "2: Add login",
            "3: View password vault",
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
        url = ''
        username = ''
        password = settings()
        output_password(name, url, username, password)

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
        url = input("URL: ")
        username = input("Username: ")
        password = settings()
        output_password(name, url, username, password)

    elif option == "3":
        displayCSV()

    elif option == "0":
        exit()


main_menu()
