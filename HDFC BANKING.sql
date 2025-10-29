Create database HDFCBANKING;


use HDFCBANKING;


CREATE TABLE IF NOT EXISTS users (
	user_id INT PRIMARY KEY AUTO_INCREMENT,
	user_name VARCHAR(50) UNIQUE NOT NULL,
	user_password VARCHAR(255) NOT NULL,
	user_role ENUM('customer', 'admin') NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select *
from users;
        
# Create accounts table
CREATE TABLE IF NOT EXISTS accounts (
	account_id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT,
	account_type ENUM('savings', 'current') NOT NULL,
	account_balance DECIMAL(12,2) DEFAULT 0.00,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES users(user_id)
	);
    
    select *
    from accounts;
        
        # Create requests table

CREATE TABLE IF NOT EXISTS requests (
	req_id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT,
	req_type ENUM('Loan', 'ATMCARD', 'Cheque Book','Delete account') NOT NULL,
	req_amount DECIMAL(12,2) DEFAULT NULL,
	req_balance DECIMAL(12,2) DEFAULT 0.00,
	req_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE cascade
	);
    
    select *
    from requests;
    describe requests;
    
    USE HDFCBANKING;

DROP TABLE IF EXISTS requests;

CREATE TABLE requests (
    req_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    req_type ENUM('Loan', 'ATMCard', 'ChequeBook') NOT NULL,
    req_amount DECIMAL(12,2) DEFAULT NULL,
    req_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

DESCRIBE requests;



