import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from db import create_connection
from database import db

class ReportsManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.window = tk.Toplevel()
        self.window.title("Reports")
        self.window.geometry("800x600")
        self.setup_ui()

    def setup_ui(self):
        # Report Options Frame
        options_frame = tk.LabelFrame(self.window, text="Report Options", padx=10, pady=10)
        options_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(options_frame, text="Expense Summary", command=self.show_expense_summary).pack(side="left", padx=5)
        tk.Button(options_frame, text="Category Breakdown", command=self.show_category_breakdown).pack(side="left", padx=5)
        tk.Button(options_frame, text="Product Inventory", command=self.show_product_inventory).pack(side="left", padx=5)
        tk.Button(options_frame, text="Monthly Spending", command=self.show_monthly_spending).pack(side="left", padx=5)

        # Display Frame
        self.display_frame = tk.Frame(self.window)
        self.display_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def clear_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    def show_expense_summary(self):
        self.clear_display()
        
        try:
            connection = create_connection()
            cursor = connection.cursor()
            
            # Total expenses
            cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (self.user_id,))
            total = cursor.fetchone()[0] or 0
            
            # Today's expenses
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date = ?", (self.user_id, today))
            today_total = cursor.fetchone()[0] or 0
            
            # This month's expenses
            month_start = datetime.now().replace(day=1).strftime("%Y-%m-%d")
            cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND date >= ?", (self.user_id, month_start))
            month_total = cursor.fetchone()[0] or 0
            
            connection.close()
            
            # Display summary
            summary_text = f"""
            EXPENSE SUMMARY
            
            Total Expenses: ${total:.2f}
            Today's Expenses: ${today_total:.2f}
            This Month's Expenses: ${month_total:.2f}
            """
            
            label = tk.Label(self.display_frame, text=summary_text, font=("Arial", 12), justify="left")
            label.pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load expense summary: {str(e)}")

    def show_category_breakdown(self):
        self.clear_display()
        
        try:
            connection = create_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT category, SUM(amount) as total 
                FROM expenses 
                WHERE user_id = ? 
                GROUP BY category 
                ORDER BY total DESC
            """, (self.user_id,))
            
            data = cursor.fetchall()
            connection.close()
            
            if data:
                # Create pie chart
                fig, ax = plt.subplots(figsize=(8, 6))
                categories = [row[0] for row in data]
                amounts = [row[1] for row in data]
                
                ax.pie(amounts, labels=categories, autopct='%1.1f%%')
                ax.set_title('Expense Breakdown by Category')
                
                canvas = FigureCanvasTkAgg(fig, self.display_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                
            else:
                tk.Label(self.display_frame, text="No expense data available", font=("Arial", 12)).pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load category breakdown: {str(e)}")

    def show_product_inventory(self):
        self.clear_display()
        
        try:
            connection = create_connection()
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT name, category, price, stock 
                FROM products 
                WHERE user_id = ? 
                ORDER BY stock ASC
            """, (self.user_id,))
            
            products = cursor.fetchall()
            connection.close()
            
            if products:
                # Create treeview
                columns = ("Name", "Category", "Price", "Stock", "Total Value")
                tree = ttk.Treeview(self.display_frame, columns=columns, show="headings")
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=120)
                
                total_inventory_value = 0
                for product in products:
                    name, category, price, stock = product
                    total_value = price * stock
                    total_inventory_value += total_value
                    tree.insert("", "end", values=(name, category, f"${price:.2f}", stock, f"${total_value:.2f}"))
                
                tree.pack(fill="both", expand=True)
                
                # Summary
                summary = tk.Label(self.display_frame, 
                                 text=f"Total Inventory Value: ${total_inventory_value:.2f}", 
                                 font=("Arial", 12, "bold"))
                summary.pack(pady=10)
                
            else:
                tk.Label(self.display_frame, text="No products available", font=("Arial", 12)).pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load product inventory: {str(e)}")

    def show_monthly_spending(self):
        self.clear_display()
        
        try:
            connection = create_connection()
            cursor = connection.cursor()
            
            # Get last 6 months of data
            months = []
            amounts = []
            
            for i in range(6):
                date = datetime.now() - timedelta(days=30*i)
                month_start = date.replace(day=1).strftime("%Y-%m-%d")
                month_end = (date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                month_end = month_end.strftime("%Y-%m-%d")
                
                cursor.execute("""
                    SELECT SUM(amount) 
                    FROM expenses 
                    WHERE user_id = ? AND date BETWEEN ? AND ?
                """, (self.user_id, month_start, month_end))
                
                total = cursor.fetchone()[0] or 0
                months.append(date.strftime("%b %Y"))
                amounts.append(total)
            
            connection.close()
            
            if any(amounts):
                # Create bar chart
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(months, amounts)
                ax.set_title('Monthly Spending')
                ax.set_ylabel('Amount ($)')
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                canvas = FigureCanvasTkAgg(fig, self.display_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                
            else:
                tk.Label(self.display_frame, text="No spending data available", font=("Arial", 12)).pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load monthly spending: {str(e)}")

class Reports:
    def __init__(self, user_id):
        self.user_id = user_id

    def monthly_expenses(self):
        """Show total expenses for the current month"""
        year_month = datetime.now().strftime("%Y-%m")
        query = """
            SELECT SUM(amount) as total
            FROM expenses
            WHERE user_id = %s AND DATE_FORMAT(date, '%%Y-%%m') = %s
        """
        result = db.execute_query(query, (self.user_id, year_month))
        total = result[0]['total'] if result and result[0]['total'] else 0
        print(f"\nTotal expenses for {year_month}: ${total:.2f}")

    def low_stock_products(self, threshold=5):
        """Show products low in stock (default threshold: 5)"""
        query = """
            SELECT name, stock
            FROM products
            WHERE user_id = %s AND stock <= %s
            ORDER BY stock ASC
        """
        products = db.execute_query(query, (self.user_id, threshold))
        print(f"\nProducts low in stock (≤ {threshold}):")
        if not products:
            print("All products are sufficiently stocked.")
            return
        for prod in products:
            print(f"- {prod['name']}: {prod['stock']} left")

    def total_inventory_value(self):
        """Show total value of all products in inventory"""
        query = """
            SELECT SUM(price * stock) as total_value
            FROM products
            WHERE user_id = %s
        """
        result = db.execute_query(query, (self.user_id,))
        total_value = result[0]['total_value'] if result and result[0]['total_value'] else 0
        print(f"\nTotal inventory value: ${total_value:.2f}") 