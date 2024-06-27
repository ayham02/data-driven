import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import tkinter.font as tkFont
import backend

current_user_id = None
current_ride_id = None

def login():
    global current_user_id
    phoneno = login_phoneno.get()
    password = login_password.get()
    user_id = backend.verify_user(phoneno, password)
    if user_id:
        current_user_id = user_id
        messagebox.showinfo("Login Success", "Welcome back!")
        show_booking_window()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

def register():
    username = register_username.get()
    phoneno = register_phoneno.get()
    password = register_password.get()
    if backend.add_user(username, phoneno, password):
        messagebox.showinfo("Registration Success", "Account created successfully!")
        show_login_window()  # Show login window after successful registration
    else:
        messagebox.showerror("Registration Failed", "Username already exists")

def book_ride():
    global current_ride_id
    pickup = pickup_location.get()
    dropoff = dropoff_location.get()
    ride_id = backend.book_ride(current_user_id, pickup, dropoff)
    if ride_id:
        current_ride_id = ride_id
        messagebox.showinfo("Booking Success", "Please continue with the payment.")
        show_payment_window()
    else:
        messagebox.showerror("Booking Failed", "Unable to book ride")

def make_payment():
    payment_method = v.get()
    amount = 100
    if backend.process_payment(current_ride_id, payment_method, amount):
        messagebox.showinfo("Payment Success", "Payment successful! Ride booked Successfully.")
        show_feedback_window()
    else:
        messagebox.showerror("Payment Failed", "Payment failed")

def submit_feedback():
    rating = feedback_rating.get()
    comments = feedback_comments.get()
    if backend.submit_feedback(current_ride_id, rating, comments):
        messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")
    else:
        messagebox.showerror("Feedback Failed", "Unable to submit feedback")

def show_login_window():
    for widget in root.winfo_children():
        widget.pack_forget()
    logo_label.pack()
    login_frame.pack()
    login_phoneno.delete(0, 'end')
    login_password.delete(0, 'end')
    ()

def show_registration_window():
    for widget in root.winfo_children():
        widget.pack_forget()
    logo_label.pack()
    registration_frame.pack()

def show_booking_window():
    for widget in root.winfo_children():
        widget.pack_forget()
    logo_label.pack()
    booking_frame.pack()

def show_payment_window():
    for widget in root.winfo_children():
        widget.pack_forget()
    logo_label.pack()
    payment_frame.pack()

def show_feedback_window():
    for widget in root.winfo_children():
        widget.pack_forget()
    logo_label.pack()
    feedback_frame.pack()

root = tk.Tk()
root.title("OLA App Clone")

# Load the logo image
logo_image = PhotoImage(file="D:\LPU/bootcamp\Ola/new\ola_logo.png")
logo_label = tk.Label(root, image=logo_image)
logo_label.pack()

login_frame = tk.Frame(root)
tk.Label(login_frame, text="Welcome to OLA Cabs", width=40, height=5, font=('Times New Roman', 15, 'bold')).pack()
tk.Label(login_frame, text="Phone number").pack()
login_phoneno = tk.Entry(login_frame)
login_phoneno.pack()
tk.Label(login_frame, text="Password").pack()
login_password = tk.Entry(login_frame, show="*")
login_password.pack()
tk.Button(login_frame, text="Login", command=login).pack()
tk.Button(login_frame, text="Register", command=show_registration_window).pack()

registration_frame = tk.Frame(root)
tk.Label(registration_frame, text="Username").pack()
register_username = tk.Entry(registration_frame)
register_username.pack()
tk.Label(registration_frame, text="Phonenumber").pack()
register_phoneno = tk.Entry(registration_frame)
register_phoneno.pack()
tk.Label(registration_frame, text="Password").pack()
register_password = tk.Entry(registration_frame, show="*")
register_password.pack()
tk.Button(registration_frame, text="Register", command=register).pack()
tk.Button(registration_frame, text="Back to Login", command=show_login_window).pack()

booking_frame = tk.Frame(root)
booking_frame.pack()
tk.Label(booking_frame, text="Pickup Location").pack()
pickup_location = tk.Entry(booking_frame)
pickup_location.pack()
tk.Label(booking_frame, text="Dropoff Location").pack()
dropoff_location = tk.Entry(booking_frame)
dropoff_location.pack()

tk.Label(booking_frame, text="Select Vehicle:").pack()
v = tk.IntVar()
tk.Radiobutton(booking_frame, 
               text="Auto",
               padx = 20, 
               variable=v, 
               value=1).pack(anchor=tk.W)

tk.Radiobutton(booking_frame, 
               text="Sedan/Hatchback",
               padx = 20, 
               variable=v, 
               value=2).pack(anchor=tk.W)

tk.Radiobutton(booking_frame, 
               text="SUV",
               padx = 20, 
               variable=v, 
               value=3).pack(anchor=tk.W)
  
tk.Button(booking_frame, text="Book Ride", command=book_ride).pack()
tk.Button(booking_frame, text="Logout", command=show_login_window).pack()

payment_frame = tk.Frame(root)
tk.Label(payment_frame, text="Payment Method").pack()
v = tk.IntVar()
tk.Radiobutton(payment_frame, 
               text="UPI",
               padx = 20, 
               variable=v, 
               value=1).pack(anchor=tk.W)

tk.Radiobutton(payment_frame, 
               text="Cash",
               padx = 20, 
               variable=v, 
               value=2).pack(anchor=tk.W)

tk.Radiobutton(payment_frame, 
               text="Credit/Debit card",
               padx = 20, 
               variable=v, 
               value=3).pack(anchor=tk.W)
tk.Button(payment_frame, text="Proceed", command=make_payment,).pack()
tk.Button(payment_frame, text="Logout", command=show_login_window).pack()

feedback_frame = tk.Frame(root)
tk.Label(feedback_frame, text="Rating (1-5)").pack()
feedback_rating = tk.Entry(feedback_frame)
feedback_rating.pack()
tk.Label(feedback_frame, text="Comments").pack()
feedback_comments = tk.Entry(feedback_frame)
feedback_comments.pack()
tk.Button(feedback_frame, text="Submit Feedback", command=submit_feedback).pack()
tk.Button(booking_frame, text="Logout", command=show_login_window).pack()

# Show the login window initially
show_login_window()

root.mainloop()
