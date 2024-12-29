from flask import Flask, render_template, request, redirect, url_for, flash
import database as db  # Import the database functions
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# Step 1: Homepage
@app.route('/')
def index():
    profile = db.get_profile()  # Get the user's profile
    expenses = db.get_all_expenses()  # Get all expenses
    incomes = db.get_all_incomes()  # Get all incomes
    return render_template('index.html', profile=profile, expenses=expenses, incomes=incomes)

# Step 2: Profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        profession = request.form['profession']

        if not name or not age or not profession:  # Simple validation
            flash("All fields are required!", "danger")
            return redirect(url_for('profile'))

        profile = db.get_profile()  # Check if a profile already exists
        if profile:
            db.update_profile(profile[0], name, int(age), profession)
            flash("Profile updated successfully!", "success")
        else:
            db.insert_profile(name, int(age), profession)
            flash("Profile created successfully!", "success")
        return redirect(url_for('index'))

    profile = db.get_profile()
    return render_template('profile.html', profile=profile)

# Step 3: Add Expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = request.form['amount']
    if not amount:
        flash("Amount is required!", "danger")
        return redirect(url_for('index'))
    db.insert_expense(float(amount))
    flash("Expense added successfully!", "success")
    return redirect(url_for('index'))

# Step 4: Add Income
@app.route('/add_income', methods=['POST'])
def add_income():
    amount = request.form['amount']
    if not amount:
        flash("Amount is required!", "danger")
        return redirect(url_for('index'))
    db.insert_income(float(amount))
    flash("Income added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    if request.method == 'POST':
        amount = request.form['amount']
        db.update_expense(expense_id, float(amount))
        flash("Expense updated successfully!", "success")
        return redirect(url_for('index'))
    expense = next((e for e in db.get_all_expenses() if e[0] == expense_id), None)
    return render_template('edit_expense.html', expense=expense)

@app.route('/edit_income/<int:income_id>', methods=['GET', 'POST'])
def edit_income(income_id):
    if request.method == 'POST':
        amount = request.form['amount']
        db.update_income(income_id, float(amount))
        flash("Income updated successfully!", "success")
        return redirect(url_for('index'))
    income = next((i for i in db.get_all_incomes() if i[0] == income_id), None)
    return render_template('edit_income.html', income=income)

@app.route('/analytics')
def analytics():
    try:
        expenses = [e[1] for e in db.get_all_expenses()]
        incomes = [i[1] for i in db.get_all_incomes()]
        print(f"Expenses: {expenses}, Incomes: {incomes}")  # Debug
        return render_template('analytics.html', expenses=expenses, incomes=incomes)
    except Exception as e:
        print(f"Error loading analytics: {e}")
        return "An error occurred while loading analytics.", 500

@app.route('/advice')
def advice():
    total_expenses = sum([e[1] for e in db.get_all_expenses()])
    total_income = sum([i[1] for i in db.get_all_incomes()])
    advice_message = (
        "You're doing great! Keep it up!" if total_income > total_expenses
        else "Your expenses are higher than your income. Consider budgeting!"
    )
    return render_template('advice.html', advice=advice_message, total_income=total_income, total_expenses=total_expenses)


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
