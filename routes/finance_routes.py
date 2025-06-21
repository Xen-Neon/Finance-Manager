from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Transaction, Budget
from datetime import datetime
from sqlalchemy import func
from flask_mail import Message
from extensions import mail

finance_bp = Blueprint('finance', __name__)

# 📥 Add Transaction
@finance_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        t_type = request.form['type']
        category = request.form['category']

        try:
            amount = float(request.form['amount'])
        except ValueError:
            flash("❌ Invalid amount entered.", "error")
            return redirect(url_for('finance.add_transaction'))

        transaction = Transaction(
            type=t_type,
            category=category,
            amount=amount,
            user_id=current_user.id,
            date=datetime.utcnow()
        )

        db.session.add(transaction)

        # ✅ Budget Check Logic
        if t_type == 'expense':
            start_of_month = datetime.utcnow().replace(day=1)
            total_spent = db.session.query(
                func.sum(Transaction.amount)
            ).filter_by(
                user_id=current_user.id,
                category=category,
                type='expense'
            ).filter(Transaction.date >= start_of_month).scalar() or 0

            budget = Budget.query.filter_by(user_id=current_user.id, category=category).first()
            if budget and total_spent > budget.limit_amount:
                message_text = (
                    f"⚠️ Budget exceeded for '{category}'!\n"
                    f"Limit: ₹{round(budget.limit_amount, 2)}, Spent: ₹{round(total_spent, 2)}"
                )
                flash(message_text, "warning")

                # 📧 Send email if user's email is present
                if current_user.email:
                    msg = Message(
                        subject="🚨 Budget Limit Exceeded",
                        recipients=[current_user.email],
                        body=message_text
                    )
                    mail.send(msg)

        db.session.commit()
        flash("✅ Transaction added.", "success")
        return redirect(url_for('finance.view_transactions'))

    return render_template('add_transaction.html')


# 📄 View Transactions
@finance_bp.route('/transactions')
@login_required
def view_transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('view_transactions.html', transactions=transactions)


# 💰 Set or Update Budget
@finance_bp.route('/set-budget', methods=['GET', 'POST'])
@login_required
def set_budget():
    if request.method == 'POST':
        category = request.form['category']

        try:
            limit = float(request.form['limit'])
        except ValueError:
            flash("❌ Invalid budget amount.", "error")
            return redirect(url_for('finance.set_budget'))

        existing = Budget.query.filter_by(user_id=current_user.id, category=category).first()
        if existing:
            existing.limit_amount = limit
            flash(f"✅ Budget for '{category}' updated to ₹{round(limit, 2)}.", "success")
        else:
            new_budget = Budget(category=category, limit_amount=limit, user_id=current_user.id)
            db.session.add(new_budget)
            flash(f"✅ Budget set for '{category}': ₹{round(limit, 2)}.", "success")

        db.session.commit()
        return redirect(url_for('finance.set_budget'))

    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    return render_template('set_budget.html', budgets=budgets, now=datetime.utcnow())
