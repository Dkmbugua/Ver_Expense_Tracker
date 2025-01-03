from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import database as db
import os


app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# Step 1: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Step 2: User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    user = db.get_user_by_id(user_id)  # Load user by ID (fixes initial issue)
    if user:
        return User(id=user[0], username=user[1])
    return None

# Step 3: Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check for empty username or password
        if not username or not password:
            flash("Username and password are required!", "danger")
            return redirect(url_for('register'))

        # Try to register the user
        if not db.register_user(username, password):
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        # Registration successful
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user_by_username(username)

        # Check credentials
        if not user or not db.verify_password(user[2], password):
            flash("Invalid credentials! Please try again.", "danger")
            return redirect(url_for('login'))
        
        login_user(User(id=user[0], username=user[1]))
        flash("Logged in successfully!", "success")

        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index'))

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))
# Profile Management

@app.route('/')  # Ensure this route is defined only once
@login_required
def index():
    profile = db.get_profile(current_user.id)  # Fetch profile
    expenses = db.get_all_expenses(current_user.id)  # Fetch expenses
    incomes = db.get_all_incomes(current_user.id)  # Fetch incomes
    print("Index - Profile fetched:", profile)  # Debugging output
    return render_template('index.html', profile=profile, expenses=expenses, incomes=incomes)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Fetch data from form
        name = request.form['name']
        age = request.form['age']
        profession = request.form['profession']

        # Validate form data
        if not name or not age or not profession:
            flash("All fields are required!", "danger")
            return redirect(url_for('profile'))

        # Check if profile already exists
        profile = db.get_profile(current_user.id)
        print("Profile fetched for update/insertion:", profile)  # Debugging output

        if profile:
            # Update existing profile
            db.update_profile(current_user.id, name, int(age), profession)
            flash("Profile updated successfully!", "success")
        else:
            # Insert new profile
            db.insert_profile(current_user.id, name, int(age), profession)
            flash("Profile created successfully!", "success")

        # Redirect to index after profile save
        return redirect(url_for('index'))

    # Handle GET request for profile page
    profile = db.get_profile(current_user.id)
    print("Profile fetched for rendering:", profile)  # Debugging output
    return render_template('profile.html', profile=profile)


# Expense and Income Management
@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    amount = request.form['amount']
    category = request.form.get('category', 'Uncategorized')
    if not amount:
        flash("Amount is required!", "danger")
        return redirect(url_for('index'))
    db.insert_expense(float(amount), current_user.id, category)
    flash(f"Expense added successfully under '{category}'!", "success")
    return redirect(url_for('index'))

