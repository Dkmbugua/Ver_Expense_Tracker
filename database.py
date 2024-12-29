import sqlite3  # Import the database library

DB_NAME = "finance.db"  # Name of the database file

# Step 1: Create tables
def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create the profile table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            profession TEXT NOT NULL
        )
    ''')

    # Create the expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the incomes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Step 2: CRUD for Profile
def insert_profile(name, age, profession):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO profile (name, age, profession) VALUES (?, ?, ?)", (name, age, profession))
    conn.commit()
    conn.close()

def get_profile():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile LIMIT 1")
    profile = cursor.fetchone()  # Get the first row
    conn.close()
    return profile

def update_profile(profile_id, name, age, profession):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE profile SET name = ?, age = ?, profession = ? WHERE id = ?", (name, age, profession, profile_id))
    conn.commit()
    conn.close()

# Step 3: CRUD for Expenses
def insert_expense(amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount) VALUES (?)", (amount,))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return expenses

# Step 4: CRUD for Incomes
def insert_income(amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO incomes (amount) VALUES (?)", (amount,))
    conn.commit()
    conn.close()

def get_all_incomes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incomes")
    incomes = cursor.fetchall()
    conn.close()
    return incomes

# Create tables when this file runs
if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
