import tkinter as tk
from tkinter import *
from tkinter import messagebox
from datetime import date, datetime
import data_manager
import spending_tracks

window = tk.Tk()
window.title('TnG Budget Planner')
window.geometry('500x500')

main_frame = tk.Frame(window)
main_frame.pack(fill=BOTH, expand=True)

# Global variable
custom_data = []
display_list = []
monthly_income = 0.0
user_name = ""
monthly_spending_database = data_manager.load_data()
income_var = None
budget_dict = {}  # Make budget_dict a global variable with an initial empty dictionary.
has_plan = False
track_button = None

# Font
LARGE_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 12)

# Function Budgetplanner
def formula(percent):
    percent = float(percent)
    income = float(income_var.get())
    rm = (percent/100)*income
    return round(rm, 2)

def standard_func(standard, aggressive, choose_type_text):
    global has_plan, budget_dict, track_button
    choose_button_hide_2(choose_type_text, standard, aggressive)
    needs = 50
    wants = 30
    savings = 20
    standard_label = Label(main_frame, text=f'\nSuggested Spending Limit (Standard Plan)\n\n1. Needs (50%): RM{formula(needs)}\n2. Wants (30%): RM{formula(wants)}\n3. Savings (20%): RM{formula(savings)}', font=LARGE_FONT)
    standard_label.pack(pady=10)
    budget_dict = {
        'Needs':formula(needs),
        'Wants':formula(wants),
        'Savings':formula(savings)
    }
    print(budget_dict)

    has_plan = True

    track_button = tk.Button(main_frame, text='Track your spending', font=BUTTON_FONT, command=lambda:track_func(budget_dict, has_plan))
    track_button.pack(pady=5)

def aggressive_func(standard, aggressive, choose_type_text):
    global has_plan, budget_dict, track_button
    choose_button_hide_2(choose_type_text, standard, aggressive)
    needs = 40
    wants = 20
    savings = 40
    standard_label = Label(main_frame, text=f'\nSuggested Spending Limit (Aggressive Plan)\n\n1. Needs (40%): RM{formula(needs)}\n2. Wants (20%): RM{formula(wants)}\n3. Savings (40%): RM{formula(savings)}', font=LARGE_FONT)
    standard_label.pack(pady=10)
    budget_dict = {
        'Needs':formula(needs),
        'Wants':formula(wants),
        'Savings':formula(savings)
    }
    print(budget_dict)

    has_plan = True

    track_button = tk.Button(main_frame, text='Track your spending', font=BUTTON_FONT, command=lambda:track_func(budget_dict, has_plan))
    track_button.pack(padx=5)

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
    for custom_categories in display_list:
        custom_categories.destroy()
    display_list.clear()

    confirm.pack_forget()
    edit.pack_forget()

    canvas_container.pack(fill="both", expand=True)
    for data_entry in custom_data:
        data_entry['group'].pack()
    
    # Update the scroll region after adding widgets
    canvas_container.update_idletasks()
    canvas_container.configure(scrollregion=canvas_container.bbox("all"))

def confirm_func(confirm, edit, canvas_container):
    global has_plan, budget_dict, track_button
    spending_limit = Label(main_frame, text='\nSuggested spending limit:\n', font=LARGE_FONT)
    spending_limit.pack(pady=5)

    for custom_categories in display_list:
        custom_categories.destroy()
    display_list.clear()

    budget_dict = {}
    for data_entry in custom_data:
        category = data_entry['category'].get()
        percent = data_entry['percent'].get()
        rm = formula(percent)
        custom_categories = Label(main_frame, text=f'- {category} ({percent}%): RM{rm}', font=LARGE_FONT)
        custom_categories.pack()
        budget_dict[category] = rm

    print(budget_dict)
    confirm.pack_forget()
    edit.pack_forget()
    canvas_container.pack_forget()
    
    has_plan = True

    track_button = tk.Button(main_frame, text='Track your spending', font=BUTTON_FONT, command=lambda:track_func(budget_dict, has_plan))
    track_button.pack(pady=5)

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
        display_list.append(custom_categories)
    
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

