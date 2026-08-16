import getpass

account = {
    "user": "Guilherme",
    "password": "Gui171609"
}

number_attempts = 3

print("\n===== SYSTEM ACCOUNT ====\n")
print("[1] Login")
print("[2] Exit")
opc = int(input("Which one do you want? R: "))

if opc == 1:

    while number_attempts < 4:
        user = input("Enter your username: ").strip()
        password = getpass.getpass("Enter your password: ").strip()

        if user == account["user"] and password == account["password"]:
            print(f"Welcome {account['user']}!")

            analyze_data = input("Analyze my data [Y/n]: ").strip().upper()

            if analyze_data == "Y":
                password = getpass.getpass("Enter your password: ").strip()

                if password == account["password"]:
                    print("My data:")
                    print(f"User: {account['user']}")
                    print(f"Password: {account['password']}")
                    break

                else:
                    print("Error! Your password are incorrect")

            else:
                print(f"Welcome {account['user']}!")
                break

        else:
            print("Error! Your email or password are incorrect")
            print(f"Your have {number_attempts} attempts")
            number_attempts -= 1

            if number_attempts == -1:
                break

elif opc == 2:
    print("Bye!")
    exit()