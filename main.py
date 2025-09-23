import tkinter as tk
from tkinter import *
from tkinter import messagebox
import datetime
import data_manager

window = tk.Tk()
window.title('TnG Budget Planner')
window.geometry('500x500')

main_frame = tk.Frame(window)
main_frame.pack(fill=BOTH, expand=True)

# Global variable
custom_data = []
editable_list = []
monthly_income = 0.0
user_name = ""
monthly_spending_database = data_manager.load_data()
income_var = None

# Font
LARGE_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 12)

# Function Budgetplanner
def formula(percent):
    percent = float(percent)
    income = float(income_var.get())
    value = (percent/100)*income
    return round(value, 2)

def standard_func(standard, aggressive, choose_type_text):
    choose_button_hide_2(choose_type_text, standard, aggressive)
    needs = 50
    wants = 30
    savings = 20
    standard_label = Label(main_frame, text=f'\nSuggested Spending Limit (Standard Plan)\n\n1. Needs (50%): RM{formula(needs)}\n2. Wants (30%): RM{formula(wants)}\n3. Savings (20%): RM{formula(savings)}', font=LARGE_FONT)
    standard_label.pack(pady=10)

def aggressive_func(standard, aggressive, choose_type_text):
    choose_button_hide_2(choose_type_text, standard, aggressive)
    needs = 40
    wants = 20
    savings = 40
    standard_label = Label(main_frame, text=f'\nSuggested Spending Limit (Aggressive Plan)\n\n1. Needs (40%): RM{formula(needs)}\n2. Wants (20%): RM{formula(wants)}\n3. Savings (40%): RM{formula(savings)}', font=LARGE_FONT)
    standard_label.pack(pady=10)

def plan_1(premade, custom, choose_plan_text):
    choose_button_hide_1(choose_plan_text, premade, custom)
    choose_type_text = Label(main_frame, text='\nThere are two plans;', font=LARGE_FONT)
    standard = tk.Button(main_frame, text='Standard Plan', font=BUTTON_FONT, command=lambda:standard_func(standard, aggressive, choose_type_text))
    aggressive = tk.Button(main_frame, text='Aggressive Plan', font=BUTTON_FONT, command=lambda:aggressive_func(standard, aggressive, choose_type_text))
    choose_type_text.pack(pady=5)
    standard.pack(pady=5)
    aggressive.pack(pady=5)

def delete_func(group, data_entry):
    group.destroy()
    if data_entry in custom_data:
        custom_data.remove(data_entry)

def count_percentage():
    total_percentage = 0
    for data_entry in custom_data:
        try:
            total_percentage += int(data_entry['percent'].get())
        except ValueError:
            pass
    return total_percentage

def add_func(canvas_container):
    group = tk.Frame(canvas_container)
    group.pack(pady=5)

    category_label = Label(group, text='Category:', font=LARGE_FONT)
    category_var = StringVar()
    category_input = Entry(group, textvariable=category_var, font=LARGE_FONT)
    category_label.pack()
    category_input.pack()

    percent_label = Label(group, text='Percentage:', font=LARGE_FONT)
    percent_var = StringVar()
    percent_input = Spinbox(group, from_=1, to=100, increment=10, textvariable=percent_var, font=LARGE_FONT)
    percent_label.pack()
    percent_input.pack()

    delete = tk.Button(group, text='Delete Category', font=BUTTON_FONT, command=lambda:delete_func(group, data_entry))
    delete.pack()

    data_entry = {
        'category':category_var,
        'percent':percent_var,
        'group':group
    }
    custom_data.append(data_entry)

def edit_func(canvas_container, edit, confirm):
    for custom_categories in editable_list:
        custom_categories.destroy()
    editable_list.clear()

    confirm.pack_forget()
    edit.pack_forget()

    canvas_container.pack(fill="both", expand=True)
    for data_entry in custom_data:
        data_entry['group'].pack()
    
    # Update the scroll region after adding widgets
    canvas_container.update_idletasks()
    canvas_container.configure(scrollregion=canvas_container.bbox("all"))

