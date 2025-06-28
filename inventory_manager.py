"""
Product Inventory Manager for Smart Budget and Inventory Manager
Handles all product-related operations: add, view, edit, delete, simulate purchase
"""

from database import db
from datetime import datetime

class InventoryManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.categories = ['Electronics', 'Groceries', 'Clothing', 'Books', 'Other']

    def add_product(self):
        """Add a new product to the inventory"""
        print("\n" + "="*50)
        print("ADD NEW PRODUCT")
        print("="*50)
        try:
            name = input("Enter product name: ").strip()
            if not name:
                print("Product name cannot be empty.")
                return
            print("\nAvailable categories:")
            for i, category in enumerate(self.categories, 1):
                print(f"{i}. {category}")
            while True:
                try:
                    cat_choice = int(input(f"Select category (1-{len(self.categories)}): "))
                    if 1 <= cat_choice <= len(self.categories):
                        category = self.categories[cat_choice - 1]
                        break
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
            while True:
                try:
                    price = float(input("Enter price: $").strip())
                    if price > 0:
                        break
                    else:
                        print("Price must be positive.")
                except ValueError:
                    print("Invalid price. Enter a number.")
            while True:
                try:
                    stock = int(input("Enter stock quantity: ").strip())
                    if stock >= 0:
                        break
                    else:
                        print("Stock cannot be negative.")
                except ValueError:
                    print("Invalid stock. Enter an integer.")
            query = """
                INSERT INTO products (user_id, name, category, price, stock)
                VALUES (%s, %s, %s, %s, %s)
            """
            if db.execute_query(query, (self.user_id, name, category, price, stock)):
                print(f"\n✓ Product '{name}' added successfully!")
            else:
                print("\n✗ Failed to add product.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def view_products(self):
        """View all products in inventory"""
        print("\n" + "="*80)
        print("PRODUCT INVENTORY")
        print("="*80)
        query = """
            SELECT id, name, category, price, stock
            FROM products
            WHERE user_id = %s
            ORDER BY name
        """
        products = db.execute_query(query, (self.user_id,))
        if not products:
            print("No products found.")
            return
        print(f"{'#':<3} {'Name':<20} {'Category':<15} {'Price':<10} {'Stock':<8}")
        print("-" * 60)
        for i, prod in enumerate(products, 1):
            print(f"{i:<3} {prod['name']:<20} {prod['category']:<15} ${prod['price']:<9.2f} {prod['stock']:<8}")
        print("-" * 60)

    def edit_product(self):
        """Edit an existing product's details"""
        self.view_products()
        query = """
            SELECT id, name, category, price, stock
            FROM products
            WHERE user_id = %s
            ORDER BY name
        """
        products = db.execute_query(query, (self.user_id,))
        if not products:
            return
        try:
            choice = int(input(f"Select product to edit (1-{len(products)}): "))
            if 1 <= choice <= len(products):
                prod = products[choice - 1]
                print(f"Editing '{prod['name']}' (leave blank to keep current value)")
                new_name = input(f"New name [{prod['name']}]: ").strip() or prod['name']
                print("\nAvailable categories:")
                for i, category in enumerate(self.categories, 1):
                    print(f"{i}. {category}")
                cat_choice = input(f"New category [{prod['category']}]: ").strip()
                if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(self.categories):
                    new_category = self.categories[int(cat_choice) - 1]
                else:
                    new_category = prod['category']
                price_input = input(f"New price [{prod['price']}]: $").strip()
                new_price = float(price_input) if price_input else prod['price']
                stock_input = input(f"New stock [{prod['stock']}]: ").strip()
                new_stock = int(stock_input) if stock_input else prod['stock']
                update_query = """
                    UPDATE products
                    SET name = %s, category = %s, price = %s, stock = %s
                    WHERE id = %s AND user_id = %s
                """
                if db.execute_query(update_query, (new_name, new_category, new_price, new_stock, prod['id'], self.user_id)):
                    print("✓ Product updated successfully!")
                else:
                    print("✗ Failed to update product.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def delete_product(self):
        """Delete a product from inventory"""
        self.view_products()
        query = """
            SELECT id, name, category, price, stock
            FROM products
            WHERE user_id = %s
            ORDER BY name
        """
        products = db.execute_query(query, (self.user_id,))
        if not products:
            return
        try:
            choice = int(input(f"Select product to delete (1-{len(products)}): "))
            if 1 <= choice <= len(products):
                prod = products[choice - 1]
                confirm = input(f"Are you sure you want to delete '{prod['name']}'? (y/n): ").lower()
                if confirm == 'y':
                    del_query = "DELETE FROM products WHERE id = %s AND user_id = %s"
                    if db.execute_query(del_query, (prod['id'], self.user_id)):
                        print("✓ Product deleted successfully!")
                    else:
                        print("✗ Failed to delete product.")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def simulate_purchase(self):
        """Simulate purchasing a product (reduce stock, add to expenses)"""
        self.view_products()
        query = """
            SELECT id, name, category, price, stock
            FROM products
            WHERE user_id = %s
            ORDER BY name
        """
        products = db.execute_query(query, (self.user_id,))
        if not products:
            return
        try:
            choice = int(input(f"Select product to purchase (1-{len(products)}): "))
            if 1 <= choice <= len(products):
                prod = products[choice - 1]
                if prod['stock'] <= 0:
                    print("Product is out of stock!")
                    return
                qty = int(input(f"Enter quantity to purchase (max {prod['stock']}): "))
                if 1 <= qty <= prod['stock']:
                    new_stock = prod['stock'] - qty
                    total_cost = prod['price'] * qty
                    # Update stock
                    update_query = "UPDATE products SET stock = %s WHERE id = %s AND user_id = %s"
                    db.execute_query(update_query, (new_stock, prod['id'], self.user_id))
                    # Add to expenses
                    expense_query = """
                        INSERT INTO expenses (user_id, date, category, amount, description)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    today = datetime.now().strftime("%Y-%m-%d")
                    db.execute_query(expense_query, (self.user_id, today, 'Shopping', total_cost, f"Purchased {qty} x {prod['name']}"))
                    print(f"✓ Purchase successful! {qty} x {prod['name']} bought for ${total_cost:.2f}")
                else:
                    print("Invalid quantity.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.") 