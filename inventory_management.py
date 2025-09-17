import sqlite3
import getpass
from colorama import init, Fore, Style
import sqlite3
import getpass

init(autoreset=True)

# ==============================
# Supplier Module
# ==============================
def add_supplier():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()
    name = input("Supplier name: ")
    contact_no = input("Contact number: ")
    address = input("Address: ")
    cur.execute("INSERT INTO Supplier (name, contact_no, address) VALUES (?, ?, ?)",
                (name, contact_no, address))
    conn.commit()
    conn.close()
    print(Fore.GREEN + "✅ Supplier added successfully!" + Style.RESET_ALL)

def view_suppliers():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Supplier")
    rows = cur.fetchall()
    print(Fore.YELLOW + "\n--- Suppliers ---" + Style.RESET_ALL)
    print(f"{'ID':<4} {'Name':<25} {'Contact':<15} {'Address':<20}")
    print("-" * 70)
    for row in rows:
        print(f"{row[0]:<4} {row[1]:<25} {row[2]:<15} {row[3]:<20}")
    conn.close()
# ==============================
# Database Setup
# ==============================
def init_db():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    # Supplier table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Supplier (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_no TEXT,
        address TEXT
    )
    """)

    # Product table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Product (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        quantity INTEGER DEFAULT 0,
        price REAL NOT NULL,
        supplier_id INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
    )
    """)

    # User table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('Admin','Customer','Staff')) NOT NULL
    )
    """)

    # Transactions table (renamed from Transaction to avoid SQL reserved keyword)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        user_id INTEGER,
        txn_type TEXT CHECK(txn_type IN ('Purchase','Sale')) NOT NULL,
        quantity INTEGER NOT NULL,
        date TEXT DEFAULT (DATE('now')),
        FOREIGN KEY (product_id) REFERENCES Product(product_id),
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
    """)

    # Default admin
    cur.execute("SELECT * FROM User WHERE role='Admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO User (username, password, role) VALUES (?, ?, ?)",
                    ("admin", "admin123", "Admin"))
    print(Fore.GREEN + "✅ Default admin created (username: admin, password: admin123)" + Style.RESET_ALL)

    conn.commit()
    conn.close()

# ==============================
# Authentication
# ==============================
def login():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    cur.execute("SELECT user_id, role FROM User WHERE username=? AND password=?", (username, password))
    row = cur.fetchone()
    conn.close()

    if row:
        print(Fore.GREEN + f"\n✅ Login successful! Welcome, {username} ({row[1]}).\n" + Style.RESET_ALL)
        return row  # (user_id, role)
    else:
        print(Fore.RED + "❌ Invalid login!" + Style.RESET_ALL)
        return None

# ==============================
# Admin Menu
# ==============================
def admin_menu(user_id):
    while True:
        print(Fore.CYAN + "\n" + "="*40 + Style.RESET_ALL)
        print(Fore.CYAN + "{:^40}".format("ADMIN MENU") + Style.RESET_ALL)
        print(Fore.CYAN + "="*40 + Style.RESET_ALL)
        print("┌─────────┬──────────────────────┐")
        print("│  CHOICE │       ACTION         │")
        print("├─────────┼──────────────────────┤")
        print("│    1    │   Add Product        │")
        print("│    2    │   View Products      │")
        print("│    3    │   Record Purchase    │")
        print("│    4    │   View Transactions  │")
        print("│    5    │   Add Supplier       │")
        print("│    6    │   View Suppliers     │")
        print("│    7    │   Logout             │")
        print("└─────────┴──────────────────────┘")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            record_transaction(user_id, "Purchase")
        elif choice == "4":
            view_transactions()
        elif choice == "5":
            add_supplier()
        elif choice == "6":
            view_suppliers()
        elif choice == "7":
            break
        else:
            print(Fore.RED + "❌ Invalid choice!" + Style.RESET_ALL)

