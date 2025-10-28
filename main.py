# main.py
from db_connection import initialize_database
from authentication import signup, login  # Fixed typo: 'authentication' not 'authencation'
from customer_menu import customer_dashboard    # Fixed: 'customer' not 'customer_menu'
from admin_menu import admin_dashboard

def main():
    print("🚀 Starting HDFC Banking System...")
    initialize_database()  # Initialize database at startup
    
    while True:
        print("\n" + "="*50)
        print("          🏦 WELCOME TO HDFC BANKING SYSTEM")
        print("="*50)
        print("1. 👤 Sign Up")
        print("2. 🔐 Login")
        print("3. 🚪 Exit")
        print("-"*50)
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            user_id = signup()
            if user_id:
                print("✅ Please login with your new account!")
                
        elif choice == '2':
            user_id, username, user_role = login()
            if user_id:
                if user_role == 'customer':
                    customer_dashboard(user_id, username)
                elif user_role == 'admin':
                    print(f"🎯 Welcome Admin {username}!")
                    admin_dashboard()
                    
        elif choice == '3':
            print("👋 Thank you for using HDFC Banking System! Goodbye! 👋")
            break
            
        else:
            print("❌ Invalid option! Please try again.")

if __name__ == "__main__":
    main()