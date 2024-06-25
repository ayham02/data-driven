import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import date

# Connect to MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Ola2"
)
db_cursor = db_connection.cursor()

class OlaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ola Application")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.current_customer_id = None

        self.login_tab = tk.Frame(self.notebook)
        self.notebook.add(self.login_tab, text="Login")
        self.create_login_tab(self.login_tab)

        # Customer registration tab
        self.customer_tab = tk.Frame(self.notebook)
        self.notebook.add(self.customer_tab, text="Registration")
        self.create_customer_tab(self.customer_tab)

        # Ride booking tab (initially disabled)
        self.ride_tab = tk.Frame(self.notebook)
        self.notebook.add(self.ride_tab, text="Book a Ride")
        self.create_ride_tab(self.ride_tab)
        self.notebook.tab(2, state="disabled")

        # Ride history tab
        self.history_tab = tk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="Ride History")
        self.create_history_tab(self.history_tab)
        self.notebook.tab(3, state="disabled")

        self.feedback_tab = tk.Frame(self.notebook)
        self.notebook.add(self.feedback_tab, text="Provide Feedback")
        self.create_feedback_tab(self.feedback_tab)
        self.notebook.tab(4, state="disabled")

        self.disable_tabs()

    def create_login_tab(self, tab):
        tk.Label(tab, text="Email:").grid(row=0, column=0, padx=10, pady=5)
        self.login_email_entry = tk.Entry(tab)
        self.login_email_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(tab, text="Password:").grid(row=1, column=0, padx=10,pady=5)
        self.login_password_entry = tk.Entry(tab)
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(tab, text="Login", command=self.login_customer)
        self.login_button.grid(row=3, columnspan=3, padx=10, pady=10)

    def login_customer(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        if not email and not password:
            messagebox.showerror("Error", "Email and password is required")
            return

        try:
            query = "SELECT CustomerID FROM Customer WHERE Email = %s and Password = %s"
            db_cursor.execute(query, (email,password,))
            customer = db_cursor.fetchone()

            if customer:
                messagebox.showinfo("Success", "Login successful")
                self.current_customer_id = customer[0]
                self.enable_tabs()
                self.notebook.select(self.ride_tab)  # Switch to the "Book a Ride" tab
                self.populate_driver_options()  # Populate driver options for booking
                self.populate_history()
                self.populate_history()  # Populate ride history for the logged-in customer
            else:
                messagebox.showerror("Error", "Email/password not found. Please register first.")

        except Exception as e:
            messagebox.showerror("Error", f"Error logging in: {str(e)}")

    def create_customer_tab(self, tab):
        tk.Label(tab, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(tab)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(tab, text="Email:").grid(row=1, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(tab)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(tab, text="Password:").grid(row=2, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(tab)
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(tab, text="Phone Number:").grid(row=3, column=0, padx=10, pady=5)
        self.phone_entry = tk.Entry(tab)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)

        self.register_button = tk.Button(tab, text="Register", command=self.register_customer)
        self.register_button.grid(row=4, columnspan=2, padx=10, pady=10)

    def register_customer(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        phone = self.phone_entry.get()

        if not name or not email or not phone:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            query = "INSERT INTO Customer (Name, Email, Password, PhoneNumber) VALUES (%s, %s, %s, %s)"
            values = (name, email, password, phone)
            db_cursor.execute(query, values)
            db_connection.commit()
            messagebox.showinfo("Success", "Customer registered successfully")

            # Enable the "Book a Ride" tab after registration
            self.notebook.tab(0, state="Disabled")
            self.notebook.tab(1, state="Disabled")
            self.notebook.tab(2, state="normal")
            self.notebook.tab(3, state="normal")
            self.notebook.select(self.ride_tab)  # Switch to the "Book a Ride" tab
            self.current_customer_id = db_cursor.lastrowid  # Get the newly inserted customer ID
            self.populate_driver_options()  # Populate driver options for booking
            self.populate_history()  # Populate ride history for the newly registered customer

        except Exception as e:
            messagebox.showerror("Error", f"Error registering customer: {str(e)}")

    def enable_tabs(self):
        # Enable all tabs (Login, Registration, Ride, History, Feedback)
        for tab_index in range(self.notebook.index("end")):
            self.notebook.tab(tab_index, state="normal")
        self.notebook.tab(0, state="disabled")
        self.notebook.tab(1, state="disabled")
    
    def create_ride_tab(self, tab):
        tk.Label(tab, text="Select Driver:").grid(row=0, column=0, padx=10, pady=5)
        self.driver_options = ttk.Combobox(tab, state="readonly")
        self.driver_options.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(tab, text="Pickup Location:").grid(row=1, column=0, padx=10, pady=5)
        self.pickup_entry = tk.Entry(tab)
        self.pickup_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(tab, text="Drop-off Location:").grid(row=2, column=0, padx=10, pady=5)
        self.dropoff_entry = tk.Entry(tab)
        self.dropoff_entry.grid(row=2, column=1, padx=10, pady=5)

        self.book_ride_button = tk.Button(tab, text="Book Ride", command=self.book_ride)
        self.book_ride_button.grid(row=3, columnspan=2, padx=10, pady=10)
        # Populate driver options when the tab is created
        self.populate_driver_options()

        self.logout_button = tk.Button(tab, text="Logout", command=self.logout_customer)
        self.logout_button.grid(columnspan=2, padx=10, pady=10)
        self.give_feedback_button = tk.Button(tab, text="Give Feedback", command=self.show_feedback_form)
        self.give_feedback_button.grid(columnspan=2, padx=10, pady=10)

    def populate_driver_options(self):
        try:
            query = "SELECT DriverID, Name FROM Driver"
            db_cursor.execute(query)
            drivers = db_cursor.fetchall()
            self.driver_options["values"] = [f"{driver[0]}: {driver[1]}" for driver in drivers]
            if drivers:
                self.driver_options.current(0)  # Select the first driver by default
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching drivers: {str(e)}")

    def book_ride(self):
        driver_info = self.driver_options.get()
        pickup = self.pickup_entry.get()
        dropoff = self.dropoff_entry.get()

        if not driver_info or not pickup or not dropoff:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            # Parse driver information
            driver_id = int(driver_info.split(":")[0])

            # Get current date
            today = date.today()

            # Insert ride into database
            query = "INSERT INTO Ride (CustomerID, DriverID, PICKUP, DROP_OFF, RIDEDATE) VALUES (%s, %s, %s, %s, %s)"
            values = (self.current_customer_id, driver_id, pickup, dropoff, today)
            db_cursor.execute(query, values)
            db_connection.commit()

            messagebox.showinfo("Success", "Ride booked successfully")
            self.clear_ride_fields()
            self.populate_history()  # Update ride history after booking

        except Exception as e:
            messagebox.showerror("Error", f"Error booking ride: {str(e)}")

    def clear_ride_fields(self):
        self.driver_options.current(0)
        self.pickup_entry.delete(0, tk.END)
        self.dropoff_entry.delete(0, tk.END)

    def create_history_tab(self, tab):
        self.history_tree = ttk.Treeview(tab, columns=("Driver", "Pickup", "Drop-off", "Date", "Cancel"))
        self.history_tree.heading("#0", text="Ride ID")
        self.history_tree.heading("Driver", text="Driver")
        self.history_tree.heading("Pickup", text="Pickup")
        self.history_tree.heading("Drop-off", text="Drop-off")
        self.history_tree.heading("Date", text="Date")
        self.history_tree.heading("Cancel", text="Cancel")
        self.history_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.cancel_ride_button = tk.Button(tab, text="Cancel Ride", command=self.cancel_ride)
        self.cancel_ride_button.pack(padx=10, pady=10)
        self.populate_history()
        self.logout_button = tk.Button(tab, text="Logout", command=self.logout_customer)
        self.logout_button.pack(pady=10)
        self.give_feedback_button = tk.Button(tab, text="Give Feedback", command=self.show_feedback_form)
        self.give_feedback_button.pack(pady=10)

    def populate_history(self):
        try:
            query = "SELECT RideID, Driver.Name, PICKUP, DROP_OFF, RIDEDATE FROM Ride JOIN Driver ON Ride.DriverID = Driver.DriverID WHERE CustomerID = %s"
            db_cursor.execute(query, (self.current_customer_id,))
            rides = db_cursor.fetchall()
            self.history_tree.delete(*self.history_tree.get_children())  # Clear existing data
            for ride in rides:
                self.history_tree.insert("", tk.END, text=ride[0], values=(ride[1], ride[2], ride[3], ride[4].strftime("%Y-%m-%d")))
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching ride history: {str(e)}")

    def create_feedback_tab(self, tab):
        self.feedback_tree = ttk.Treeview(tab, columns=("Driver", "Rating", "Comments", "Date"))
        self.feedback_tree.heading("#0", text="Ride ID")
        self.feedback_tree.heading("Driver", text="Driver")
        self.feedback_tree.heading("Rating", text="Rating")
        self.feedback_tree.heading("Comments", text="Comments")
        self.feedback_tree.heading("Date", text="Date")
        self.feedback_tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.populate_feedback()
        self.logout_button = tk.Button(tab, text="Logout", command=self.logout_customer)
        self.logout_button.pack(pady=10)
        self.give_feedback_button = tk.Button(tab, text="Give Feedback", command=self.show_feedback_form)
        self.give_feedback_button.pack(pady=10)

    def populate_feedback(self):
        try:
            if self.current_customer_id is not None:
                query = "SELECT Ride.RideID, Driver.Name, Feedback.Rating, Feedback.Comments, Feedback.FeedbackDate FROM Ride JOIN Driver ON Ride.DriverID = Driver.DriverID LEFT JOIN Feedback ON Ride.RideID = Feedback.RideID WHERE Ride.CustomerID = %s"
                db_cursor.execute(query, (self.current_customer_id,))
                feedbacks = db_cursor.fetchall()
                self.feedback_tree.delete(*self.feedback_tree.get_children())  # Clear existing data
                for feedback in feedbacks:
                    self.feedback_tree.insert("", tk.END, text=feedback[0], values=(feedback[1], feedback[2], feedback[3], feedback[4].strftime("%Y-%m-%d")))
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching feedback: {str(e)}")
    
    def show_feedback_form(self):
        feedback_form = tk.Toplevel()
        feedback_form.title("Feedback Form")

        tk.Label(feedback_form, text="Rating (1-5):").pack()
        rating_entry = tk.Entry(feedback_form)
        rating_entry.pack()

        tk.Label(feedback_form, text="Comments:").pack()
        comments_entry = tk.Text(feedback_form, height=5)
        comments_entry.pack()

        submit_button = tk.Button(feedback_form, text="Submit", command=lambda: self.submit_feedback(rating_entry.get(), comments_entry.get("1.0", tk.END)))
        submit_button.pack()

    def submit_feedback(self, rating, comments):
        try:
            # Assuming you have access to current ride details (RideID, DriverID, CustomerID)
            ride_id = 1  # Replace with actual RideID
            driver_id = 1  # Replace with actual DriverID
            customer_id = 1  # Replace with actual CustomerID

            # Insert feedback into database
            sql = "INSERT INTO Feedback (RideID, DriverID, CustomerID, Rating, Comments, FeedbackDate) VALUES (%s, %s, %s, %s, %s, NOW())"
            values = (ride_id, driver_id, customer_id, rating, comments)
            db_cursor.execute(sql, values)
            db_connection.commit()

            messagebox.showinfo("Success", "Feedback submitted successfully.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error submitting feedback: {str(e)}")

    def cancel_ride(self):
        selected_item = self.history_tree.focus()  # Get currently selected item
        if selected_item:
            ride_id = self.history_tree.item(selected_item)["text"]
            try:
                # Check if the ride has already been cancelled
                query = "SELECT RideID FROM Ride WHERE RideID = %s AND CustomerID = %s AND CANCEL = TRUE"
                db_cursor.execute(query, (ride_id, self.current_customer_id))
                if db_cursor.fetchone():
                    messagebox.showinfo("Info", "This ride has already been cancelled.")
                    return

                # Update the ride to mark it as cancelled
                query_update = "UPDATE Ride SET CANCEL = TRUE WHERE RideID = %s AND CustomerID = %s"
                db_cursor.execute(query_update, (ride_id, self.current_customer_id))
                db_connection.commit()
                messagebox.showinfo("Success", "Ride cancelled successfully.")
                self.populate_history()  # Refresh ride history after cancellation

            except Exception as e:
                messagebox.showerror("Error", f"Error cancelling ride: {str(e)}")

    def logout_customer(self):
        try:
            self.current_customer_id = None
            self.disable_tabs()  # Disable all tabs after logout
            self.notebook.tab(0, state="normal")
            self.notebook.tab(1, state="normal")
            self.clear_login_fields()
            self.notebook.select(self.login_tab)

        except Exception as e:
            messagebox.showerror("Error", f"Error logging out: {str(e)}")

    def clear_login_fields(self):
        self.login_email_entry.delete(0, tk.END)
        self.login_password_entry.delete(0, tk.END)
    
    def disable_tabs(self):
        # Disable all tabs except Login and Customer Registration tabs
        for tab_index in range(self.notebook.index("end")):
            tab_name = self.notebook.tab(tab_index, "text")
            if tab_name not in ["Login", "Registration"]:
                self.notebook.tab(tab_index, state="hidden")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = OlaApp(root)
    root.mainloop()