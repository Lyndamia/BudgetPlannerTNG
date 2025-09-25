import json
import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import date, datetime

# Font
LARGE_FONT = ("Arial", 12)

# Create file for budgetdata in json
def load_data(filename='budget_data.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save file for budgetdata in json
def save_data(data, filename='budget_data.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError:
        messagebox.showerror("File Save Error", "Could not save data. Please check file permissions.")

# function is used to clear a tkinter frame
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Show function budget suggestion
def get_budget_suggestion(monthly_data, user_name, main_frame):
    clear_frame(main_frame)

    if user_name not in monthly_data or not monthly_data[user_name]:
        messagebox.showinfo("No Data", "Not enough data to make a suggestion. Please track spending for at least one month.")
        return

    latest_month = list(monthly_data[user_name].keys())[-1]
    monthly_spending = monthly_data[user_name][latest_month]['spending']
    monthly_budget = monthly_data[user_name][latest_month]['budget']

    suggestion_label = tk.Label(main_frame, text=f"----- Budget Suggestion for {user_name} -----", font=LARGE_FONT)
    suggestion_label.pack(pady=10)

    for category, spent_amount in monthly_spending.items():
        budget_amount = monthly_budget.get(category, 0)

        if spent_amount > budget_amount:
            over_by = spent_amount - budget_amount
            suggestion_text = (f"You overspent your '{category}' budget by RM {over_by:.2f} last month.\n"
                               "Suggestion: Consider increasing this category's budget slightly for a more realistic plan.")
        elif spent_amount < budget_amount:
            under_by = budget_amount - spent_amount
            suggestion_text = (f"You were under your '{category}' budget by RM {under_by:.2f} last month.\n"
                               "Suggestion: You are a great saver! Consider moving these funds to a savings category.")
        else:
            suggestion_text = (f"You are right on track for your '{category}' budget! No changes needed.")

        suggestion_content = tk.Label(main_frame, text=suggestion_text, font=LARGE_FONT)
        suggestion_content.pack(pady=5)

# Show function for monthly data summary
def display_data(monthly_data, user_name, main_frame):
    clear_frame(main_frame)
    data_label = tk.Label(main_frame, text=f"----- Monthly Data Summary for {user_name} -----", font=LARGE_FONT)
    data_label.pack(pady=10)

    if user_name not in monthly_data or not monthly_data[user_name]:
        no_data_label = tk.Label(main_frame, text="No data available yet.", font=LARGE_FONT)
        no_data_label.pack(pady=5)
    else:
        for month, data in monthly_data[user_name].items():
            month_label = tk.Label(main_frame, text=f"--- {month} ---", font=LARGE_FONT)
            month_label.pack(pady=5)

            total_spending = sum(data['spending'].values())

            total_label = tk.Label(main_frame, text=f"Total Monthly Spending: RM {total_spending:.2f}", font=LARGE_FONT)
            total_label.pack()

            for category, spent_amount in data['spending'].items():
                budget_amount = data['budget'].get(category, 0)
                category_label = tk.Label(main_frame, text=f"  - {category}: Spent RM {spent_amount:.2f} (Budget: RM {budget_amount:.2f})", font=LARGE_FONT)
                category_label.pack()

# Calculate daily allowance for each category based on the monthly budget allocation
def get_daily_allowance(budget_dict):
    today = datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    return {cat: round(amount / days_in_month, 2) for cat, amount in budget_dict.items()}

# Save the entered spending to the database
def save_daily_spending(monthly_spending_database, user_name, budget_dict, amount, category):
    today_str = date.today().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%B")
    
    # Create user profile if missing
    if user_name not in monthly_spending_database:
        monthly_spending_database[user_name] = {}

    # Create month entry if missing
    if month not in monthly_spending_database[user_name]:
        monthly_spending_database[user_name][month] = {
            "budget": budget_dict,
            "spending": {}
        }

    # Add amount to chosen category under the 'spending' key
    monthly_spending_database[user_name][month]["spending"][category] = \
        monthly_spending_database[user_name][month]["spending"].get(category, 0) + amount

    save_data(monthly_spending_database)
    messagebox.showinfo("Success", f"Added RM {amount:.2f} to {category} for today.")

# Get spending data for the current month
def get_current_month_spending(monthly_spending_database, user_name):
    month = datetime.now().strftime("%B")
    if (user_name in monthly_spending_database and
        month in monthly_spending_database[user_name]):
        return monthly_spending_database[user_name][month]["spending"]
    return {}