import cv2
import os
from tkinter import Tk, messagebox
from deepface import DeepFace
import numpy as np

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

# Function to perform spoof detection using DeepFace (based on deep learning models)
def is_spoofed(frame):
    try:
        # Use DeepFace's find method to check for spoof detection
        # DeepFace can use the `age`, `gender`, `emotion`, and `race` models to check for anomalies
        # For spoof detection, you can try using an emotion detection model or age-gender model to detect unrealistic traits
        
        # Example of running DeepFace on the frame for emotion detection (this is a placeholder for spoofing)
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        # If the detected emotion is very flat or "no emotion", it could indicate a spoofed image (e.g., photo)
        if result and 'dominant_emotion' in result[0]:
            emotion = result[0]['dominant_emotion']
            if emotion == "neutral":
                return True  # If neutral emotion detected, mark as spoofed
    except Exception as e:
        print("Error during spoof detection:", e)
    return False

# Function to recognize face using DeepFace and perform spoof detection
def recognize_face(frame, known_faces):
    try:
        # Check if the image is spoofed
        if is_spoofed(frame):
            label = "Spoof Detected"
            color = (0, 0, 255)  # Red for spoof detected
        else:
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
                label = "No Face Detected"
                color = (0, 0, 255)  # Red for no face detected

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

        # Recognize face and check for spoofing
        label, color = recognize_face(frame, known_faces)

        # Display the result on the frame
        cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.imshow("Face Recognition with Anti-Spoofing", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
