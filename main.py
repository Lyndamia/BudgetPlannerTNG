import tkinter as tk
from tkinter import *
from tkinter import messagebox
import datetime
import data_manager

window = tk.Tk()
window.title('TnG Budget Planner')
window.geometry('500x500')
canvas = tk.Canvas(window)

scroll = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll.set)
scroll.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

main_frame = tk.Frame(canvas)
canvas.create_window((0,0), window=main_frame, anchor='nw')

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
main_frame.bind('<Configure>', on_frame_configure)

custom_data = []
editable_list = []
monthly_income = 0.0
user_name = ""
monthly_spending_database = data_manager.load_data()
income_var = None 

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
    standard_label = Label(main_frame, text=f'\nSuggested Spending Limit (Standard Plan)\n\n1. Needs (50%): RM{formula(needs)}\n2. Wants (30%): RM{formula(wants)}\n3. Savings (20%): RM{formula(savings)}')
    standard_label.pack()

def aggressive_func(standard, aggressive, choose_type_text):
    choose_button_hide_2(choose_type_text, standard, aggressive)
    needs = 40
    wants = 20
    savings = 40
    standard_label = Label(main_frame, text=f'\nSuggested Spending Limit (Aggressive Plan)\n\n1. Needs (40%): RM{formula(needs)}\n2. Wants (20%): RM{formula(wants)}\n3. Savings (40%): RM{formula(savings)}')
    standard_label.pack()

def plan_1(premade, custom, choose_plan_text):
    choose_button_hide_1(choose_plan_text, premade, custom)
    choose_type_text = Label(main_frame, text = '\nThere are two plans;')
    standard = tk.Button(main_frame, text='Standard Plan', command=lambda:standard_func(standard, aggressive, choose_type_text))
    aggressive = tk.Button(main_frame, text='Aggressive Plan', command=lambda:aggressive_func(standard, aggressive, choose_type_text))
    choose_type_text.pack()
    standard.pack()
    aggressive.pack()

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

def add_func():
    group = tk.Frame(main_frame)
    group.pack()

    category_label = Label(group, text='Category:')
    category_var = StringVar()
    category_input = Entry(group, textvariable=category_var)
    category_label.pack()
    category_input.pack()

    percent_label = Label(group, text='Percentage:')
    percent_var = StringVar()
    percent_input = Spinbox(group, from_=1, to=100, increment=10, textvariable=percent_var)
    percent_label.pack()
    percent_input.pack()

    delete = tk.Button(group, text='Delete Category', command=lambda:delete_func(group, data_entry))
    delete.pack()

    data_entry = {
        'category':category_var,
        'percent':percent_var,
        'group':group
    }
    custom_data.append(data_entry)

def edit_func(container, edit, confirm):
    for custom_categories in editable_list:
        custom_categories.destroy()
    editable_list.clear()

    confirm.pack_forget()
    edit.pack_forget()

    container.pack()
    for data_entry in custom_data:
        data_entry['group'].pack()

def confirm_func(confirm, edit):
    spending_limit = Label(main_frame, text='\nSuggested spending limit:\n')
    spending_limit.pack()

    for custom_categories in editable_list:
        custom_categories.destroy()
    editable_list.clear()

    for data_entry in custom_data:
        category = data_entry['category'].get()
        percent = data_entry['percent'].get()
        value = formula(percent)
        custom_categories = Label(main_frame, text=f'- {category} ({percent}%): RM{value}')
        custom_categories.pack()
        editable_list.append(custom_categories)

    confirm.pack_forget()
    edit.pack_forget()

