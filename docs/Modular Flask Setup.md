# Resolving Issues with Modular Flask App Setup

This guide provides step-by-step instructions to set up a modular Flask application and address common issues encountered during development.

## **Directory Structure**
Make sure your project has the following structure:

```plaintext
satori/
├── finlytic/
│   ├── __init__.py    # Initializes the Flask app and SQLAlchemy
│   ├── app.py         # Main entry point of the application
│   ├── models.py      # Database models
│   ├── data/
│   │   └── finlytic.db # SQLite database file
│   ├── static/        # Static assets (CSS, JS, images)
│   ├── templates/     # HTML templates
├── venv/              # Python virtual environment
└── requirements.txt   # Dependencies
```

---

## **Step-by-Step Setup**

### **1. Initialize the Flask App in `__init__.py`**

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/finlytic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

---

### **2. Define Models in `models.py`**

```python
from finlytic import db

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.String(50))
```

---

### **3. Create Routes in `app.py`**

```python
from flask import request, jsonify
from finlytic import app, db
from finlytic.models import Income, Expense

@app.route("/")
def home():
    return "Welcome to Finlytic!"

@app.route("/add_income", methods=["POST"])
def add_income():
    data = request.json
    source = data.get("source")
    amount = data.get("amount")

    if not source or not amount:
        return jsonify({"error": "Invalid data"}), 400

    new_income = Income(source=source, amount=amount)
    db.session.add(new_income)
    db.session.commit()

    return jsonify({"message": "Income added successfully!"})

@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json
    name = data.get("name")
    amount = data.get("amount")
    due_date = data.get("due_date")

    if not name or not amount:
        return jsonify({"error": "Invalid data"}), 400

    new_expense = Expense(name=name, amount=amount, due_date=due_date)
    db.session.add(new_expense)
    db.session.commit()

    return jsonify({"message": "Expense added successfully!"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
        print("Database setup complete!")
    app.run(debug=True)
```

---

### **4. Create the Database**

Ensure the `data/finlytic.db` file exists. If it doesn't:

```bash
mkdir -p data
```
Run the app to create the database:

```bash
python -m finlytic.app
```

---

### **5. Verify Database**

Open the SQLite database to check the tables:

```bash
sqlite3 data/finlytic.db
```

Run the following commands:

```sql
.tables
SELECT * FROM Income;
SELECT * FROM Expense;
```

---

### **6. Run the App**

Navigate to the project root (`satori`) and run the app:

```bash
python -m finlytic.app
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## **Common Issues and Fixes**

### **Circular Import Error**
If you encounter:
```
ImportError: cannot import name '...' from partially initialized module
```
Ensure that:
- Imports in `app.py` use `from finlytic.models` instead of direct `models`.
- Run the app using `python -m` from the parent directory.

---

### **SQLite OperationalError: unable to open database file**
- Verify the `data/` folder exists.
- Ensure the `data/finlytic.db` file has proper write permissions:

```bash
chmod 666 data/finlytic.db
```

---

### **ModuleNotFoundError: No module named 'finlytic'**
- Ensure you're running the app from the `satori` directory:

```bash
python -m finlytic.app
