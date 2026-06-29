import os, csv

FILENAME = "inventory.csv"
HEADERS = ["product_id", "product_name", "unit_price", "stock_qty"]
print("Inventory file saved at:", os.path.abspath(FILENAME))

def init_inventory():
    if os.path.exists(FILENAME):
        choice = input("Inventory file exists. Load (L) or Create new (C)? ").lower()
        if choice == "c":
            with open(FILENAME, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(HEADERS)
            print("New inventory created.")
        else:
            print("Loaded existing inventory.")
    else:
        with open(FILENAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
        print("No file found. New inventory created.")

def menu():
    while True:
        print("\n--- Inventory Menu ---")
        print("1. Add Product")
        print("2. View All Products")
        print("3. Search Product")
        print("4. Adjust Stock")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            search_product()
        elif choice == "4":
            adjust_stock()
        elif choice == "5":
            print("Saving and exiting...")
            break
        else:
            print("Invalid choice. Try again.")

def add_product():
    pid = input("Enter Product ID: ")
    name = input("Enter Product Name: ")
    
    try:
        price = float(input("Enter Unit Price: "))
        qty = int(input("Enter Stock Quantity: "))
    except ValueError:
        print("Invalid input. Price must be a number, and quantity must be an integer.")
        return
    
    if not pid.isdigit() or int(pid) <= 0:
        print("Invalid Product ID. Must be a positive number.")
        return
    if price <= 0:
        print("Invalid Unit Price. Must be greater than zero.")
        return
    if qty < 0:
        print("Invalid Stock Quantity. Cannot be negative.")
        return
    
    with open(FILENAME, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["product_id"] == pid:
                print("Duplicate ID. Product not added.")
                return
    
    with open(FILENAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([pid, name, price, qty])
    print("Product added successfully.")

def view_products():
    with open(FILENAME, "r") as f:
        reader = csv.DictReader(f)
        print("\n--- Product List ---")
        for row in reader:
            print(row)

def search_product():
    keyword = input("Enter Product ID or Name: ").lower()
    found = False
    with open(FILENAME, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if keyword in (row["product_id"].lower(), row["product_name"].lower()):
                print("Found:", row)
                found = True
    if not found:
        print("Product not found.")

MAX_STOCK = 10000   

def adjust_stock():
    pid = input("Enter Product ID: ")
    try:
        change = int(input("Enter stock adjustment (+/-): "))
    except ValueError:
        print("Invalid input. Must be integer.")
        return
    
    rows = []
    updated = False
    with open(FILENAME, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["product_id"] == pid:
                current_qty = int(row["stock_qty"])
                new_qty = current_qty + change
                
                if new_qty < 0:
                    print("Error: Stock cannot go below zero.")
                    return
                if new_qty > MAX_STOCK:
                    print(f"Error: Stock cannot exceed maximum limit ({MAX_STOCK}).")
                    return
                
                row["stock_qty"] = str(new_qty)
                updated = True
            rows.append(row)
    
    if updated:
        with open(FILENAME, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(rows)
        print("Stock updated successfully.")
    else:
        print("Product ID not found.")
    
if __name__ == "__main__":
    init_inventory()   
    menu()             

