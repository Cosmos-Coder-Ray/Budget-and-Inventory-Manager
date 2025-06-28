# Smart Budget and Inventory Manager

A Python + MySQL project for managing personal expenses and product inventory.  
Perfect for Computer Science assignments or personal use!

## Features

- **User Login System:** Register and log in with secure password hashing.
- **Expense Tracker:** Add, view, delete, and filter expenses by category or month.
- **Product Inventory Manager:** Add, view, edit, delete products. Simulate purchases (reduces stock and adds to expenses).
- **Reports:** View monthly expenses, products low in stock, and total inventory value.
- **Menu-driven CLI:** Easy-to-use text interface.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Cosmos-Coder-Ray/Budget-and-Inventory-Manager.git
cd Budget-and-Inventory-Manager
```

### 2. Install Python Dependencies
```bash
pip install mysql-connector-python
```

### 3. Set Up MySQL Database
- Open MySQL Workbench or CLI.
- Run the `database_setup.sql` script to create the database and tables.

### 4. Configure Database Connection
- Edit `config.py` and set your MySQL username and password.

### 5. Run the Program
```bash
python main.py
```

## File Structure

- `main.py` - Main CLI interface
- `database.py` - Database connection and utilities
- `expense_tracker.py` - Expense management
- `inventory_manager.py` - Product management
- `reports.py` - Reporting features
- `config.py` - Database configuration
- `database_setup.sql` - SQL for database/tables

## License

MIT License

---

> Created for educational purposes.  
> For any issues, open an issue on GitHub!
