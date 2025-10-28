from db_connection import db_connection
import mysql.connector
from mysql.connector import Error

def customer_dashboard(user_id, username):
    while True:
        print(f"\n🎯 Welcome {username}!")
        print("="*40)
        print("      🏦 CUSTOMER DASHBOARD")
        print("="*40)
        print("1. 💰 Withdrawal")
        print("2. 💳 Deposit")
        print("3. 📊 View Balance")
        print("4. 📝 Services Request")
        print("5. 🚪 Logout")
        print("-"*40)
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            withdrawal(user_id)
        elif choice == '2':
            deposit(user_id)
        elif choice == '3':
            check_balance(user_id)
        elif choice == '4':
            request_service(user_id)
        elif choice == '5':
            print("👋 Logging out... Thank you for banking with HDFC!")
            break
        else:
            print("❌ Invalid option! Please try again.")

def withdrawal(user_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT account_balance FROM accounts WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        
        if not result:
            print("❌ No account found!")
            return
            
        current_balance = result[0]
        print(f"💰 Current Balance: ₹{current_balance}")
        
        amt = float(input("Enter amount to withdraw: ₹"))
        
        if amt <= 0:
            print("❌ Amount must be positive!")
            return
            
        if amt > current_balance:
            print("❌ Insufficient balance!")
            return
        
        cursor.execute(
            "UPDATE accounts SET account_balance = account_balance - %s WHERE user_id = %s",
            (amt, user_id)
        )
        conn.commit()
        
        cursor.execute("SELECT account_balance FROM accounts WHERE user_id = %s", (user_id,))
        new_balance = cursor.fetchone()[0]
        
        print(f"\n✅ Withdrawal successful!")
        print(f"💰 Withdrawn: ₹{amt}")
        print(f"💳 New Balance: ₹{new_balance}")
        
    except ValueError:
        print("❌ Please enter a valid amount!")
    except Error as e:
        print(f"❌ Withdrawal failed: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def deposit(user_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT account_balance FROM accounts WHERE user_id = %s", (user_id,))
        current_balance = cursor.fetchone()[0]
        print(f"💰 Current Balance: ₹{current_balance}")
        
        amt = float(input("Enter amount to deposit: ₹"))
        
        if amt <= 0:
            print("❌ Amount must be positive!")
            return
        
        cursor.execute(
            "UPDATE accounts SET account_balance = account_balance + %s WHERE user_id = %s",
            (amt, user_id)
        )
        conn.commit()
        
        cursor.execute("SELECT account_balance FROM accounts WHERE user_id = %s", (user_id,))
        new_balance = cursor.fetchone()[0]
        
        print(f"\n✅ Deposit successful!")
        print(f"💰 Deposited: ₹{amt}")
        print(f"💳 New Balance: ₹{new_balance}")
        
    except ValueError:
        print("❌ Please enter a valid amount!")
    except Error as e:
        print(f"❌ Deposit failed: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def check_balance(user_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT account_balance, account_type FROM accounts WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        
        if result:
            balance, acc_type = result
            print(f"\n" + "="*30)
            print("     📊 ACCOUNT SUMMARY")
            print("="*30)
            print(f"👤 User ID: {user_id}")
            print(f"🏦 Account Type: {acc_type}")
            print(f"💰 Current Balance: ₹{balance}")
            print("="*30)
        else:
            print("❌ No account found!")
            
    except Error as e:
        print(f"❌ Error checking balance: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def request_service(user_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        
        print("\n" + "="*35)
        print("     📝 SERVICE REQUEST")
        print("="*35)
        print("1. 🏠 Loan Application")
        print("2. 💳 ATM Card Request")
        print("3. 📋 Cheque Book Request")
        print("4. 🗑️  Delete Account Request")
        print("5. ↩️ Back to Menu")
        print("-"*35)
        
        choice = input("Choose service (1-5): ")
        
        # Use EXACT ENUM values from database
        if choice == '1':
            # Loan request
            amt = float(input("Enter loan amount: ₹"))
            cursor.execute(
                "INSERT INTO requests (user_id, req_type, req_amount) VALUES (%s, 'Loan', %s)",
                (user_id, amt)
            )
            print(f"✅ Loan application submitted for ₹{amt}")
            
        elif choice == '2':
            # ATM Card request - using EXACT ENUM value
            cursor.execute(
                "INSERT INTO requests (user_id, req_type) VALUES (%s, 'ATM Card')",  # Note: Space in 'ATM Card'
                (user_id,)
            )
            print("✅ ATM Card request submitted")
            
        elif choice == '3':
            # Cheque Book request - using EXACT ENUM value
            cursor.execute(
                "INSERT INTO requests (user_id, req_type) VALUES (%s, 'Cheque Book')",  # Note: Space in 'Cheque Book'
                (user_id,)
            )
            print("✅ Cheque Book request submitted")
            
        elif choice == '4':
            # Delete Account request - using EXACT ENUM value
            confirm = input("⚠️  Are you sure you want to request account deletion? (yes/no): ").lower()
            if confirm == 'yes':
                cursor.execute(
                    "INSERT INTO requests (user_id, req_type) VALUES (%s, 'Delete Account')",  # Note: Space in 'Delete Account'
                    (user_id,)
                )
                print("✅ Account deletion request submitted. Admin will process your request.")
            else:
                print("❕ Account deletion request cancelled.")
                return
                
        elif choice == '5':
            return
        else:
            print("❌ Invalid choice!")
            return
        
        conn.commit()
        print("📝 Your request has been submitted for admin approval!")
        
    except ValueError:
        print("❌ Please enter a valid amount!")
    except Error as e:
        print(f"❌ Request failed: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()