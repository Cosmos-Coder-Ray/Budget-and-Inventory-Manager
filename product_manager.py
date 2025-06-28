import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import create_connection

class ProductManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.window = tk.Toplevel()
        self.window.title("Product Manager")
        self.window.geometry("700x500")
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        # Add Product Frame
        add_frame = tk.LabelFrame(self.window, text="Add New Product", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(add_frame)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(add_frame, text="Category:").grid(row=0, column=2, sticky="w")
        self.category_entry = tk.Entry(add_frame)
        self.category_entry.grid(row=0, column=3, padx=5)

        tk.Label(add_frame, text="Price:").grid(row=1, column=0, sticky="w")
        self.price_entry = tk.Entry(add_frame)
        self.price_entry.grid(row=1, column=1, padx=5)

        tk.Label(add_frame, text="Stock:").grid(row=1, column=2, sticky="w")
        self.stock_entry = tk.Entry(add_frame)
        self.stock_entry.grid(row=1, column=3, padx=5)

        tk.Button(add_frame, text="Add Product", command=self.add_product).grid(row=2, column=0, columnspan=4, pady=10)

        # Products List
        list_frame = tk.LabelFrame(self.window, text="Products", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview for products
        columns = ("Name", "Category", "Price", "Stock")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill="both", expand=True)
        
        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(button_frame, text="Delete Selected", command=self.delete_product).pack(side="left", padx=5)
        tk.Button(button_frame, text="Simulate Purchase", command=self.simulate_purchase).pack(side="left", padx=5)
        tk.Button(button_frame, text="Refresh", command=self.load_products).pack(side="left", padx=5)

    def add_product(self):
        try:
            name = self.name_entry.get()
            category = self.category_entry.get()
            price = float(self.price_entry.get())
            stock = int(self.stock_entry.get())

            if not all([name, category, price, stock]):
                messagebox.showerror("Error", "Please fill all required fields")
                return

            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO products (user_id, name, category, price, stock) VALUES (?, ?, ?, ?, ?)",
                (self.user_id, name, category, price, stock)
            )
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Product added successfully!")
            self.clear_entries()
            self.load_products()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid price and stock values")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")

    def load_products(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT name, category, price, stock FROM products WHERE user_id = ? ORDER BY name",
                (self.user_id,)
            )
            
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
            
            connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {str(e)}")

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            try:
                item = self.tree.item(selected[0])
                name, category, price, stock = item['values']

                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "DELETE FROM products WHERE user_id = ? AND name = ? AND category = ? AND price = ? AND stock = ?",
                    (self.user_id, name, category, price, stock)
                )
                connection.commit()
                connection.close()

                messagebox.showinfo("Success", "Product deleted successfully!")
                self.load_products()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def simulate_purchase(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to purchase")
            return

        try:
            item = self.tree.item(selected[0])
            name, category, price, stock = item['values']

            if stock <= 0:
                messagebox.showwarning("Warning", "Product is out of stock!")
                return

            quantity = tk.simpledialog.askinteger("Purchase", f"How many {name} do you want to buy?", 
                                                minvalue=1, maxvalue=stock)
            
            if quantity:
                new_stock = stock - quantity
                total_cost = price * quantity

                connection = create_connection()
                cursor = connection.cursor()
                
                # Update stock
                cursor.execute(
                    "UPDATE products SET stock = ? WHERE user_id = ? AND name = ? AND category = ? AND price = ? AND stock = ?",
                    (new_stock, self.user_id, name, category, price, stock)
                )
                
                # Add expense for the purchase
                from datetime import datetime
                cursor.execute(
                    "INSERT INTO expenses (user_id, date, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                    (self.user_id, datetime.now().strftime("%Y-%m-%d"), "Product Purchase", total_cost, f"Purchased {quantity} {name}")
                )
                
                connection.commit()
                connection.close()

                messagebox.showinfo("Success", f"Purchase completed! Total cost: ${total_cost:.2f}")
                self.load_products()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process purchase: {str(e)}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END) 