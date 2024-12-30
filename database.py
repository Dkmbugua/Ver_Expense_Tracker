import sqlite3  # Import the database library
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "finance.db"  # Name of the database file

# Create tables
def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Profile table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            profession TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')


    # Incomes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    # Add the category column to the expenses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL DEFAULT 'Other',
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')


    conn.commit()
    conn.close()

# Fetch a user by username
def get_user_by_username(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Fetch a user by ID
def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Register a new user
def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True  # Success
    except sqlite3.IntegrityError:  # Username already exists
        return False
    finally:
        conn.close()

# Verify a user's password
def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)

# Profile CRUD operations
def insert_profile(user_id, name, age, profession):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO profile (user_id, name, age, profession) VALUES (?, ?, ?, ?)",
        (user_id, name, age, profession)
    )
    conn.commit()
    conn.close()

def get_profile(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile WHERE user_id = ?", (user_id,))
    profile = cursor.fetchone()
    conn.close()
    return profile

def update_profile(user_id, name, age, profession):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE profile SET name = ?, age = ?, profession = ? WHERE user_id = ?",
        (name, age, profession, user_id)
    )
    conn.commit()
    conn.close()

# CRUD operations for expenses
def insert_expense(amount, user_id, category='Uncategorized'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, user_id, category) VALUES (?, ?, ?)", (amount, user_id, category))
    conn.commit()
    conn.close()

def get_all_expenses(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()
    conn.close()
    return expense

def update_expense(expense_id, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE expenses SET amount = ? WHERE id = ?", (amount, expense_id))
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

# CRUD operations for incomes
def insert_income(amount, user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO incomes (amount, user_id) VALUES (?, ?)", (amount, user_id))
    conn.commit()
    conn.close()

def get_all_incomes(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incomes WHERE user_id = ?", (user_id,))
    incomes = cursor.fetchall()
    conn.close()
    return incomes

def get_income(income_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incomes WHERE id = ?", (income_id,))
    income = cursor.fetchone()
    conn.close()
    return income

def update_income(income_id, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE incomes SET amount = ? WHERE id = ?", (amount, income_id))
    conn.commit()
    conn.close()

def delete_income(income_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incomes WHERE id = ?", (income_id,))
    conn.commit()
    conn.close()


def get_expenses_grouped_by_category(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch expenses grouped by category with their total amounts
    cursor.execute("""
        SELECT category, SUM(amount) 
        FROM expenses 
        WHERE user_id = ?
        GROUP BY category
    """, (user_id,))

    grouped_expenses = cursor.fetchall()
    conn.close()

    # Convert the result into a dictionary {category: total_amount}
    return {row[0]: row[1] for row in grouped_expenses}


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
