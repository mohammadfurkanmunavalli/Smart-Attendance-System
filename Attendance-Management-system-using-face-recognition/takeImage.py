import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time


# take Image of user
def TakeImage(l1, l2, l3, l4, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if not l1 and not l2:
        t = "Please enter your Enrollment Number and Name."
        text_to_speech(t)
        return
    elif not l1:
        t = "Please enter your Enrollment Number."
        text_to_speech(t)
        return
    elif not l2:
        t = "Please enter your Name."
        text_to_speech(t)
        return
    elif not l3:
        t = "Please enter your Branch."
        text_to_speech(t)
        return
    elif not l4:
        t = "Please enter your Email."
        text_to_speech(t)
        return

    try:
        cam = cv2.VideoCapture(0)  # Use 0 for the default camera; adjust index if needed
        if not cam.isOpened():
            text_to_speech("Error: Camera not accessible.")
            message.configure(text="Error: Camera not accessible.")
            return

        detector = cv2.CascadeClassifier(haarcasecade_path)
        if detector.empty():
            text_to_speech("Error: Haar Cascade file not found.")
            message.configure(text="Error: Haar Cascade file not found.")
            return

        Enrollment = l1
        Name = l2
        Branch = l3
        Email = l4
        sampleNum = 0
        directory = f"{Enrollment}_{Name}"
        path = os.path.join(trainimage_path, directory)

        if os.path.exists(path):
            text_to_speech("Student data already exists.")
            message.configure(text="Student data already exists.")
            return

        os.mkdir(path)

        while True:
            ret, img = cam.read()
            if not ret:
                text_to_speech("Error: Failed to capture image.")
                message.configure(text="Error: Failed to capture image.")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                image_path = os.path.join(
                    path,
                    f"{Name}_{Enrollment}_{Branch}_{sampleNum}.jpg"
                )
                cv2.imwrite(image_path, gray[y:y+h, x:x+w])
                cv2.imshow("Frame", img)

            if cv2.waitKey(1) & 0xFF == ord("q"):  # Quit on pressing 'q'
                break
            elif sampleNum >= 5:  # Limit to 5 samples
                break

        cam.release()
        cv2.destroyAllWindows()

        # Save details to CSV
        csv_path = "E:\\Project\\Project\\StudentDetails\\studentdetails.csv"
        if not os.path.exists(csv_path):
            with open(csv_path, "w", newline="") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(["Enrollment", "Name", "Branch", "Email"])  # Add headers

        with open(csv_path, "a", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([Enrollment, Name, Branch, Email])

        res = f"Images saved for Enrollment No: {Enrollment}, Name: {Name}, Branch: {Branch}, Email: {Email}"
        message.configure(text=res)
        text_to_speech(res)

    except Exception as e:
        error_message = f"Error: {str(e)}"
        text_to_speech(error_message)
        message.configure(text=error_message)
