from app import app, db
import models  # Make sure this imports User, Transaction, Budget

with app.app_context():
    db.create_all()
    print(" Database created successfully!")
