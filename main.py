"""
Main CLI for Smart Budget and Inventory Manager
Handles user login/registration and main menu navigation
"""

from database import db
from expense_tracker import ExpenseTracker
from inventory_manager import InventoryManager
from reports import Reports
import getpass

APP_NAME = "Smart Budget and Inventory Manager"

# --- User Authentication ---
def register():
    print("\nREGISTER NEW USER")
    while True:
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
        if db.user_exists(username):
            print("Username already exists. Try another.")
            continue
        password = getpass.getpass("Enter password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords do not match.")
            continue
        if db.create_user(username, password):
            print("✓ Registration successful! You can now log in.")
            break
        else:
            print("✗ Registration failed. Try again.")


def login():
    print("\nLOGIN")
    for _ in range(3):
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")
        user = db.validate_user(username, password)
        if user:
            print(f"\nWelcome, {user['username']}!")
            return user['id']
        else:
            print("Invalid credentials. Try again.")
    print("Too many failed attempts. Exiting.")
    return None

# --- Main Menu ---
def main_menu(user_id):
    expense_tracker = ExpenseTracker(user_id)
    inventory_manager = InventoryManager(user_id)
    reports = Reports(user_id)
    while True:
        print("\n" + "="*50)
        print(f"{APP_NAME} - Main Menu")
        print("="*50)
        print("1. Expense Tracker")
        print("2. Product Inventory Manager")
        print("3. Reports")
        print("4. Logout")
        choice = input("Select an option: ").strip()
        if choice == '1':
            expense_menu(expense_tracker)
        elif choice == '2':
            inventory_menu(inventory_manager)
        elif choice == '3':
            reports_menu(reports)
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

# --- Expense Tracker Menu ---
def expense_menu(expense_tracker):
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Delete Expense")
        print("4. Filter Expenses")
        print("5. Back to Main Menu")
        choice = input("Select an option: ").strip()
        if choice == '1':
            expense_tracker.add_expense()
        elif choice == '2':
            expense_tracker.view_expenses()
        elif choice == '3':
            expense_tracker.delete_expense()
        elif choice == '4':
            expense_tracker.filter_expenses()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.")

# --- Inventory Manager Menu ---
def inventory_menu(inventory_manager):
    while True:
        print("\nProduct Inventory Menu")
        print("1. Add Product")
        print("2. View Products")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Simulate Purchase")
        print("6. Back to Main Menu")
        choice = input("Select an option: ").strip()
        if choice == '1':
            inventory_manager.add_product()
        elif choice == '2':
            inventory_manager.view_products()
        elif choice == '3':
            inventory_manager.edit_product()
        elif choice == '4':
            inventory_manager.delete_product()
        elif choice == '5':
            inventory_manager.simulate_purchase()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Try again.")

# --- Reports Menu ---
def reports_menu(reports):
    while True:
        print("\nReports Menu")
        print("1. Monthly Total Expenses")
        print("2. Products Low in Stock")
        print("3. Total Inventory Value")
        print("4. Back to Main Menu")
        choice = input("Select an option: ").strip()
        if choice == '1':
            reports.monthly_expenses()
        elif choice == '2':
            reports.low_stock_products()
        elif choice == '3':
            reports.total_inventory_value()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

# --- Entry Point ---
def main():
    print("="*60)
    print(f"{APP_NAME}")
    print("="*60)
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select an option: ").strip()
        if choice == '1':
            user_id = login()
            if user_id:
                main_menu(user_id)
        elif choice == '2':
            register()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main() 