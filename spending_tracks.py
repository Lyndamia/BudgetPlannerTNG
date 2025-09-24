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