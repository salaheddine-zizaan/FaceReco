import tkinter as tk
from tkinter import messagebox
import os
import cv2

def capture_face():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Error", "Please enter a name.")
        return

    faces_dir = "faces"
    os.makedirs(faces_dir, exist_ok=True)
    file_path = os.path.join(faces_dir, f"{name}.jpg")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access the camera.")
        return

    messagebox.showinfo("Info", "Press 's' to save the image and 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image from camera.")
            break

        cv2.imshow("Capture Face", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            cv2.imwrite(file_path, frame)
            messagebox.showinfo("Success", f"Face saved as {file_path}")
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Create the Add New Face window
add_face_window = tk.Tk()
add_face_window.title("Add New Face")
add_face_window.geometry("500x400")
add_face_window.configure(bg="#f0f0f0")

# Interface elements
tk.Label(add_face_window, text="Add New Face", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=20)

# Name entry
tk.Label(add_face_window, text="Name:", font=("Arial", 14), bg="#f0f0f0", fg="#333333").pack(pady=10)
name_entry = tk.Entry(add_face_window, font=("Arial", 14), width=30)
name_entry.pack(pady=10)

# Capture button
tk.Button(add_face_window, text="Capture Face", command=capture_face, font=("Arial", 14), width=20, bg="#4caf50", fg="white", relief="raised", bd=3).pack(pady=20)

# Exit button
tk.Button(add_face_window, text="Exit", command=add_face_window.destroy, font=("Arial", 14), width=20, bg="#f44336", fg="white", relief="raised", bd=3).pack(pady=10)

add_face_window.mainloop()
