# 💸 Personal Finance Manager (Flask App)

A beautiful and user-friendly personal finance management system built with Flask. It helps users track income, expenses, set monthly category-wise budgets, and get notified (on screen and via email) when they exceed those budgets.

---

## 📂 Features

- ✅ User Registration & Login
- ✅ Add, View, and Track Income & Expenses
- ✅ Set Monthly Budget Limits per Category
- ✅ Flash Warnings & Email Alerts when Over Budget
- ✅ Dashboard Summary with Income, Expenses & Balance
- ✅ Budget Report with Pie Chart Distribution (matplotlib)
- ✅ Responsive UI with Clean Gradient Styling

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/personal-finance-app.git
cd personal-finance-app
.
.
.
Create and Activate a Virtual Environment 
python -m venv venv
# Activate:
venv\Scripts\activate    # on Windows
source venv/bin/activate # on macOS/Linux
.
.
.
Install Requirements
pip install -r requirements.txt
.
.
.
Initialize the Database
python setup_db.py     <-----run this in terminal
.
.
.
Run the App
python app.py          <-----run this in terminal

Now open your browser and visit:   http://127.0.0.1:5000/login
.
.
.
📧 Email Alerts (for Budget Exceed)
To enable email notifications:

Go to app.py

Set your Flask-Mail config:

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'  # Not your main Gmail password

Enable less secure app access or use App Passwords if using Gmail.
.
.
.
🧪 Run Tests
pytest tests/
includes:
test_auth.py
test_transaction.py
.
.
.
🔄 Backup
Run the script to create a backup of your database:
.
.
.
📁 Project Structure


personal-finance-app/
├── app.py
├── extensions.py
├── models.py
├── setup_db.py
├── backup.py
├── requirements.txt
├── README.md
│
├── database/
│   └── finance.db (auto-created)
│
├── static/
│   └── styles.css
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── add_transaction.html
│   ├── view_transactions.html
│   ├── set_budget.html
│   └── report.html
│
├── routes/
│   ├── auth_routes.py
│   ├── finance_routes.py
│   └── report_routes.py
│
└── utils/
    └── chart_utils.py
.
.
.
👨‍💻 Built With
Flask

SQLite

SQLAlchemy

Flask-Login

Flask-Mail

matplotlib

Html (jinja)/css