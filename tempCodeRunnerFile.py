from db_connection import db_connection
import mysql.connector
from mysql.connector import Error

def signup():
    try:
        conn = db_connection()
        if not conn:
            return None
            
        cursor = conn.cursor()
        
        print("\n=== USER REGISTRATION ===")
        user_name = input("Enter your name: ").strip()
        
        cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name,))
        if cursor.fetchone():
            print("❌ Username already exists!")
            return None
        
        user_password = input("Enter your password: ")
        user_role = "customer"
        
        cursor.execute(
            "INSERT INTO users (user_name, user_password, user_role) VALUES (%s, %s, %s)",
            (user_name, user_password, user_role)
        )
        conn.commit()
        
        user_id = cursor.lastrowid
        
        print("\n=== ACCOUNT CREATION ===")
        print("1. Savings Account")
        print("2. Current Account")
        acc_choice = input("Choose account type (1/2): ")
        
        account_type = "savings" if acc_choice == "1" else "current"
        initial_balance = 1000.00
        
        cursor.execute(
            "INSERT INTO accounts (user_id, account_type, account_balance) VALUES (%s, %s, %s)",
            (user_id, account_type, initial_balance)
        )
        conn.commit()
        
        print(f"✅ Registration successful! Welcome {user_name}")
        print(f"✅ Account created with initial balance: ₹{initial_balance}")
        
        return user_id
        
    except Error as e:
        print(f"❌ Registration failed: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def login():
    try:
        conn = db_connection()
        if not conn:
            return None, None, None
            
        cursor = conn.cursor()
        
        print("\n=== USER LOGIN ===")
        user_name = input("Enter your name: ").strip()
        user_password = input("Enter your password: ")
        
        cursor.execute(
            "SELECT user_id, user_name, user_role FROM users WHERE user_name = %s AND user_password = %s",
            (user_name, user_password)
        )
        user_data = cursor.fetchone()
        
        if user_data:
            user_id, username, user_role = user_data
            print(f"✅ Login successful! Welcome {username}")
            return user_id, username, user_role
        else:
            print("❌ Invalid username or password!")
            return None, None, None
            
    except Error as e:
        print(f"❌ Login failed: {e}")
        return None, None, None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()