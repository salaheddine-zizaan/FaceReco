import cv2
import os
import time
import threading
from tkinter import Tk, Label, Button, messagebox
from deepface import DeepFace
from PIL import Image, ImageTk


# Path to the folder containing known faces
KNOWN_FACES_FOLDER = "faces"
TEMP_IMAGE_PATH = "temp_img/temp_image.jpg"  # Path to store the single temporary image

# Ensure the temp folder exists
if not os.path.exists("temp_img"):
    os.makedirs("temp_img")

# Initialize camera
cap = cv2.VideoCapture(0)

# Global variable to store the captured frame
captured_frame = None

# Function to process the frame and save the full image temporarily
def process_frame(frame):
    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Save the entire frame as a temporary image (overwrite the existing one)
    cv2.imwrite(TEMP_IMAGE_PATH, frame)  # Save the full frame, not just the face

    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

# Function to take the image after a delay of 5 seconds
def capture_image():
    # Capture the frame immediately when the button is clicked
    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Failed to capture the image.")
        return

    # Process the captured frame and save it temporarily
    processed_frame = process_frame(frame)

    # Show the result in the same window
    show_results(processed_frame)

# Function to show results in the same window
def show_results(frame):
    try:
        # Use DeepFace to find and check for spoofing
        result = DeepFace.find(img_path=TEMP_IMAGE_PATH, db_path=KNOWN_FACES_FOLDER, enforce_detection=False, anti_spoofing=True)
        identities = []
        for df in result:
            if not df.empty:
                identities.extend(df['identity'].tolist())

        if identities:
            name = os.path.basename(identities[0])  # Extract name from the path
            label = f"Hello, {name}"
            color = (0, 255, 0)  # Green for matched face
        else:
            label = "Unauthorized"
            color = (0, 0, 255)  # Red for unauthorized

    except Exception as e:
        print(f"Spoof detected: {e}")
        label = "Spoof Detected"
        color = (0, 0, 255)  # Red for spoofed face

    # Update the result label with the outcome
    result_label.config(text=label, fg="white", bg="green" if color == (0, 255, 0) else "red")
    result_label.pack(pady=10)

    # Display the image in the Tkinter window
    show_camera_image(frame)

# Function to display the camera feed in Tkinter window
def show_camera_image(frame):
    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    img = img.resize((640, 480))  # Resize for the Tkinter window

    # Convert image to Tkinter format
    img_tk = ImageTk.PhotoImage(img)

    # Update the label with the new image
    camera_label.config(image=img_tk)
    camera_label.image = img_tk  # Keep a reference to avoid garbage collection

# Function to start the process
def start_recognition():
    # Start the capture process in a new thread to avoid blocking the main UI
    threading.Thread(target=capture_image).start()

# Function to update the live camera feed continuously
def update_camera_feed():
    global captured_frame
    ret, frame = cap.read()
    if ret:
        captured_frame = frame
        show_camera_image(frame)
    main_window.after(10, update_camera_feed)  # Update every 10 ms

# Create the main Tkinter window
main_window = Tk()
main_window.title("Face Recognition with Anti-Spoofing")

# Label to show the camera feed
camera_label = Label(main_window)
camera_label.pack(pady=10)

# Button to start the recognition process
start_button = Button(main_window, text="Start Recognition", command=start_recognition, font=("Arial", 14), bg="#4caf50", fg="white")
start_button.pack(pady=20)

# Label to show the recognition result
result_label = Label(main_window, text="", font=("Arial", 20, "bold"))
result_label.pack(pady=10)

# Retry button to close the result window and return to the main screen
retry_button = Button(main_window, text="Retry", command=result_label.pack_forget, font=("Arial", 14), bg="#4caf50", fg="white")
retry_button.pack(pady=10)

# Run the Tkinter main loop
main_window.geometry("800x600")
main_window.after(1, update_camera_feed)  # Start the camera feed immediately
main_window.mainloop()

# Release resources when done
cap.release()
cv2.destroyAllWindows()
