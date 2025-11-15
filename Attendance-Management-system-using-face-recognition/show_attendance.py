import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = "Please enter the subject name."
            text_to_speech(t)
            return

        os.chdir(f"E:\\Project\\Project\\Attendance\\{Subject}")
        filenames = glob(f"E:\\Project\\Project\\Attendance\\{Subject}\\{Subject}*.csv")
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = (
                str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + "%"
            )
        newdf.to_csv("attendance.csv", index=False)

        send_emails(newdf, Subject)  # Send emails after calculating attendance

        root = tkinter.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="black")
        cs = f"E:\\Project\\Project\\Attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:

                    label = tkinter.Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    def send_emails(attendance_df, subject_name):
        try:
            # Load student details with emails
            student_details_path = "E:\\Project\\Project\\StudentDetails\\studentdetails.csv"
            student_details = pd.read_csv(student_details_path)

            # Convert to dictionary for quick lookup
            email_dict = dict(
                zip(student_details["Enrollment"], student_details["Email"])
            )

            # Email setup
            sender_email = "Your email"
            app_password = "gmail password"  # Replace with your email app password
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            # Initialize SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, app_password)

            # Send emails
            for _, row in attendance_df.iterrows():
                enrollment = row["Enrollment"]
                name = row["Name"]
                attendance = row["Attendance"]
                if enrollment in email_dict:
                    recipient_email = email_dict[enrollment]

                    # Email content
                    subject = f"Attendance Details for {subject_name}"
                    body = (
                        f"Dear {name},\n\n"
                        f"Your attendance for the subject '{subject_name}' is: {attendance}.\n\n"
                        "Best regards,\nAttendance Management System"
                    )
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = recipient_email
                    msg["Subject"] = subject
                    msg.attach(MIMEText(body, "plain"))

                    # Send email
                    server.sendmail(sender_email, recipient_email, msg.as_string())
                    print(f"Email sent to {name} at {recipient_email}")

            server.quit()
            text_to_speech("Emails sent successfully.")
        except Exception as e:
            print(f"Error sending emails: {str(e)}")
            text_to_speech(f"Error sending emails: {str(e)}")

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    titl = tk.Label(
        subject,
        text="Attendance of which subject?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"E:\\Project\\Project\\Attendance\\{sub}")

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()