# ==============================
# Customer Menu
# ==============================
def customer_menu(user_id):
    while True:
        print(Fore.CYAN + "\n" + "="*40 + Style.RESET_ALL)
        print(Fore.CYAN + "{:^40}".format("CUSTOMER MENU") + Style.RESET_ALL)
        print(Fore.CYAN + "="*40 + Style.RESET_ALL)
        print("┌─────────┬────────────────────────────┐")
        print("│  CHOICE │          ACTION            │")
        print("├─────────┼────────────────────────────┤")
        print("│    1    │   View Products           │")
        print("│    2    │   Book Product (Sale)     │")
        print("│    3    │   View My Transactions    │")
        print("│    4    │   Logout                  │")
        print("└─────────┴────────────────────────────┘")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            view_products()
        elif choice == "2":
            record_transaction(user_id, "Sale")
        elif choice == "3":
            view_transactions(user_id)
        elif choice == "4":
            break
        else:
            print(Fore.RED + "❌ Invalid choice!" + Style.RESET_ALL)

# ==============================
# CRUD Operations
# ==============================
def add_product():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    name = input("Product name: ")
    category = input("Category: ")
    quantity = int(input("Quantity: "))
    price = float(input("Price: "))

    cur.execute("INSERT INTO Product (name, category, quantity, price) VALUES (?, ?, ?, ?)",
                (name, category, quantity, price))

    conn.commit()
    conn.close()
    print(Fore.GREEN + "✅ Product added successfully!" + Style.RESET_ALL)

def view_products():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM Product")
    rows = cur.fetchall()

    print(Fore.YELLOW + "\n--- Available Products ---" + Style.RESET_ALL)
    print(f"{'ID':<4} {'Name':<25} {'Category':<15} {'Qty':<6} {'Price':<8}")
    print("-" * 65)
    for row in rows:
        print(f"{row[0]:<4} {row[1]:<25} {row[2]:<15} {row[3]:<6} {row[4]:<8}")

    conn.close()

# ==============================
# Transaction Handling
# ==============================
def record_transaction(user_id, txn_type):
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    prod_id = int(input("Enter Product ID: "))
    qty = int(input("Enter quantity: "))

    # Get product stock
    cur.execute("SELECT quantity FROM Product WHERE product_id=?", (prod_id,))
    row = cur.fetchone()
    if not row:
        print(Fore.RED + "❌ Product not found!" + Style.RESET_ALL)
        conn.close()
        return
    current_qty = row[0]

    if txn_type == "Purchase":
        new_qty = current_qty + qty
        cur.execute("UPDATE Product SET quantity=? WHERE product_id=?", (new_qty, prod_id))
        cur.execute("INSERT INTO Transactions (product_id, user_id, txn_type, quantity, date) VALUES (?, ?, ?, ?, datetime('now'))",
                    (prod_id, user_id, "Purchase", qty))
        conn.commit()
        print(Fore.GREEN + f"✅ Purchase recorded. New stock: {new_qty}" + Style.RESET_ALL)
    elif txn_type == "Sale":
        if qty > current_qty:
            print(Fore.RED + "❌ Not enough stock!" + Style.RESET_ALL)
            conn.close()
            return
        new_qty = current_qty - qty
        cur.execute("UPDATE Product SET quantity=? WHERE product_id=?", (new_qty, prod_id))
        cur.execute("INSERT INTO Transactions (product_id, user_id, txn_type, quantity, date) VALUES (?, ?, ?, ?, datetime('now'))",
                    (prod_id, user_id, "Sale", qty))
        conn.commit()
        print(Fore.GREEN + f"✅ Sale recorded. Remaining stock: {new_qty}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ Invalid transaction type!" + Style.RESET_ALL)
    conn.close()
def view_transactions(user_id=None):
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    if user_id:
        cur.execute("SELECT * FROM Transactions WHERE user_id=?", (user_id,))
    else:
        cur.execute("SELECT * FROM Transactions")

    rows = cur.fetchall()

    print(Fore.YELLOW + "\n--- Transactions ---" + Style.RESET_ALL)
    print(f"{'TxnID':<6} {'ProductID':<10} {'UserID':<7} {'Type':<10} {'Qty':<5} {'Date':<20}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<6} {row[1]:<10} {row[2]:<7} {row[3]:<10} {row[4]:<5} {row[5]:<20}")

    conn.close()

# ==============================
# Main
# ==============================
def main():
    init_db()

    while True:
        user = login()
        if user:
            user_id, role = user
            if role == "Admin":
                admin_menu(user_id)
            elif role == "Customer":
                customer_menu(user_id)
        else:
            print(Fore.MAGENTA + "Try again!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
