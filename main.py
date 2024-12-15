import tkinter as tk
from tkinter import messagebox
import subprocess

# Dummy admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        login_window.destroy()
        open_choice_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def open_choice_menu():
    choice_window = tk.Tk()
    choice_window.title("Admin Menu")
    choice_window.geometry("500x400")
    choice_window.configure(bg="#f0f0f0")

    tk.Label(choice_window, text="Admin Menu", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=20)

    def open_add_new_face():
        try:
            subprocess.Popen(["python", "addNewFace.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Add New Face interface: {e}")

    def face_recognition_interface():
        try:
            subprocess.Popen(["python", "FaceRecog.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Face recognition interface: {e}")
        # Add functionality to open Face Recognition interface here

    tk.Button(choice_window, text="Add New Face", command=open_add_new_face, width=25, font=("Arial", 14), bg="#4caf50", fg="white", relief="raised", bd=3).pack(pady=15)
    tk.Button(choice_window, text="Face Recognition", command=face_recognition_interface, width=25, font=("Arial", 14), bg="#2196f3", fg="white", relief="raised", bd=3).pack(pady=15)

    tk.Button(choice_window, text="Exit", command=choice_window.destroy, width=25, font=("Arial", 14), bg="#f44336", fg="white", relief="raised", bd=3).pack(pady=15)

    choice_window.mainloop()

# Create login window
login_window = tk.Tk()
login_window.title("Admin Login")
login_window.geometry("500x400")
login_window.configure(bg="#f0f0f0")

# Login form
tk.Label(login_window, text="Admin Login", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333333").grid(row=0, column=1, pady=20)

# Username
tk.Label(login_window, text="Username:", font=("Arial", 14), bg="#f0f0f0", fg="#333333").grid(row=1, column=0, padx=10, pady=10, sticky="e")
username_entry = tk.Entry(login_window, font=("Arial", 14), width=20)
username_entry.grid(row=1, column=1, pady=10)

# Password
tk.Label(login_window, text="Password:", font=("Arial", 14), bg="#f0f0f0", fg="#333333").grid(row=2, column=0, padx=10, pady=10, sticky="e")
password_entry = tk.Entry(login_window, font=("Arial", 14), show="*", width=20)
password_entry.grid(row=2, column=1, pady=10)

# Login button
login_button = tk.Button(login_window, text="Login", command=login, font=("Arial", 14), width=15, bg="#4caf50", fg="white", relief="raised", bd=3)
login_button.grid(row=3, column=1, pady=30)

login_window.mainloop()
