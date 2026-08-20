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
    email TEXT UNIQUE NOT NULL,
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

    except sqlite3.IntegrityError:
        print("Error: This email is already registered!")
        
    except Exception as e:
        print(f"Error! {e}")
        

def login():
    try:
        print("\n===== LOGIN =====\n")
        email = input("Type your Email: ").strip()

        try:
            validado = validate_email(email)
            email = validado.normalized
        except EmailNotValidError as e:
            print(f"Invalid Email: {e}")
            return 
        
        password = getpass.getpass("Type your Password: ").strip()

        cursor.execute("""SELECT email, password 
                          FROM users
                          WHERE email = ?""", (email,))
        user = cursor.fetchone()

        if user:
            # Pegamos a senha guardada (ela vem do banco como string ou bytes)
            encrypted_password = user[1]
            
            # CORREÇÃO: Garantimos que o hash do banco esteja em formato de bytes
            if isinstance(encrypted_password, str):
                encrypted_password = encrypted_password.encode('utf-8')

            # CORREÇÃO: Trocamos o 'bcrypt.gensalt()' por 'encrypted_password'
            if bcrypt.checkpw(password.encode("utf-8"), encrypted_password):
                print("Login successful!")
            else:
                print("Incorrect password! Try again")

        else:
            print("Email not found!")

    except Exception as e:
        print(f"Error! {e}")

while True:
    print("\n===== SYSTEM LOGIN ====\n")
    print("[1] Sign up")
    print("[2] Login")
    print("[3] Exit")

    try:
        opc = int(input("\nWhich one do you want? R: \n"))
    except ValueError:
        print("Please type a number!")
        continue

    if opc == 1:
        sing_up()
    elif opc == 2:
        login()
    elif opc == 3:
        print("Bye")
        cursor.close()
        connection.close()
        break
    else:
        print("Invalid Option! Try again")