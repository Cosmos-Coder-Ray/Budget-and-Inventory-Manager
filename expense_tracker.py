"""
Expense Tracker Module for Smart Budget and Inventory Manager
Handles all expense-related operations including add, view, delete, and filtering
"""

from database import db
from datetime import datetime, timedelta
import re

class ExpenseTracker:
    def __init__(self, user_id):
        """Initialize expense tracker with user ID"""
        self.user_id = user_id
        self.categories = ['Food', 'Travel', 'Shopping', 'Bills', 'Entertainment', 'Other']
    
    def add_expense(self):
        """Add a new expense to the database"""
        print("\n" + "="*50)
        print("ADD NEW EXPENSE")
        print("="*50)
        
        # Get expense details from user
        try:
            # Date input with validation
            while True:
                date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                if not date_str:
                    date_str = datetime.now().strftime("%Y-%m-%d")
                
                if self._validate_date(date_str):
                    break
                print("Invalid date format. Please use YYYY-MM-DD")
            
            # Category selection
            print("\nAvailable categories:")
            for i, category in enumerate(self.categories, 1):
                print(f"{i}. {category}")
            
            while True:
                try:
                    cat_choice = int(input(f"\nSelect category (1-{len(self.categories)}): "))
                    if 1 <= cat_choice <= len(self.categories):
                        category = self.categories[cat_choice - 1]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Amount input with validation
            while True:
                amount_str = input("Enter amount: $").strip()
                if self._validate_amount(amount_str):
                    amount = float(amount_str)
                    break
                print("Invalid amount. Please enter a positive number.")
            
            # Description (optional)
            description = input("Enter description (optional): ").strip()
            if not description:
                description = f"{category} expense"
            
            # Insert into database
            query = """
                INSERT INTO expenses (user_id, date, category, amount, description)
                VALUES (%s, %s, %s, %s, %s)
            """
            if db.execute_query(query, (self.user_id, date_str, category, amount, description)):
                print(f"\n✓ Expense added successfully!")
                print(f"  Date: {date_str}")
                print(f"  Category: {category}")
                print(f"  Amount: ${amount:.2f}")
                print(f"  Description: {description}")
            else:
                print("\n✗ Failed to add expense. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def view_expenses(self, filter_type=None, filter_value=None):
        """View expenses with optional filtering"""
        print("\n" + "="*80)
        print("EXPENSE LIST")
        print("="*80)
        
        # Build query based on filter
        if filter_type == 'category':
            query = """
                SELECT date, category, amount, description 
                FROM expenses 
                WHERE user_id = %s AND category = %s 
                ORDER BY date DESC
            """
            params = (self.user_id, filter_value)
        elif filter_type == 'month':
            query = """
                SELECT date, category, amount, description 
                FROM expenses 
                WHERE user_id = %s AND DATE_FORMAT(date, '%%Y-%%m') = %s 
                ORDER BY date DESC
            """
            params = (self.user_id, filter_value)
        else:
            query = """
                SELECT date, category, amount, description 
                FROM expenses 
                WHERE user_id = %s 
                ORDER BY date DESC
            """
            params = (self.user_id,)
        
        expenses = db.execute_query(query, params)
        
        if not expenses:
            print("No expenses found.")
            return
        
        # Display expenses in table format
        print(f"{'Date':<12} {'Category':<15} {'Amount':<12} {'Description':<30}")
        print("-" * 80)
        
        total = 0
        for expense in expenses:
            print(f"{expense['date']:<12} {expense['category']:<15} ${expense['amount']:<11.2f} {expense['description']:<30}")
            total += expense['amount']
        
        print("-" * 80)
        print(f"{'TOTAL':<27} ${total:<11.2f}")
    
    def delete_expense(self):
        """Delete an expense by selecting from list"""
        print("\n" + "="*50)
        print("DELETE EXPENSE")
        print("="*50)
        
        # Get recent expenses for selection
        query = """
            SELECT id, date, category, amount, description 
            FROM expenses 
            WHERE user_id = %s 
            ORDER BY date DESC 
            LIMIT 10
        """
        expenses = db.execute_query(query, (self.user_id,))
        
        if not expenses:
            print("No expenses found to delete.")
            return
        
        # Display expenses for selection
        print("Recent expenses:")
        print(f"{'#':<3} {'Date':<12} {'Category':<15} {'Amount':<12} {'Description':<20}")
        print("-" * 70)
        
        for i, expense in enumerate(expenses, 1):
            print(f"{i:<3} {expense['date']:<12} {expense['category']:<15} ${expense['amount']:<11.2f} {expense['description'][:20]:<20}")
        
        # Get user selection
        try:
            choice = int(input(f"\nSelect expense to delete (1-{len(expenses)}): "))
            if 1 <= choice <= len(expenses):
                selected_expense = expenses[choice - 1]
                
                # Confirm deletion
                confirm = input(f"\nAre you sure you want to delete this expense? (y/n): ").lower()
                if confirm == 'y':
                    delete_query = "DELETE FROM expenses WHERE id = %s AND user_id = %s"
                    if db.execute_query(delete_query, (selected_expense['id'], self.user_id)):
                        print("✓ Expense deleted successfully!")
                    else:
                        print("✗ Failed to delete expense.")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
    
    def filter_expenses(self):
        """Filter expenses by category or month"""
        print("\n" + "="*50)
        print("FILTER EXPENSES")
        print("="*50)
        print("1. Filter by Category")
        print("2. Filter by Month")
        print("3. Back to main menu")
        
        try:
            choice = int(input("\nSelect option: "))
            
            if choice == 1:
                # Filter by category
                print("\nAvailable categories:")
                for i, category in enumerate(self.categories, 1):
                    print(f"{i}. {category}")
                
                cat_choice = int(input(f"\nSelect category (1-{len(self.categories)}): "))
                if 1 <= cat_choice <= len(self.categories):
                    category = self.categories[cat_choice - 1]
                    self.view_expenses('category', category)
                else:
                    print("Invalid choice.")
                    
            elif choice == 2:
                # Filter by month
                month = input("Enter month (YYYY-MM): ")
                if self._validate_month(month):
                    self.view_expenses('month', month)
                else:
                    print("Invalid month format. Use YYYY-MM")
                    
            elif choice == 3:
                return
            else:
                print("Invalid choice.")
                
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
    
    def get_monthly_total(self, year_month=None):
        """Get monthly total expenses"""
        if not year_month:
            year_month = datetime.now().strftime("%Y-%m")
        
        query = """
            SELECT SUM(amount) as total 
            FROM expenses 
            WHERE user_id = %s AND DATE_FORMAT(date, '%%Y-%%m') = %s
        """
        result = db.execute_query(query, (self.user_id, year_month))
        
        if result and result[0]['total']:
            return result[0]['total']
        return 0
    
    def _validate_date(self, date_str):
        """Validate date format"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def _validate_amount(self, amount_str):
        """Validate amount input"""
        try:
            amount = float(amount_str)
            return amount > 0
        except ValueError:
            return False
    
    def _validate_month(self, month_str):
        """Validate month format"""
        try:
            datetime.strptime(month_str, "%Y-%m")
            return True
        except ValueError:
            return False 