def save_func(container):
    current_percentage = count_percentage()
    if current_percentage > 100:
        messagebox.showwarning("Percentage Inconsistency", "Total percentage exceeds 100%. Please edit.")
        return
    if current_percentage < 100:
        messagebox.showwarning("Percentage Inconsistency", "Total percentage does not reach 100%. Please edit.")
        return
    
    container.pack_forget()

    for data_entry in custom_data:
        data_entry['group'].pack_forget()
        category = data_entry['category'].get()
        percent = data_entry['percent'].get()
        custom_categories = Label(main_frame, text=f'- {category}: {percent}%')
        custom_categories.pack()
        editable_list.append(custom_categories)
    
    edit = tk.Button(main_frame, text='Edit', command=lambda:edit_func(container, edit, confirm))
    edit.pack()

    confirm = tk.Button(main_frame, text='Confirm', command=lambda:confirm_func(confirm, edit))
    confirm.pack()

def plan_2(premade, custom, choose_plan_text):
    choose_button_hide_1(choose_plan_text, premade, custom)
    container = tk.Frame(main_frame)
    container.pack()
    add = tk.Button(container, text='Add Category', command=add_func)
    add.pack()

    save = tk.Button(container, text='Save', command=lambda:save_func(container))
    save.pack()

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
    choose_plan_text = Label(main_frame, text = '\nHow would you like to allocate your savings?')
    premade = tk.Button(main_frame, text='Use our ready made plan', command=lambda:plan_1(premade, custom, choose_plan_text))
    custom = tk.Button(main_frame, text='Create your own custom plan', command=lambda:plan_2(premade, custom, choose_plan_text))
    choose_plan_text.pack()
    premade.pack()
    custom.pack()

def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def show_main_menu():
    clear_frame()
    
    main_menu_label = Label(main_frame, text="\n---> Main Menu <---")
    main_menu_label.pack()

    btn_budget_plan = Button(main_frame, text="1. See Budget Plan", command=show_budget_plan)
    btn_budget_plan.pack()

    btn_track_spending = Button(main_frame, text="2. Track Wants Spending (for 7 days)", command=show_spending_tracker)
    btn_track_spending.pack()

    btn_data_management = Button(main_frame, text="3. See Monthly Data Management", command=show_data_management)
    btn_data_management.pack()

    btn_budget_suggestion = Button(main_frame, text="4. Get Budget Suggestion", command=get_suggestion)
    btn_budget_suggestion.pack()

    btn_exit = Button(main_frame, text="5. Exit", command=window.quit)
    btn_exit.pack()

def show_budget_plan():
    clear_frame()
    
    title_label = Label(main_frame, text = '\nTnG Budget Planner')
    title_label.pack()
    
    income_label = Label(main_frame, text = f'Monthly Income: RM {monthly_income:.2f}')
    income_label.pack()
    
    next_button = tk.Button(main_frame, text='Next', command=lambda:next_func(next_button))
    next_button.pack()
    
    back_button = Button(main_frame, text="Back to Main Menu", command=show_main_menu)
    back_button.pack()

def show_spending_tracker():
    clear_frame()
    spending_tracker_label = Label(main_frame, text="Daily Spending Tracker Goes Here...")
    spending_tracker_label.pack()
    
    back_button = Button(main_frame, text="Back to Main Menu", command=show_main_menu)
    back_button.pack()

def show_data_management():
    clear_frame()
    data_manager.display_data(monthly_spending_database, user_name,  main_frame)
    back_button = Button(main_frame, text="Back to Main Menu", command=show_main_menu)
    back_button.pack()

def get_suggestion():
    clear_frame()
    data_manager.get_budget_suggestion(monthly_spending_database, user_name,  main_frame)
    back_button = Button(main_frame, text="Back to Main Menu", command=show_main_menu)
    back_button.pack()

def setup_screen():
    clear_frame()
    
    global user_name_entry, income_entry

    welcome_label = Label(main_frame, text="\nWelcome to the Budget Planner!")
    welcome_label.pack()
    
    name_label = Label(main_frame, text="Please enter your username:")
    name_label.pack()
    user_name_entry = Entry(main_frame)
    user_name_entry.pack()
    
    income_label = Label(main_frame, text="Enter your monthly income:")
    income_label.pack()
    income_entry = Entry(main_frame)
    income_entry.pack()

    proceed_button = Button(main_frame, text="Proceed", command=process_setup)
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