import tkinter as tk
from tkinter import messagebox
from auth import register_user, login_user
from db import init_database
from expense_manager import ExpenseManager
from product_manager import ProductManager
from reports import ReportsManager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense & Product Manager")
        self.user_id = None
        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()
        
        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            success, result = login_user(username, password)
            if success:
                self.user_id = result
                self.show_main_menu()
            else:
                messagebox.showerror("Login Failed", result)
        
        tk.Button(self.root, text="Login", command=do_login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.show_register).pack()

    def show_register(self):
        self.clear_window()
        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()
        
        def do_register():
            username = username_entry.get()
            password = password_entry.get()
            success, msg = register_user(username, password)
            if success:
                messagebox.showinfo("Success", msg)
                self.show_login()
            else:
                messagebox.showerror("Error", msg)
        
        tk.Button(self.root, text="Register", command=do_register).pack(pady=5)
        tk.Button(self.root, text="Back to Login", command=self.show_login).pack()

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Main Menu", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Manage Expenses", width=25, command=self.open_expense_manager).pack(pady=5)
        tk.Button(self.root, text="Manage Products", width=25, command=self.open_product_manager).pack(pady=5)
        tk.Button(self.root, text="View Reports", width=25, command=self.open_reports).pack(pady=5)
        tk.Button(self.root, text="Logout", width=25, command=self.logout).pack(pady=5)

    def open_expense_manager(self):
        ExpenseManager(self.user_id)

    def open_product_manager(self):
        ProductManager(self.user_id)

    def open_reports(self):
        ReportsManager(self.user_id)

    def logout(self):
        self.user_id = None
        self.show_login()

if __name__ == "__main__":
    init_database()
    root = tk.Tk()
    app = App(root)
    root.mainloop() 