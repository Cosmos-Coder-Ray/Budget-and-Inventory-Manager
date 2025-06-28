import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import create_connection

class ExpenseManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.window = tk.Toplevel()
        self.window.title("Expense Manager")
        self.window.geometry("600x400")
        self.setup_ui()
        self.load_expenses()

    def setup_ui(self):
        # Add Expense Frame
        add_frame = tk.LabelFrame(self.window, text="Add New Expense", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(add_frame, text="Date:").grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(add_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(add_frame, text="Category:").grid(row=0, column=2, sticky="w")
        self.category_entry = tk.Entry(add_frame)
        self.category_entry.grid(row=0, column=3, padx=5)

        tk.Label(add_frame, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(add_frame)
        self.amount_entry.grid(row=1, column=1, padx=5)

        tk.Label(add_frame, text="Description:").grid(row=1, column=2, sticky="w")
        self.description_entry = tk.Entry(add_frame)
        self.description_entry.grid(row=1, column=3, padx=5)

        tk.Button(add_frame, text="Add Expense", command=self.add_expense).grid(row=2, column=0, columnspan=4, pady=10)

        # Expenses List
        list_frame = tk.LabelFrame(self.window, text="Expenses", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview for expenses
        columns = ("Date", "Category", "Amount", "Description")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True)
        
        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(button_frame, text="Delete Selected", command=self.delete_expense).pack(side="left", padx=5)
        tk.Button(button_frame, text="Refresh", command=self.load_expenses).pack(side="left", padx=5)

    def add_expense(self):
        try:
            date = self.date_entry.get()
            category = self.category_entry.get()
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()

            if not all([date, category, amount]):
                messagebox.showerror("Error", "Please fill all required fields")
                return

            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO expenses (user_id, date, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                (self.user_id, date, category, amount, description)
            )
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_entries()
            self.load_expenses()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")

    def load_expenses(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT date, category, amount, description FROM expenses WHERE user_id = ? ORDER BY date DESC",
                (self.user_id,)
            )
            
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            
            connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load expenses: {str(e)}")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            try:
                item = self.tree.item(selected[0])
                date, category, amount, description = item['values']

                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "DELETE FROM expenses WHERE user_id = ? AND date = ? AND category = ? AND amount = ? AND description = ?",
                    (self.user_id, date, category, amount, description)
                )
                connection.commit()
                connection.close()

                messagebox.showinfo("Success", "Expense deleted successfully!")
                self.load_expenses()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete expense: {str(e)}")

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END) 