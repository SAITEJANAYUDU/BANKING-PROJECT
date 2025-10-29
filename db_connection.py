import mysql.connector
from mysql.connector import Error

def db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='HDFCBANKING'
        )
        if conn.is_connected():
            print("db_connected successfully...")
            return conn
    except Error as e:
        print(f" Database connection failed: {e}")
        return None

def initialize_database():
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = conn.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS HDFCBANKING")
        cursor.execute("USE HDFCBANKING")
        
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                user_name VARCHAR(50) UNIQUE NOT NULL,
                user_password VARCHAR(255) NOT NULL,
                user_role ENUM('customer', 'admin') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT,
                account_type ENUM('savings', 'current') NOT NULL,
                account_balance DECIMAL(12,2) DEFAULT 1000.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        
        cursor.execute("DROP TABLE IF EXISTS requests")
        
        cursor.execute("""
            CREATE TABLE requests (
                req_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT,
                req_type ENUM('Loan', 'ATM Card', 'Cheque Book', 'Delete Account') NOT NULL,
                req_amount DECIMAL(12,2) DEFAULT NULL,
                req_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        
        cursor.execute("SELECT * FROM users WHERE user_name = 'Malleshyadav'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (user_name, user_password, user_role) VALUES (%s, %s, %s)",
                ('Malleshyadav', '123456', 'admin')
            )
            print(" Admin user 'Malleshyadav' created!")
        
        conn.commit()
        print(" HDFCBANKING database initialized successfully!")
        
    except Error as e:
        print(f" Database initialization failed: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


initialize_database()
