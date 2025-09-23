import json
import tkinter as tk
from tkinter import messagebox

def load_data():
    try:
        with open('budget_data.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open('budget_data.json', 'w') as file:
        json.dump(data, file, indent=4)

def update_monthly_data(monthly_data, user_name, month_name, total_wants_spending, wants_budget):
    if user_name not in monthly_data:
        monthly_data[user_name] = {}
        
    if month_name not in monthly_data[user_name]:
        monthly_data[user_name][month_name] = {'spending': total_wants_spending, 'budget': wants_budget}
    else:
        monthly_data[user_name][month_name]['spending'] += total_wants_spending

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def get_budget_suggestion(monthly_data, user_name, main_frame):

    clear_frame(main_frame)

    if user_name not in monthly_data or len(monthly_data[user_name]) < 1:
        messagebox.showinfo("No Data", "Not enough data to make a suggestion. Please track spending for at least one month.")
        return

    latest_month = list(monthly_data[user_name].keys())[-1]
    spending = monthly_data[user_name][latest_month]['spending']
    budget = monthly_data[user_name][latest_month]['budget']

    if spending > budget:
        over_by = spending - budget
        suggestion_text = (f"You overspent your 'Wants' budget by RM {over_by:.2f} last month.\n"
                           "Suggestion: Consider increasing your 'Wants' budget slightly to make it more realistic.\n"
                           "Recommended new 'Wants' percentage: 35%")
    elif spending < budget:
        under_by = budget - spending
        suggestion_text = (f"You were under your 'Wants' budget by RM {under_by:.2f} last month.\n"
                           "Suggestion: You are a great saver! Consider moving more funds to savings.\n"
                           "Recommended new 'Wants' percentage: 25%")
    else:
        suggestion_text = "You are right on track! No changes needed to your budget plan."

    suggestion_label = tk.Label(main_frame, text=f"--- Budget Suggestion for {user_name} ---")
    suggestion_label.pack()
    
    suggestion_content = tk.Label(main_frame, text=suggestion_text)
    suggestion_content.pack()

def display_data(monthly_data, user_name, main_frame):

    clear_frame(main_frame)
    data_label = tk.Label(main_frame, text=f"--- Monthly Data Summary for {user_name} ---")
    data_label.pack()

    if user_name not in monthly_data or not monthly_data[user_name]:
        no_data_label = tk.Label(main_frame, text="No data available yet.")
        no_data_label.pack()
    else:
        for month, data in monthly_data[user_name].items():
            month_label = tk.Label(main_frame, text=f"Total spending for {month}: RM {data['spending']:.2f} (Budget: RM {data['budget']:.2f})")
            month_label.pack()