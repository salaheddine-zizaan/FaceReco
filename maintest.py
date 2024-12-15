import cv2
from tkinter import Tk, messagebox
from deepface import DeepFace
import numpy as np
import os  # Import the os module


# Directory where authorized faces are stored
faces_dir = "faces"

# Function to load known faces from the 'faces' directory
def load_known_faces(faces_dir):
    known_faces = []
    if os.path.exists(faces_dir):
        for file in os.listdir(faces_dir):
            if file.endswith(".jpg") or file.endswith(".png"):
                image_path = os.path.join(faces_dir, file)
                known_faces.append(image_path)
    return known_faces

# Function to recognize face using DeepFace and perform spoof detection
def recognize_face(frame, known_faces):
    try:
        # Use DeepFace's find method for face recognition
        result = DeepFace.find(frame, db_path=faces_dir, enforce_detection=False)

        if result and len(result) > 0:
            # Extract the name from the result DataFrame
            matched_face = result[0]
            matched_image_path = matched_face["identity"][0]  # The first match from the DataFrame
            matched_name = os.path.splitext(os.path.basename(matched_image_path))[0]  # Extract name from image path
            label = matched_name if matched_name else "Unknown"
            color = (0, 255, 0)  # Green for authorized face

        else:
            label = "Spoof Detected"
            color = (0, 0, 255)  # Red for spoof detected

    except Exception as e:
        label = "Error"
        color = (0, 0, 255)  # Red for error
        print("Error:", e)

    return label, color

def main():
    # Load known faces
    known_faces = load_known_faces(faces_dir)

    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        Tk().withdraw()
        messagebox.showerror("Error", "Cannot access the camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # If faces are detected, process them
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Crop the face region from the frame
            face_roi = frame[y:y + h, x:x + w]

            # Recognize the face and check for spoof
            label, color = recognize_face(face_roi, known_faces)

            # Display the result on the frame
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # Show the frame with face detection
        cv2.imshow("Face Recognition with Anti-Spoofing", frame)

        # Exit the loop when 'q' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
