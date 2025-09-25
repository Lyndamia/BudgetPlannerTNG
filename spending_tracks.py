import tkinter as tk
from tkinter import Label, messagebox, StringVar, OptionMenu, Entry, Button
from datetime import datetime
import data_manager

# Font
LARGE_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 12)

def show_spending_tracker(main_frame, user_name, monthly_spending_database, budget_dict, show_main_menu_callback):
    """ Display the Daily Spending Tracker screen.
     Users can log spending for categories and view daily allowance. """
    
    # Clear previous widgets
    data_manager.clear_frame(main_frame)

    # Title
    title_label = Label(main_frame, text="Daily Spending Tracker", font=LARGE_FONT)
    title_label.pack(pady=10)

    # Greeting
    greeting_label = Label(main_frame, text=f"Hello, {user_name}!", font=LARGE_FONT)
    greeting_label.pack(pady=5)         

    # Show daily allowance per category
    allowance_dict = data_manager.get_daily_allowance(budget_dict)
    allowance_label = Label(main_frame, text="Daily Suggested Allowance:", font=LARGE_FONT)
    allowance_label.pack(pady=5)

    for cat, amt in allowance_dict.items():
        Label(main_frame, text=f"{cat}: RM {amt:.2f}", font=LARGE_FONT).pack()

    # Category dropdown (default to first category)
    categories = list(budget_dict.keys())
    if not categories:
        messagebox.showwarning("No Categories", "Please set up a budget plan with categories first.")
        show_main_menu_callback()
        return

    category_var = StringVar(value=categories[0])
    category_menu = OptionMenu(main_frame, category_var, *categories)
    category_menu.pack(pady=5)

    # Input spending amount 
    amount_var = StringVar()
    amount_entry = Entry(main_frame, textvariable=amount_var, font=LARGE_FONT)
    amount_entry.pack(pady=5)

    def save_spending():
        """ Save the entered spending to the database """
        try:
            amount = float(amount_var.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for amount.")
            return
        
        category = category_var.get()
        data_manager.save_daily_spending(monthly_spending_database, user_name, budget_dict, amount, category)
        
        # Refresh display
        show_spending_tracker(main_frame, user_name, monthly_spending_database, budget_dict, show_main_menu_callback)

    # Save button
    save_button = Button(main_frame, text="Save Spending", font=BUTTON_FONT, command=save_spending)
    save_button.pack(pady=10)

    # Display today's spending
    current_spending = data_manager.get_current_month_spending(monthly_spending_database, user_name)
    if current_spending:
        Label(main_frame, text="Current Monthly Spending:", font=LARGE_FONT).pack(pady=5)
        for cat, amt in current_spending.items():
            Label(main_frame, text=f"{cat}: RM {amt:.2f}", font=LARGE_FONT).pack()
            
    # Back to Main Menu button
    back_button = Button(main_frame, text="Back to Main Menu", font=BUTTON_FONT, command=show_main_menu_callback)
    back_button.pack(pady=10)