@app.route('/add_income', methods=['POST'])
@login_required
def add_income():
    amount = request.form['amount']
    if not amount:
        flash("Amount is required!", "danger")
        return redirect(url_for('index'))
    db.insert_income(float(amount), current_user.id)
    flash("Income added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    if request.method == 'POST':
        amount = request.form['amount']
        db.update_expense(expense_id, float(amount))
        flash("Expense updated successfully!", "success")
        return redirect(url_for('index'))
    expense = db.get_expense(expense_id)
    if not expense:
        flash("Expense not found!", "danger")
        return redirect(url_for('index'))
    return render_template('edit_expense.html', expense=expense)

@app.route('/edit_income/<int:income_id>', methods=['GET', 'POST'])
@login_required
def edit_income(income_id):
    if request.method == 'POST':
        amount = request.form['amount']
        db.update_income(income_id, float(amount))
        flash("Income updated successfully!", "success")
        return redirect(url_for('index'))
    income = db.get_income(income_id)
    if not income:
        flash("Income not found!", "danger")
        return redirect(url_for('index'))
    return render_template('edit_income.html', income=income)

@app.route('/delete_expense/<int:expense_id>', methods=['GET'])
@login_required
def delete_expense(expense_id):
    expense = db.get_expense(expense_id)
    if not expense:
        flash("Expense not found!", "danger")
        return redirect(url_for('index'))
    db.delete_expense(expense_id)
    flash("Expense deleted successfully!", "success")
    return redirect(url_for('index'))

@app.route('/delete_income/<int:income_id>', methods=['GET'])
@login_required
def delete_income(income_id):
    income = db.get_income(income_id)
    if not income:
        flash("Income not found!", "danger")
        return redirect(url_for('index'))
    db.delete_income(income_id)
    flash("Income deleted successfully!", "success")
    return redirect(url_for('index'))
#finance Analytics
@app.route('/analytics')
@login_required
def analytics():
    # Fetch monthly data for expenses and incomes
    monthly_expenses = db.get_monthly_expenses(current_user.id)
    monthly_incomes = db.get_monthly_incomes(current_user.id)

    # Convert to lists to avoid serialization issues
    months_expenses = [row[0] for row in monthly_expenses] if monthly_expenses else []
    expense_values = [row[1] for row in monthly_expenses] if monthly_expenses else []
    months_incomes = [row[0] for row in monthly_incomes] if monthly_incomes else []
    income_values = [row[1] for row in monthly_incomes] if monthly_incomes else []

    # Fetch categorized expenses
    categorized_expenses = db.get_expenses_grouped_by_category(current_user.id)
    categories = list(categorized_expenses.keys()) if categorized_expenses else []
    expenses_by_category = list(categorized_expenses.values()) if categorized_expenses else []

    # Calculate savings
    savings = [income - expense for income, expense in zip(income_values, expense_values)]

    # Render the analytics page with datasets
    return render_template(
        'analytics.html',
        months_expenses=months_expenses,
        expense_values=expense_values,
        months_incomes=months_incomes,
        income_values=income_values,
        categories=categories,
        expenses_by_category=expenses_by_category,
        savings=savings
    )

# Financial Advice
@app.route('/advice')
@login_required
def advice():
    # Calculate total expenses and income
    total_expenses = sum([e[1] for e in db.get_all_expenses(current_user.id)])
    total_income = sum([i[1] for i in db.get_all_incomes(current_user.id)])
    
    # Calculate savings
    savings = total_income - total_expenses

    # Generate advice message
    advice_message = []
    if total_income > total_expenses:
        advice_message.append("DK says You're doing great! Keep it up!")
    else:
        advice_message.append("DK say Your expenses are higher than your income. Consider budgeting!")
    
    if savings > 0.2 * total_income:
        advice_message.append("DK says Great job! You're saving more than 20% of your income. Consider investing your savings.")

    return render_template(
        'advice.html', 
        advice=advice_message, 
        total_income=total_income, 
        total_expenses=total_expenses, 
        savings=savings  # Pass savings to the template
    )


#expense_summary
@app.route('/expense_summary')
@login_required
def expense_summary():
    # Fetch grouped expenses by category
    grouped_expenses_dict = db.get_expenses_grouped_by_category(current_user.id)
    
    # Convert the dictionary to a list of tuples
    grouped_expenses = [(category, total) for category, total in grouped_expenses_dict.items()]
    
    # Debugging
    print("Grouped Expenses for Summary:", grouped_expenses)
    
    # Render the summary template
    return render_template('expense_summary.html', grouped_expenses=grouped_expenses)

@app.route('/add_recurring', methods=['POST'])
@login_required
def add_recurring_transaction():
    amount = request.form['amount']
    category = request.form['category']
    frequency = request.form['frequency']
    transaction_type = request.form['transaction_type']
    next_due_date = request.form['next_due_date']

    if not amount or not frequency or not transaction_type or not next_due_date:
        flash("All fields are required for recurring transactions!", "danger")
        return redirect(url_for('index'))

    db.insert_recurring_transaction(
        current_user.id, float(amount), category, frequency, next_due_date, transaction_type
    )
    flash(f"Recurring {transaction_type} added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/recurring_transactions')
@login_required
def view_recurring_transactions():
    transactions = db.get_recurring_transactions(current_user.id)
    return render_template('recurring_transactions.html', transactions=transactions)

@app.route('/delete_recurring/<int:transaction_id>', methods=['GET'])
@login_required
def delete_recurring_transaction(transaction_id):
    db.delete_recurring_transaction(transaction_id)
    flash("Recurring transaction deleted successfully!", "success")
    return redirect(url_for('recurring_transactions'))

@app.route('/edit_recurring/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_recurring_transaction(transaction_id):
    if request.method == 'POST':
        # Fetch form data
        amount = request.form['amount']
        category = request.form['category']
        frequency = request.form['frequency']
        next_due_date = request.form['next_due_date']
        transaction_type = request.form['transaction_type']

        # Update the recurring transaction
        db.update_recurring_transaction(transaction_id, amount, category, frequency, next_due_date, transaction_type)
        flash("Recurring transaction updated successfully!", "success")
        return redirect(url_for('recurring_transactions'))

    # Fetch the existing transaction details
    transaction = db.get_recurring_transaction(transaction_id)
    return render_template('edit_recurring.html', transaction=transaction)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))