# Function Spending tracks after Budgetplanner
def compare_func(budget_dict, spending_dict):
    total = 0
    for key in budget_dict:
        budget = float(budget_dict[key])
        spent_entry = spending_dict.get(key)
        spent = float(spent_entry.get())
        total += spent

        if spent > budget:
            over = spent - budget
            warn_label = Label(main_frame, text=f"\nYou exceeded the recommended limit for {key} by RM{over}!", font=LARGE_FONT)
            warn_label.pack()
        elif spent == budget:
            warn_label = Label(main_frame, text=f"\nYou have reached the recommended limit for {key} of RM{budget}!", font=LARGE_FONT)
            warn_label.pack()
        elif spent < budget:
            remain = budget - spent
            warn_label = Label(main_frame, text=f"\nYou are still within the recommended limit for {key}! You have RM{remain} remaining.", font=LARGE_FONT)
            warn_label.pack()
        
    if total > float(income_var.get()):
        deficit = total - float(income_var.get())
        msg_label = Label(main_frame, text=f"\nBad news! You spent RM{deficit} more than what you earn!", font=LARGE_FONT)
        msg_label.pack()
    elif total == float(income_var.get()):
        msg_label = Label(main_frame, text=f"\nYou used up all {income_var.get()} of your earnings!", font=LARGE_FONT)
        msg_label.pack()
    elif total < float(income_var.get()):
        surplus = float(income_var.get()) - total
        msg_label = Label(main_frame, text=f"\nGood news! You have a surplus of RM{surplus}!", font=LARGE_FONT)
        msg_label.pack()

def track_func(budget_dict, has_plan):
    if not has_plan:
        messagebox.showwarning("No Budget Plan", "You do not have a budget plan yet. Please create a plan first.")
        return
    
    #plan_button.destroy()
    if track_button:
        track_button.destroy()

    now = datetime.now()
    month = now.strftime("%B")
    today_date = date.today()
    date_label = Label(main_frame, text=f"\n{month}'s Spendings as of {today_date}\n", font=LARGE_FONT)
    date_label.pack()

    spending_dict = {}
    for key in budget_dict:
        spent_var = StringVar()
        spent_label = Label(main_frame, text=f"Money spent for {key}:", font=LARGE_FONT)
        spent_entry = Entry(main_frame, textvariable=spent_var, font=LARGE_FONT)
        spent_label.pack()
        spent_entry.pack()
        spending_dict[key] = spent_entry
    
    compare_button = tk.Button(main_frame, text='Generate summary', font=BUTTON_FONT, command=lambda:compare_func(budget_dict, spending_dict))
    compare_button.pack(padx=5)

# Main menu Function
def show_main_menu():
    data_manager.clear_frame(main_frame)

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

    btn_track_spending = Button(main_frame, text="2. Track Spending", font=BUTTON_FONT, command=show_spending_tracker)
    btn_track_spending.pack(pady=5)

    btn_data_management = Button(main_frame, text="3. See Monthly Data Management", font=BUTTON_FONT, command=show_data_management)
    btn_data_management.pack(pady=5)

    btn_budget_suggestion = Button(main_frame, text="4. Get Budget Suggestion", font=BUTTON_FONT, command=get_suggestion)
    btn_budget_suggestion.pack(pady=5)

    btn_exit = Button(main_frame, text="5. Exit", font=BUTTON_FONT, command=window.quit)
    btn_exit.pack(pady=5)

# Called from Main Menu
def show_budget_plan():
    data_manager.clear_frame(main_frame)
    
    title_label = Label(main_frame, text='\nTnG Budget Planner', font=LARGE_FONT)
    title_label.pack(pady=10)
    
    income_label = Label(main_frame, text=f'Monthly Income: RM {monthly_income:.2f}', font=LARGE_FONT)
    income_label.pack(pady=5)
    
    next_button = tk.Button(main_frame, text='Next', font=BUTTON_FONT, command=lambda:next_func(next_button))
    next_button.pack(pady=5)
    
    back_button = Button(main_frame, text="Back to Main Menu", font=BUTTON_FONT, command=show_main_menu)
    back_button.pack(pady=10)

def show_spending_tracker():
    data_manager.clear_frame(main_frame)
    global budget_dict
    
    if not budget_dict:
        messagebox.showwarning("No Budget Plan", "You do not have a budget plan yet. Please create a plan first.")
        show_main_menu()
        return
    
    spending_tracks.show_spending_tracker(main_frame, user_name, monthly_spending_database, budget_dict, show_main_menu)

def show_data_management():
    data_manager.clear_frame(main_frame)
    data_manager.display_data(monthly_spending_database, user_name, main_frame)
    back_button = Button(main_frame, text="Back to Main Menu", font=BUTTON_FONT, command=show_main_menu)
    back_button.pack(pady=10)

def get_suggestion():
    data_manager.clear_frame(main_frame)
    data_manager.get_budget_suggestion(monthly_spending_database, user_name, main_frame)
    back_button = Button(main_frame, text="Back to Main Menu", font=BUTTON_FONT, command=show_main_menu)
    back_button.pack(pady=10)

# Initial setup screen
def setup_screen():
    data_manager.clear_frame(main_frame)

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