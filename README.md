# Smart Attendance System Using ML-Based Face Recognition

A machine learning-based face recognition attendance system that allows educational institutions and organizations to automate and digitize attendance using face detection and recognition. 
This system registers student faces, marks attendance with real-time face recognition, and stores attendance data in CSV files.

## 🧠 Key Features

- Face Registration using OpenCV
- Real-time Face Detection and Recognition
- Subject-wise Attendance Marking
- Attendance Logging in CSV
- Email Notifications on Attendance
- Offline Functionality (No Internet Required)
- Simple GUI using Tkinter (Windows-compatible)

---

## 🛠️ Technologies and Libraries Used

- **Python 3.x**
- **OpenCV** - for image processing and face detection
- **NumPy** - for array manipulation
- **Tkinter** - for GUI
- **Pandas** - for attendance file handling
- **scikit-learn** - for model training (SVM/KNN)
- **face_recognition** - for facial encoding and matching
- **smtplib & email** - for sending attendance notification emails
- **os / shutil** - for file and folder operations
- **datetime** - for timestamping attendance

---

## 📁 Project Structure

Smart-Attendance-System-Using-ML-Based-Face-Recognition/
│
├── Attendance/ # Generated attendance CSVs
├── Dataset/ # Stored face images of registered students
├── Trained_model/ # Encoded face data saved as .pkl
├── main.py # Main launcher with GUI
├── train_model.py # Encodes faces and trains model
├── face_recog.py # Recognition and attendance marking logic
├── register.py # Face registration module
├── utils/ # Email, validation helpers
├── requirements.txt # Python libraries required
└── README.md # Project documentation
