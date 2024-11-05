import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from decimal import Decimal

# Database connection function
def connect_db(username, password):
    return mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        database="BankDB"
    )

# Bank Management System GUI
class BankManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")

        # Set window size
        window_width = 800
        window_height = 600
        self.root.geometry(f"{window_width}x{window_height}")

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Variable to track if logged in
        self.is_logged_in = False

        # Database credentials
        self.db_username = tk.StringVar()
        self.db_password = tk.StringVar()

        # Customer details input
        self.customer_name = tk.StringVar()
        self.customer_email = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.initial_balance = tk.DoubleVar()

        # Account details
        self.account_customer_id = tk.IntVar()

        # Transaction details
        self.transaction_account_id = tk.IntVar()
        self.transaction_amount = tk.DoubleVar()
        self.transaction_type = tk.StringVar(value="deposit")

        # GUI Layout
        self.create_login_gui()

    # Create login GUI
    def create_login_gui(self):
        self.clear_gui()
        tk.Label(self.root, text="Database Credentials", font=('Arial', 24, 'bold'), bg='lightblue').pack(pady=20)
        tk.Label(self.root, text="Username", font=('Arial', 16), bg='lightblue').pack(pady=5)
        tk.Entry(self.root, textvariable=self.db_username, font=('Arial', 16)).pack(pady=5)
        tk.Label(self.root, text="Password", font=('Arial', 16), bg='lightblue').pack(pady=5)
        tk.Entry(self.root, textvariable=self.db_password, show='*', font=('Arial', 16)).pack(pady=5)
        tk.Button(self.root, text="Connect", command=self.login, font=('Arial', 16), bg='green', fg='white').pack(pady=20)

    # Clear the GUI
    def clear_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Log in and create the main GUI
    def login(self):
        try:
            db = connect_db(self.db_username.get(), self.db_password.get())
            self.is_logged_in = True
            self.create_main_gui()
            self.root.attributes('-fullscreen', False)  # Avoid fullscreen
        except mysql.connector.Error as err:
            messagebox.showerror("Connection Error", f"Error: {err}")

    # Create main GUI
    def create_main_gui(self):
        self.clear_gui()

        # Create a frame for scrolling
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas to hold the main frame
        self.main_canvas = tk.Canvas(main_frame)
        self.main_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=self.main_canvas.yview)
        self.main_scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)

        # Create a frame inside the canvas
        self.content_frame = tk.Frame(self.main_canvas)
        self.main_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Bind the frame to the canvas for resizing
        self.content_frame.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))

        tk.Label(self.content_frame, text="Welcome to the Bank Management System", font=('Arial', 24, 'bold'), bg='lightgreen').pack(pady=20)

        # Customer Section
        tk.Label(self.content_frame, text="Customer Management", font=('Arial', 20), bg='lightyellow').pack(pady=10)
        tk.Label(self.content_frame, text="Name", font=('Arial', 16)).pack()
        tk.Entry(self.content_frame, textvariable=self.customer_name, font=('Arial', 16)).pack(pady=5)
        tk.Label(self.content_frame, text="Email", font=('Arial', 16)).pack()
        tk.Entry(self.content_frame, textvariable=self.customer_email, font=('Arial', 16)).pack(pady=5)
        tk.Label(self.content_frame, text="Phone", font=('Arial', 16)).pack()
        tk.Entry(self.content_frame, textvariable=self.customer_phone, font=('Arial', 16)).pack(pady=5)
        tk.Label(self.content_frame, text="Initial Balance", font=('Arial', 16)).pack()
        tk.Entry(self.content_frame, textvariable=self.initial_balance, font=('Arial', 16)).pack(pady=5)
        tk.Button(self.content_frame, text="Add Customer", command=self.add_customer, font=('Arial', 16), bg='blue', fg='white').pack(pady=5)
        tk.Button(self.content_frame, text="Show All Customers", command=self.show_customers, font=('Arial', 16), bg='blue', fg='white').pack(pady=5)

        # Account Section
        tk.Label(self.content_frame, text="Account Management", font=('Arial', 20), bg='lightyellow').pack(pady=10)
        tk.Label(self.content_frame, text="Customer ID", font=('Arial', 16)).pack()
        tk.Entry(self.content_frame, textvariable=self.account_customer_id, font=('Arial', 16)).pack(pady=5)
        tk.Button(self.content_frame, text="Search Customer", command=self.search_customer, font=('Arial', 16), bg='blue', fg='white').pack(pady=5)

        # Transaction Section
        tk.Label(self.content_frame, text="Transaction", font=('Arial', 20), bg='lightyellow').pack(pady=10)
        tk.Label(self.content_frame, text="Account ID", font=('Arial', 16)).pack()
        tk.Entry(self.content_frame, textvariable=self.transaction_account_id, font=('Arial', 16)).pack(pady=5)
        tk.Label(self.content_frame, text="Amount", font=('Arial', 16)).pack()
        tk.Entry(self.content_frame, textvariable=self.transaction_amount, font=('Arial', 16)).pack(pady=5)
        tk.Label(self.content_frame, text="Type", font=('Arial', 16)).pack()
        tk.OptionMenu(self.content_frame, self.transaction_type, "deposit", "withdrawal").pack(pady=5)
        tk.Button(self.content_frame, text="Process Transaction", command=self.process_transaction, font=('Arial', 16), bg='blue', fg='white').pack(pady=5)

    # Method to add a customer
    def add_customer(self):
        name = self.customer_name.get()
        email = self.customer_email.get()
        phone = self.customer_phone.get()
        balance = self.initial_balance.get()

        db = connect_db(self.db_username.get(), self.db_password.get())
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO Customers (customer_name, email, phone_number, balance) VALUES (%s, %s, %s, %s)",
                           (name, email, phone, balance))
            db.commit()
            messagebox.showinfo("Success", "Customer added successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    # Method to show all customers
    def show_customers(self):
        db = connect_db(self.db_username.get(), self.db_password.get())
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Customers")
        records = cursor.fetchall()
        customer_list = "\n".join([f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Phone: {row[3]}, Balance: {row[4]}" for row in records])
        messagebox.showinfo("Customers", customer_list)
        cursor.close()
        db.close()

    # Method to search for a customer
    def search_customer(self):
        customer_id = self.account_customer_id.get()
        db = connect_db(self.db_username.get(), self.db_password.get())
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Customers WHERE customer_id = %s", (customer_id,))
        record = cursor.fetchone()
        if record:
            messagebox.showinfo("Customer Found", f"ID: {record[0]}, Name: {record[1]}, Email: {record[2]}, Phone: {record[3]}, Balance: {record[4]}")
        else:
            messagebox.showerror("Not Found", "Customer not found")
        cursor.close()
        db.close()

    # Method to process a transaction
    def process_transaction(self):
        account_id = self.transaction_account_id.get()
        amount = Decimal(self.transaction_amount.get())
        transaction_type = self.transaction_type.get()

        db = connect_db(self.db_username.get(), self.db_password.get())
        cursor = db.cursor()

        try:
            cursor.execute("SELECT balance FROM Customers WHERE customer_id = %s", (account_id,))
            record = cursor.fetchone()
            if record:
                current_balance = record[0]  # This is a Decimal
                if transaction_type == "deposit":
                    new_balance = current_balance + amount  # Both are now Decimal
                elif transaction_type == "withdrawal":
                    if current_balance >= amount:
                        new_balance = current_balance - amount  # Both are now Decimal
                    else:
                        messagebox.showerror("Error", "Insufficient funds")
                        return

                cursor.execute("UPDATE Customers SET balance = %s WHERE customer_id = %s", (new_balance, account_id))
                db.commit()
                messagebox.showinfo("Success", f"Transaction successful! New balance: {new_balance}")
            else:
                messagebox.showerror("Error", "Account not found")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            db.close()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BankManagementSystem(root)
    root.mainloop()
