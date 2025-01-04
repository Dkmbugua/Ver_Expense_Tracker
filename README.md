Expense Tracker Application link to website  https://ver-expense-tracker.onrender.com/

An advanced, user-friendly web-based financial management application for tracking expenses, incomes, and savings while offering analytical insights and budgetary advice.

Features
User Authentication:

User registration, login, and logout functionalities.
Profile management for storing user information like name, age, and profession.
![Screenshot (236)](https://github.com/user-attachments/assets/0bf4f236-d96f-4504-beb7-dd2ffab782ea)

Expense and Income Management:

Add, edit, and delete expenses and incomes.
Categorize expenses for better organization.
![Screenshot (237)](https://github.com/user-attachments/assets/a2c3167a-c137-4b54-972d-abbf117069b8)
Recurring Transactions:

Add recurring incomes and expenses with customizable frequencies.
Edit or delete recurring transactions.
Analytics Dashboard:

Dynamic visualizations of expense distribution, monthly income vs. expenses, and savings growth.
Supports bar, pie, and line charts for financial analytics.
Financial Advice:

Provides personalized advice based on savings and income-to-expense ratios.
Encourages budgeting and investment strategies for better financial health.

![Screenshot (238)](https://github.com/user-attachments/assets/feffc15e-ba48-44dd-bf87-bc26eb30f973)

Expense Summary:

A categorized summary of all expenses for easy tracking.
Responsive Design:

Fully responsive and optimized for both small and large screens.
![Screenshot (240)](https://github.com/user-attachments/assets/00e8a5eb-6c7e-49d6-b46d-04b77212fd6f)

![Screenshot (241)](https://github.com/user-attachments/assets/11a60e57-675f-4828-bf37-76f47f280286)

Installation and Setup
Prerequisites
Python 3.8+ installed on your system.
A virtual environment tool like venv or virtualenv.
Step-by-Step Setup
Clone the Repository:

bash
Copy code
git clone https://github.com/Dkmbugua/Ver_Expense_Tracker.git
cd Var_Expense_Tracker
Set Up Virtual Environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Initialize the Database:

Create tables using the database schema defined in database.py. Run:
bash
Copy code
python -c "import database as db; db.create_tables()"
Verify that finance.db is created in your project directory.
Run the Application:

bash
Copy code
python app.py
Access the website at https://ver-expense-tracker.onrender.com/
Deployment
The application can be deployed to a cloud hosting platform like Render or Railway.

Deployed on Render

Technologies Used
Backend: Flask (Python)
Frontend: HTML5, CSS3, JavaScript (with Plotly.js for visualizations)
Database: SQLite for persistent data storage
Authentication: Flask-Login for user session management
Hosting: Render / Railway for deployment
