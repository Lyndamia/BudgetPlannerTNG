import tkinter as tk
from tkinter import *

window = tk.Tk()
window.title('TnG Budget Planner')
window.geometry('500x500')
# need to add scrollbar !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
custom_data = []
editable_list = []

title_label = Label(window, text = '\nTnG Budget Planner')
title_label.pack()

income_label = Label(window, text = '\nMonthly Income: RM')
income_var = StringVar()
income_input = Entry(window, textvariable=income_var, validate='key')
income_label.pack()
income_input.pack()

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
    standard_label = Label(window, text=f'\nStandard Plan\n\n1. Needs (50%): RM{formula(needs)}\n2. Wants (30%): RM{formula(wants)}\n3. Savings (20%): RM{formula(savings)}')
    standard_label.pack()

def aggressive_func(standard, aggressive, choose_type_text):
    choose_button_hide_2(choose_type_text, standard, aggressive)
    needs = 40
    wants = 20
    savings = 40
    standard_label = Label(window, text=f'\nAggressive Plan\n\n1. Needs (40%): RM{formula(needs)}\n2. Wants (20%): RM{formula(wants)}\n3. Savings (40%): RM{formula(savings)}')
    standard_label.pack()

def plan_1(premade, custom, choose_plan_text):
    choose_button_hide_1(choose_plan_text, premade, custom)
    choose_type_text = Label(window, text = '\nThere are two plans;')
    standard = tk.Button(window, text='Standard Plan', command=lambda:standard_func(standard, aggressive, choose_type_text))
    aggressive = tk.Button(window, text='Aggressive Plan', command=lambda:aggressive_func(standard, aggressive, choose_type_text))
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
        total_percentage += int(data_entry['percent'].get())
    return total_percentage

def add_func():
    group = tk.Frame(window)
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

def confirm_func():
    for data_entry in custom_data:
        category = data_entry['category'].get()
        percent = data_entry['percent'].get()
        value = formula(percent)
        custom_categories = Label(window, text=f'- {category} ({percent}%): RM{value}')
        custom_categories.pack()
        editable_list.append(custom_categories)

def save_func(container):
    current_percentage = count_percentage()
    if current_percentage > 100:
        print(current_percentage)
        Message(window, text='Total percentage exceeds 100%. Please edit.').pack()
        return #need to remove message after another button clicked !!!!!!!!!!!!!!!!!!!!!!!!!!
    if current_percentage < 100:
        print(current_percentage)
        Message(window, text='Total percentage does not reach 100%. Please edit.').pack()
        return #need to remove message after another button clicked !!!!!!!!!!!!!!!!!!!!!!!!!!
    
    container.pack_forget()

    for data_entry in custom_data:
        data_entry['group'].pack_forget()
        category = data_entry['category'].get()
        percent = data_entry['percent'].get()
        custom_categories = Label(window, text=f'- {category}: {percent}%')
        custom_categories.pack()
        editable_list.append(custom_categories)
    
    edit = tk.Button(window, text='Edit', command=lambda:edit_func(container, edit, confirm))
    edit.pack()

    confirm = tk.Button(window, text='Confirm', command=confirm_func)
    confirm.pack()

def plan_2(premade, custom, choose_plan_text):
    choose_button_hide_1(choose_plan_text, premade, custom)
    container = tk.Frame(window)
    container.pack()
    add = tk.Button(container, text='Add Category', command=add_func)
    add.pack() # need to make the button be on the side !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
    choose_plan_text = Label(window, text = '\nHow would you like to allocate your savings?')
    premade = tk.Button(window, text='Use our ready made plan', command=lambda:plan_1(premade, custom, choose_plan_text))
    custom = tk.Button(window, text='Create your own custom plan', command=lambda:plan_2(premade, custom, choose_plan_text))
    choose_plan_text.pack()
    premade.pack()
    custom.pack()

next_button = tk.Button(window, text='Next', command=lambda:next_func(next_button))
next_button.pack()

window.mainloop()