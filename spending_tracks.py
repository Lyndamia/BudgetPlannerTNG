# spending_tracks.py

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from datetime import date, datetime
import data_manager
import calendar

# Font
LARGE_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 12)

def get_daily_allowance(budget_dict):
    """ Calculate daily allowance for each category 
    based on the monthly budget allocation"""
    today = datetime.now()

    # Get number of days in current month
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    
    # Divide each category budget by number of days
    return {cat: round(amount / days_in_month, 2) for cat, amount in budget_dict.items()}

def show_spending_tracker(main_frame, user_name, monthly_spending_database, budget_dict):
    """ Display the Daily Spending Tracker screen.
     Users can log spending for categories and view daily allowance. """
    
    # Clear previous widgets
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Title
    title_label = Label(main_frame, text="Daily Spending Tracker", font=LARGE_FONT)
    title_label.pack(pady=10)

    # Greeting
    greeting_label = Label(main_frame, text=f"Hello, {user_name}!", font=LARGE_FONT)
    greeting_label.pack(pady=5)         

    #Show today's date
    today_str = date.today().strftime("%B %d, %Y")
    today_label = Label(main_frame, text=f"Today's Date: {today_str}", font=LARGE_FONT)
    today_label.pack(pady=5)

    #Show daily allowance per category
    allowance_dict = get_daily_allowance(budget_dict)
    allowance_label = Label(main_frame, text="Daily Suggested Allowance:", font=LARGE_FONT)
    allowance_label.pack(pady=5)

    for cat, amt in allowance_dict.items():
        Label(main_frame, text=f"{cat}: RM {amt:<.2f>}", font=LARGE_FONT).pack()

    # Category dropdown (default to first category)
    category_var = StringVar(value=list(budget_dict.keys())[0])
    category_menu = OptionMenu(main_frame, category_var, *budget_dict.keys())
    category_menu.pack(pady=5)

    # input spending amount 
    amount_var = StringVar()
    amount_entry = Entry(main_frame, textvariable=amount_var, font=LARGE_FONT)
    amount_entry.pack(pady=5)

def save_spending():
        """ Save the entered spending to the database """
        try:
            amount = float(amount_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")
            return
        
        month = datetime.now().strftime("%B")

        # Create user profile is missing
        if user_name not in monthly_spending_database:
            monthly_spending_database[user_name] = {}

        # Create month entry if missing
        if month not in monthly_spending_database[user_name]:
            monthly_spending_database[user_name][month] = {
                "budget": budget_dict,
                "daily": {}
            }

        # Create today's record if missing
        if today_str not in monthly_spending_database[user_name][month]["daily"]:
            monthly_spending_database[user_name][month]["daily"][today_str] = {}

        # Add amount to chosen category
        category = category_var.get()
        monthly_spending_database[user_name][month]["daily"][today_str][category] = \
            monthly_spending_database[user_name][month]["daily"][today_str].get(category,0) + amount
        
        # Save to JSON
        data_manager.save_data(monthly_spending_database, 'monthly_spending_database.json')
        messagebox.showinfo("Success", f"Added RM {amount:.2f} to {category} for today.")

        #Refresh display
        show_spending_tracker(main_frame, user_name, monthly_spending_database, budget_dict)    

    save_button = Button(main_frame, text="Save Spending", font=BUTTON_FONT, command=save_spending)
    save_button.pack(pady=10)
