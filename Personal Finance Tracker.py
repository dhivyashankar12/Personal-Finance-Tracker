import os
import csv
import getpass
import warnings
from datetime import datetime
import schedule
import time
from plyer import notification

warnings.filterwarnings("ignore", category=UserWarning)

# Define file paths for income, expenses, and bill reminders
income_file = "income.csv"
expenses_file = "expenses.csv"
reminders_file = "reminders.csv"  # New file for bill reminders

# Function to create a new user profile
def create_user_profile(username, password):
    user_dir = os.path.join("user_profiles", username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
        with open(os.path.join(user_dir, "pin.txt"), "w") as pin_file:
            pin_file.write(password)
        # Create user-specific data files (income, expenses, etc.)
        with open(os.path.join(user_dir, "income.csv"), "w", newline="") as f:
            pass
        with open(os.path.join(user_dir, "expenses.csv"), "w", newline="") as f:
            pass
        with open(os.path.join(user_dir, "reminders.csv"), "w", newline="") as f:
            pass
        return True
    return False

# Function to authenticate users
def authenticate_user(username, password):
    user_dir = os.path.join("user_profiles", username)
    if os.path.exists(user_dir):
        with open(os.path.join(user_dir, "pin.txt"), "r") as pin_file:
            saved_password = pin_file.read()
        return password == saved_password
    return False

# Function to get the user's data directory
def get_user_data_directory(username):
    return os.path.join("user_profiles", username)

# Function to log income or expense
def log_transaction(file_path, category, amount):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount])

# Function to display transactions
def display_transactions(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            header = next(reader)  # Read the header row
            if header:
                print("\t".join(header))
            total_amount = 0
            for row in reader:
                if row and row[2]:  # Check if the row and the third column are not empty
                    try:
                        total_amount += float(row[2])
                        print("\t".join(row))
                    except ValueError:
                        print("Error: Invalid amount found in the transaction.")
            print(f"Total Amount: {total_amount}")
    else:
        print("No transactions found.")

# Function to add a bill reminder
def add_reminder(name, due_date, amount):
    with open(reminders_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, due_date, amount])

# Function to list bill reminders
def list_reminders():
    if os.path.exists(reminders_file):
        with open(reminders_file, "r") as f:
            reader = csv.reader(f)
            header = ["Name", "Due Date", "Amount"]
            print("\t".join(header))
            for row in reader:
                print("\t".join(row))
    else:
        print("No bill reminders found.")

# Function to set alert frequency
def set_alert_frequency():
    print("\nSet Alert Frequency")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")

    frequency_choice = input("Select your preferred alert frequency: ")

    # Update the user's alert frequency preference in your application's settings
    if frequency_choice == '1':
        # Set the alert frequency to daily
        print("Alert frequency set to Daily.")
        # Update the user's settings accordingly
    elif frequency_choice == '2':
        # Set the alert frequency to weekly
        print("Alert frequency set to Weekly.")
        # Update the user's settings accordingly
    elif frequency_choice == '3':
        # Set the alert frequency to monthly
        print("Alert frequency set to Monthly.")
        # Update the user's settings accordingly
    else:
        print("Invalid choice. Please select a valid alert frequency.")

    # Schedule alerts based on the chosen frequency
    if frequency_choice == '1':
        # Set daily alerts
        schedule.every(1).day.at("09:00").do(send_alert)
    elif frequency_choice == '2':
        # Set weekly alerts on Mondays at 09:00 AM
        schedule.every().monday.at("09:00").do(send_alert)
    elif frequency_choice == '3':
        # Set monthly alerts on the 1st day of the month at 09:00 AM
        schedule.every(1).month.at("09:00").do(send_alert)
    else:
        print("Invalid choice. Please select a valid alert frequency.")

def send_alert():
    # Implement logic to check for pending expenses or financial events
    # If an event is pending, send a notification
    notification_title = "Financial Reminder"
    notification_message = "You have pending expenses to review."
    notification.notify(
        title=notification_title,
        message=notification_message,
        app_name="Personal Finance Tracker",
    )

def main():
    # Configure the alert frequency here (e.g., daily, weekly, monthly)
    alert_frequency = "weekly"

    # Schedule alerts based on the chosen frequency
    if alert_frequency == "daily":
        schedule.every().day.at("09:00").do(send_alert, "Daily Reminder", "Don't forget to update your finances today!")

    elif alert_frequency == "weekly":
        schedule.every(7).days.at("09:00").do(send_alert, "Weekly Reminder", "It's time to review your weekly expenses!")

    elif alert_frequency == "monthly":
        schedule.every().month.at("09:00").do(send_alert, "Monthly Reminder", "Time to check your monthly financial report!")

    # Run the alert scheduler in the background
    while True:
        schedule.run_pending()
        time.sleep(60)

# Main menu
while True:
    print("\nPersonal Finance Tracker")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Select an option: ")

    if choice == '1':
        username = input("Enter a username: ")
        password = getpass.getpass("Enter a password: ")
        if create_user_profile(username, password):
            print("Registration successful. You can now log in.")
        else:
            print("Username already exists. Please choose a different one.")

    elif choice == '2':
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        if authenticate_user(username, password):
            print("Login successful. Welcome, " + username + "!")
            while True:
                user_data_directory = get_user_data_directory(username)
                print("\nPersonal Finance Tracker")
                print("1. Log Expense")
                print("2. Log Income")
                print("3. Display Expenses")
                print("4. Display Income")
                print("5. Add Bill Reminder")
                print("6. List Bill Reminders")
                print("7. Set alert frequency")
                print("8. Switch User")
                print("9. Logout")

                choice = input("Select an option: ")

                if choice == '1':
                    category = input("Enter expense category: ")
                    try:
                        amount = float(input("Enter expense amount: "))
                        log_transaction(os.path.join(user_data_directory, expenses_file), category, amount)
                        print("Expense logged successfully.")
                    except ValueError:
                        print("Invalid amount. Please enter a valid number.")

                elif choice == '2':
                    category = input("Enter income category: ")
                    try:
                        amount = float(input("Enter income amount: "))
                        log_transaction(os.path.join(user_data_directory, income_file), category, amount)
                        print("Income logged successfully.")
                    except ValueError:
                        print("Invalid amount. Please enter a valid number.")

                elif choice == '3':
                    print("\nExpense Transactions:")
                    display_transactions(os.path.join(user_data_directory, expenses_file))

                elif choice == '4':
                    print("\nIncome Transactions:")
                    display_transactions(os.path.join(user_data_directory, income_file))

                elif choice == '5':
                    name = input("Enter bill name: ")
                    due_date = input("Enter due date (YYYY-MM-DD): ")
                    amount = float(input("Enter bill amount: "))
                    add_reminder(name, due_date, amount)
                    print("Bill reminder added successfully.")

                elif choice == '6':
                    print("\nBill Reminders:")
                    list_reminders()

                elif choice == '7':
                    set_alert_frequency()

                elif choice == '8':
                    break  # Break the inner loop to switch users

                elif choice == '9':
                    print("Logging out. Goodbye!")
                    break  # Break the inner loop to log out
            
        else:
            print("Invalid login credentials. Please try again.")
            
    elif choice == '3':
        print("Exiting the Personal Finance Tracker. Goodbye!")
        break
