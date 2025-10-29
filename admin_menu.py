from db_connection import db_connection
import mysql.connector
from mysql.connector import Error

def admin_dashboard():
    while True:
        print("\n=== ADMIN DASHBOARD ===")
        print("1. View All Users")
        print("2. View All Accounts")
        print("3. Manage Service Requests")
        print("4. Logout")
        
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            view_all_users()
        elif choice == '2':
            view_all_accounts()
        elif choice == '3':
            manage_requests()
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid option!")

def view_all_users():
    try:
        conn = db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id, user_name, user_role, created_at FROM users")
        users = cursor.fetchall()
        
        print("\n=== ALL REGISTERED USERS ===")
        print(f"{'ID':<5} {'Name':<15} {'Role':<10} {'Created At'}")
        print("-" * 50)
        for user in users:
            print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10} {user[3]}")
        print(f"Total Users: {len(users)}")
        
    except Error as e:
        print(f" Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def view_all_accounts():
    try:
        conn = db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT a.account_id, u.user_name, a.account_type, a.account_balance, a.created_at 
            FROM accounts a 
            JOIN users u ON a.user_id = u.user_id
        """)
        accounts = cursor.fetchall()
        
        print("\n=== ALL BANK ACCOUNTS ===")
        print(f"{'Acc ID':<8} {'User':<15} {'Type':<10} {'Balance':<12} {'Created At'}")
        print("-" * 60)
        for acc in accounts:
            print(f"{acc[0]:<8} {acc[1]:<15} {acc[2]:<10} ₹{acc[3]:<10} {acc[4]}")
        print(f"Total Accounts: {len(accounts)}")
        
    except Error as e:
        print(f" Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def manage_requests():
    try:
        conn = db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.req_id, u.user_name, r.req_type, r.req_amount, r.req_status, r.created_at 
            FROM requests r 
            JOIN users u ON r.user_id = u.user_id 
            ORDER BY r.req_status, r.created_at
        """)
        requests = cursor.fetchall()
        
        print("\n=== SERVICE REQUESTS ===")
        if not requests:
            print("No pending requests!")
            return
            
        print(f"{'Req ID':<8} {'User':<15} {'Type':<15} {'Amount':<12} {'Status':<10} {'Created At'}")
        print("-" * 75)
        for req in requests:
            amount = f"₹{req[3]}" if req[3] else "N/A"
            print(f"{req[0]:<8} {req[1]:<15} {req[2]:<15} {amount:<12} {req[4]:<10} {req[5]}")
        
        req_id = input("\nEnter Request ID to update (or press Enter to go back): ")
        if req_id:
            req_id = int(req_id)
            
            cursor.execute("""
                SELECT r.req_type, r.user_id, u.user_name, r.req_status
                FROM requests r 
                JOIN users u ON r.user_id = u.user_id 
                WHERE r.req_id = %s
            """, (req_id,))
            request_details = cursor.fetchone()
            
            if not request_details:
                print("Request ID not found!")
                return
                
            req_type, req_user_id, username, current_status = request_details
            
            print(f"\n Request Details:")
            print(f"User: {username} (ID: {req_user_id})")
            print(f"Request Type: {req_type}")
            print(f"Current Status: {current_status}")
            
            print("\n1. Approve")
            print("2. Reject")
            print("3. Keep Pending")
            action = input("Choose action (1-3): ")
            
            status_map = {'1': 'Approved', '2': 'Rejected', '3': 'Pending'}
            if action in status_map:
                new_status = status_map[action]
                
                if action == '1' and req_type == 'Delete Account':
                    confirm = input(f" WARNING: This will PERMANENTLY delete {username}'s account and ALL data! Confirm? (yes/no): ").lower()
                    if confirm == 'yes':
                        try:
                            print("Starting account deletion process...")
                            
                            # First, check if user still exist
                            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (req_user_id,))
                            user_exists = cursor.fetchone()
                            
                            if not user_exists:
                                print("User no longer exists!")
                                return
                            
                            
                            cursor.execute("SELECT account_balance FROM accounts WHERE user_id = %s", (req_user_id,))
                            account_info = cursor.fetchone()
                            balance = account_info[0] if account_info else 0
                            
                            print(f" Deleting account for {username} (Balance: ₹{balance})...")
                            
                            # First, delete all requests for this use
                            cursor.execute("DELETE FROM requests WHERE user_id = %s", (req_user_id,))
                            print(f" Deleted all service requests for {username}")
                            
                            cursor.execute("DELETE FROM accounts WHERE user_id = %s", (req_user_id,))
                            print(f" Deleted bank account for {username}")
                            
                            cursor.execute("DELETE FROM users WHERE user_id = %s", (req_user_id,))
                            print(f" Deleted user {username}")
                            
                            conn.commit()
                            print(f" Account for {username} has been PERMANENTLY deleted!")
                            
                        except Error as e:
                            conn.rollback()
                            print(f" Error during deletion: {e}")
                            print(" Rolling back changes...")
                            
                else:
                    cursor.execute(
                        "UPDATE requests SET req_status = %s WHERE req_id = %s",
                        (new_status, req_id)
                    )
                    conn.commit()
                    print(f" Request {req_id} updated to: {new_status}")
        
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
