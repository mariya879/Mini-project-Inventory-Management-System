import sqlite3

def seed_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # --- Create Tables ---
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('Admin','Customer','Staff')) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Supplier (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_no TEXT,
        address TEXT
    );

    CREATE TABLE IF NOT EXISTS Product (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        quantity INTEGER DEFAULT 0,
        price REAL NOT NULL,
        supplier_id INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
    );

    CREATE TABLE IF NOT EXISTS Transactions (
        txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        user_id INTEGER,
        txn_type TEXT CHECK(txn_type IN ('Purchase','Sale')) NOT NULL,
        quantity INTEGER NOT NULL,
        date TEXT DEFAULT (DATE('now')),
        FOREIGN KEY (product_id) REFERENCES Product(product_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    );
    """)

    # --- Insert Users (unique usernames) ---
    users = [
        ('admin', 'admin123', 'Admin'),
        ('john_doe', 'pass123', 'Customer'),
        ('alice', 'alicepwd', 'Customer'),
        ('bob', 'bobpwd', 'Customer'),
        ('charlie', 'charliepwd', 'Customer'),
        ('david', 'davidpwd', 'Customer'),
        ('emma', 'emmapwd', 'Customer'),
        ('frank', 'frankpwd', 'Customer'),
        ('grace', 'gracepwd', 'Customer'),
        ('staff1', 'staffpwd', 'Staff')
    ]
    cursor.executemany("INSERT OR IGNORE INTO User (username, password, role) VALUES (?, ?, ?)", users)

    # --- Insert Suppliers (avoid duplicates by checking count) ---
    cursor.execute("SELECT COUNT(*) FROM Supplier")
    if cursor.fetchone()[0] == 0:
        suppliers = [
            ('ABC Traders', '9876543210', 'New Delhi'),
            ('Global Supplies', '9876501234', 'Mumbai'),
            ('QuickMart Distributors', '9988776655', 'Chennai'),
            ('FreshStock Ltd', '9123456789', 'Bangalore'),
            ('City Wholesale', '9898989898', 'Kolkata'),
            ('FastTrack Suppliers', '9765432100', 'Hyderabad'),
            ('Prime Distribution', '9001122334', 'Pune'),
            ('MegaMart Supply Co', '9887766554', 'Jaipur'),
            ('GreenLeaf Traders', '9345678901', 'Lucknow'),
            ('SuperStock Pvt Ltd', '9456123789', 'Ahmedabad')
        ]
        cursor.executemany("INSERT INTO Supplier (name, contact_no, address) VALUES (?, ?, ?)", suppliers)

    # --- Insert Products (avoid duplicates by checking count) ---
    cursor.execute("SELECT COUNT(*) FROM Product")
    if cursor.fetchone()[0] == 0:
        products = [
            ('Rice Bag 25kg', 'Grocery', 50, 1200.00, 1),
            ('Wheat Flour 10kg', 'Grocery', 80, 450.00, 1),
            ('Cooking Oil 5L', 'Grocery', 60, 750.00, 2),
            ('Shampoo 500ml', 'Personal Care', 40, 180.00, 3),
            ('Soap Pack (4)', 'Personal Care', 70, 90.00, 4),
            ('Toothpaste 200g', 'Personal Care', 100, 95.00, 5),
            ('Notebook A4', 'Stationery', 120, 60.00, 6),
            ('Ball Pen Pack (10)', 'Stationery', 200, 150.00, 7),
            ('Printer Ink Cartridge', 'Electronics', 25, 950.00, 8),
            ('USB Flash Drive 32GB', 'Electronics', 45, 600.00, 9)
        ]
        cursor.executemany("INSERT INTO Product (name, category, quantity, price, supplier_id) VALUES (?, ?, ?, ?, ?)", products)

    # --- Insert Transactions (avoid duplicates by checking count) ---
    cursor.execute("SELECT COUNT(*) FROM Transactions")
    if cursor.fetchone()[0] == 0:
        transactions = [
            (1, 2, 'Sale', 2, '2025-08-01'),
            (2, 3, 'Sale', 1, '2025-08-02'),
            (3, 4, 'Sale', 1, '2025-08-03'),
            (4, 5, 'Sale', 2, '2025-08-04'),
            (5, 6, 'Sale', 3, '2025-08-05'),
            (6, 7, 'Sale', 2, '2025-08-06'),
            (7, 8, 'Sale', 5, '2025-08-07'),
            (8, 9, 'Sale', 2, '2025-08-08'),
            (9, 2, 'Purchase', 10, '2025-08-09'),
            (10, 3, 'Purchase', 15, '2025-08-10')
        ]
    cursor.executemany("INSERT INTO Transactions (product_id, user_id, txn_type, quantity, date) VALUES (?, ?, ?, ?, ?)", transactions)

    conn.commit()
    conn.close()
    print("✅ Database seeded with sample data successfully (no duplicates)!")


if __name__ == "__main__":
    seed_database()
