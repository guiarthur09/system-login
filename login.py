from email_validator import validate_email, EmailNotValidError
from datetime import datetime
import sqlite3
import bcrypt
import getpass

connection = sqlite3.connect("database/data.db")
cursor = connection.cursor()

#[Date Created]
now = datetime.now()
readable_string = now.strftime("%Y-%m-%d %H:%M")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TEXT NOT NULL,
    status_account TEXT DEFAULT 'active' CHECK(status_account IN ('active', 'inactive'))
);
""")

connection.commit()

def sing_up():
    try:
        print("\n===== SIGN UP =====\n")
        username = input("Type your Username: ").strip()
        email = input("Type your Email: ").strip()

        # [Verify Validated Email]
        try:
            validado = validate_email(email)
            email = validado.normalized
        except EmailNotValidError as e:
            print(f"Invalid Email: {e}")
            return 
        
        password = getpass.getpass("Type your Password: ").strip()

        # [Password Encrypted]
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("""
        INSERT INTO users
        (username, email, password, created_at)
        VALUES (?, ?, ?, ?)""", (username, email, password_hash, readable_string))

        connection.commit()
        print("User registered successfully!")
        
    except Exception as e:
        print(f"Error! {e}")
        
    finally:
        cursor.close()

while True:
    print("\n===== SYSTEM LOGIN ====\n")
    print("[1] Sign up")
    print("[2] Login")
    print("[3] Exit")
    opc = int(input("\nWhich one do you want? R: \n"))

    if opc == 1:
        sing_up()
    #if opc = 2:
        #login() -> Still to be done
    elif opc == 3:
        print("Bye")
        break
    else:
        print("Invalid Option! Try again")