def confirm_func(confirm, edit, canvas_container):
    spending_limit = Label(main_frame, text='\nSuggested spending limit:\n', font=LARGE_FONT)
    spending_limit.pack(pady=5)

    for custom_categories in editable_list:
        custom_categories.destroy()
    editable_list.clear()

    for data_entry in custom_data:
        category = data_entry['category'].get()
        percent = data_entry['percent'].get()
        value = formula(percent)
        custom_categories = Label(main_frame, text=f'- {category} ({percent}%): RM{value}', font=LARGE_FONT)
        custom_categories.pack()
        editable_list.append(custom_categories)

    confirm.pack_forget()
    edit.pack_forget()
    canvas_container.pack_forget()

def save_func(container, canvas_container):
    current_percentage = count_percentage()
    if current_percentage > 100:
        messagebox.showwarning("Percentage Inconsistency", "Total percentage exceeds 100%. Please edit.")
        return
    if current_percentage < 100:
        messagebox.showwarning("Percentage Inconsistency", "Total percentage does not reach 100%. Please edit.")
        return
    
    container.pack_forget()
    canvas_container.pack_forget()

    for data_entry in custom_data:
        data_entry['group'].pack_forget()
        category = data_entry['category'].get()
        percent = data_entry['percent'].get()
        custom_categories = Label(main_frame, text=f'- {category}: {percent}%', font=LARGE_FONT)
        custom_categories.pack()
        editable_list.append(custom_categories)
    
    edit = tk.Button(main_frame, text='Edit', font=BUTTON_FONT, command=lambda:edit_func(canvas_container, edit, confirm))
    edit.pack(pady=5)

    confirm = tk.Button(main_frame, text='Confirm', font=BUTTON_FONT, command=lambda:confirm_func(confirm, edit, canvas_container))
    confirm.pack(pady=5)

def plan_2(premade, custom, choose_plan_text):
    choose_button_hide_1(choose_plan_text, premade, custom)
    container = tk.Frame(main_frame)
    container.pack()

    # Create scrollable canvas for categories
    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=LEFT, fill="both", expand=True)
    scrollbar.pack(side=RIGHT, fill="y")
    
    canvas_container = tk.Frame(canvas)
    canvas.create_window((0, 0), window=canvas_container, anchor='nw')
    canvas_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    add = tk.Button(container, text='Add Category', font=BUTTON_FONT, command=lambda:add_func(canvas_container))
    add.pack(pady=5)

    save = tk.Button(container, text='Save', font=BUTTON_FONT, command=lambda:save_func(container, canvas_container))
    save.pack(pady=5)
    
def choose_button_hide_1(choose_plan_text, premade, custom):
    choose_plan_text.pack_forget()
    premade.pack_forget()
    custom.pack_forget()

def choose_button_hide_2(choose_type_text, standard, aggressive):
    choose_type_text.pack_forget()
    standard.pack_forget()
    aggressive.pack_forget()

def next_func(next_button):
    next_button.pack_forget()
    choose_plan_text = Label(main_frame, text = '\nHow would you like to allocate your savings?', font=LARGE_FONT)
    premade = tk.Button(main_frame, text='Use our ready made plan', font=BUTTON_FONT, command=lambda:plan_1(premade, custom, choose_plan_text))
    custom = tk.Button(main_frame, text='Create your own custom plan', font=BUTTON_FONT, command=lambda:plan_2(premade, custom, choose_plan_text))
    choose_plan_text.pack(pady=5)
    premade.pack(pady=5)
    custom.pack(pady=5)

# Main menu Function
def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def show_main_menu():
    clear_frame()

    title_label = Label(main_frame, text='\nTnG Budget Planner', font=LARGE_FONT)
    title_label.pack(pady=10)
    
    income_label = Label(main_frame, text=f'Monthly Income {user_name}: RM {monthly_income:.2f}', font=LARGE_FONT)
    income_label.pack(pady=5)
    
    main_menu_label = Label(main_frame, text="* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ", font=LARGE_FONT)
    main_menu_label.pack(pady=5)

    main_menu_label = Label(main_frame, text="\n----- Main Menu -----", font=LARGE_FONT)
    main_menu_label.pack(pady=10)

    btn_budget_plan = Button(main_frame, text="1. See Budget Plan", font=BUTTON_FONT, command=show_budget_plan)
    btn_budget_plan.pack(pady=5)

    btn_track_spending = Button(main_frame, text="2. Track Wants Spending (for 7 days)", font=BUTTON_FONT, command=show_spending_tracker)
    btn_track_spending.pack(pady=5)

    btn_data_management = Button(main_frame, text="3. See Monthly Data Management", font=BUTTON_FONT, command=show_data_management)
    btn_data_management.pack(pady=5)

    btn_budget_suggestion = Button(main_frame, text="4. Get Budget Suggestion", font=BUTTON_FONT, command=get_suggestion)
    btn_budget_suggestion.pack(pady=5)

    btn_exit = Button(main_frame, text="5. Exit", font=BUTTON_FONT, command=window.quit)
    btn_exit.pack(pady=5)

