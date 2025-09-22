import datetime
import budget_planner
import data_manager

def main():
    try:

        print("\nWelcome to the Budget Planner!")
        
        while True:
            user_name = input("Please enter your username: ")
            if user_name.replace(" ", "").isalpha():
                break 
            else:
                print("\nWarning: Please enter a valid name. It should not contain numbers.")
        
        monthly_income = float(input("Enter your monthly income: "))
        
    except ValueError:
        print("Invalid input. Please enter a valid number for monthly income.")

if __name__ == "__main__":
    main()