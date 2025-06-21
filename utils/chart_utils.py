import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')  # ✅ Use non-GUI backend for server-side plotting
import matplotlib.pyplot as plt


def create_expense_pie(user_id, transactions, output_path):
    data = {}
    for t in transactions:
        if t.user_id == user_id and t.type == 'expense':
            data[t.category] = data.get(t.category, 0) + t.amount

    if not data:
        return None

    categories = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution by Category")
    plt.tight_layout()

    # Save as static image
    plt.savefig(output_path)
    plt.close()
    return output_path
