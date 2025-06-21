#  app.py

import os
from flask import Flask, redirect, url_for, render_template
from flask_login import login_required, current_user
from flask_mail import Mail, Message

#  Import extensions
from extensions import db, login_manager, mail

#  Initialize Flask app
app = Flask(__name__)
#  Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '1nionbarai@gmail.com'          
app.config['MAIL_PASSWORD'] = 'yzgl rnol hbgn ecit'        
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'    

app.secret_key = 'your-secret-key'

# SQLite DB path setup
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database', 'finance.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Initialize extensions
db.init_app(app)
login_manager.init_app(app)
mail = Mail(app)
login_manager.login_view = 'auth.login'

#  Import models after db init (avoid circular import)
from models import User, Transaction

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#  Register Blueprints
from routes.auth_routes import auth_bp
from routes.finance_routes import finance_bp
from routes.report_routes import report_bp

app.register_blueprint(auth_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(report_bp)

#  Default route goes to login page
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

#  Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    income = sum(t.amount for t in Transaction.query.filter_by(user_id=current_user.id, type='income'))
    expense = sum(t.amount for t in Transaction.query.filter_by(user_id=current_user.id, type='expense'))
    return render_template('dashboard.html', income=income, expense=expense)

if __name__ == '__main__':
    app.run(debug=True)