# Called from Main Menu
def show_budget_plan():
    clear_frame()
    
    title_label = Label(main_frame, text='\nTnG Budget Planner', font=LARGE_FONT)
    title_label.pack(pady=10)
    
    income_label = Label(main_frame, text=f'Monthly Income: RM {monthly_income:.2f}', font=LARGE_FONT)
    income_label.pack(pady=5)
    
    next_button = tk.Button(main_frame, text='Next', font=BUTTON_FONT, command=lambda:next_func(next_button))
    next_button.pack(pady=5)
    
    back_button = Button(main_frame, text="Back to Main Menu", font=BUTTON_FONT, command=show_main_menu)
    back_button.pack(pady=10)

def show_spending_tracker():
    clear_frame()
    spending_tracker_label = Label(main_frame, text="Daily Spending Tracker Goes Here...", font=LARGE_FONT)
    spending_tracker_label.pack(pady=10)
    
    
    back_button = Button(main_frame, text="Back to Main Menu", font=BUTTON_FONT, command=show_main_menu)
    back_button.pack(pady=10)

def show_data_management():
    clear_frame()
    data_manager.display_data(monthly_spending_database, user_name, main_frame)
    back_button = Button(main_frame, text="Back to Main Menu", font=BUTTON_FONT, command=show_main_menu)
    back_button.pack(pady=10)

def get_suggestion():
    clear_frame()
    data_manager.get_budget_suggestion(monthly_spending_database, user_name, main_frame)
    back_button = Button(main_frame, text="Back to Main Menu", font=BUTTON_FONT, command=show_main_menu)
    back_button.pack(pady=10)

# Initial setup screen
def setup_screen():
    clear_frame()
    
    global user_name_entry, income_entry, income_var

    welcome_label = Label(main_frame, text="\nWelcome to the TnG Budget Planner!", font=LARGE_FONT)
    welcome_label.pack(pady=10)
    
    name_label = Label(main_frame, text="Please enter your username:", font=LARGE_FONT)
    name_label.pack(pady=5)
    user_name_entry = Entry(main_frame, font=LARGE_FONT)
    user_name_entry.pack(pady=5)
    
    income_label = Label(main_frame, text="Enter your monthly income:", font=LARGE_FONT)
    income_label.pack(pady=5)
    income_entry = Entry(main_frame, font=LARGE_FONT)
    income_entry.pack(pady=5)

    proceed_button = Button(main_frame, text="Proceed", font=BUTTON_FONT, command=process_setup)
    proceed_button.pack(pady=20)

def process_setup():
    global user_name, monthly_income, income_var
    
    user_name_input = user_name_entry.get().strip()
    income_input = income_entry.get().strip()
    
    if not user_name_input.replace(" ", "").isalpha():
        messagebox.showwarning("Invalid Input", "Warning: Please enter a valid name. It should not contain numbers.")
        return
    
    try:
        monthly_income = float(income_input)
    except ValueError:
        messagebox.showwarning("Invalid Input", "Invalid input. Please enter a valid number for monthly income.")
        return

    user_name = user_name_input
    
    if user_name in monthly_spending_database:
        messagebox.showinfo("Welcome Back", f"Welcome back, {user_name}! Loading your previous data.")
    else:
        messagebox.showinfo("New Profile", f"Hello, {user_name}! A new profile has been created for you.")
        monthly_spending_database[user_name] = {}
        
    income_var = StringVar(value=str(monthly_income))
    
    show_main_menu()

setup_screen()
window.mainloop()