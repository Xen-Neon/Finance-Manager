import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from extensions import db
from models import Budget, Transaction
from utils.chart_utils import create_expense_pie

report_bp = Blueprint('report', __name__)

# 💰 Set Budget Route
@report_bp.route('/set-budget', methods=['GET', 'POST'])
@login_required
def set_budget():
    if request.method == 'POST':
        category = request.form['category']
        limit_amount = float(request.form['limit_amount'])

        existing = Budget.query.filter_by(user_id=current_user.id, category=category).first()
        if existing:
            existing.limit_amount = limit_amount
        else:
            new_budget = Budget(category=category, limit_amount=limit_amount, user_id=current_user.id)
            db.session.add(new_budget)

        db.session.commit()
        return redirect(url_for('report.view_report'))

    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    now = datetime.utcnow()
    return render_template('set_budget.html', budgets=budgets, now=now)

# 📊 View Report Route
@report_bp.route('/report')
@login_required
def view_report():
    now = datetime.utcnow()
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    summary = {}
    for budget in budgets:
        spent = sum(
            t.amount for t in transactions
            if t.category == budget.category and t.type == 'expense'
        )
        summary[budget.category] = {
            'limit': budget.limit_amount,
            'spent': spent,
            'remaining': budget.limit_amount - spent
        }

    # Generate chart
    chart_filename = f'pie_{current_user.id}.png'
    chart_path = os.path.join('static', chart_filename)
    chart_generated = create_expense_pie(current_user.id, transactions, chart_path)

    return render_template(
        'report.html',
        budgets=budgets,
        now=now,
        summary=summary,
        chart_url=chart_filename if chart_generated else None
    )
