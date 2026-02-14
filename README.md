# 🔐 Blink-Based Facial Authentication System

A real-time biometric facial authentication web application built using Python, OpenCV, and Flask.

This system uses face recognition + blink detection (liveness check) to authenticate users securely through a circular Aadhaar-style UI interface.

---




```markdown
![Python](https://img.shields.io/badge/Python-3.14-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![Flask](https://img.shields.io/badge/Flask-WebApp-black)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)

---

## 🚀 Features

- 📷 Real-time webcam streaming
- 🧠 Face recognition using LBPH algorithm
- 👁 Blink detection for liveness verification
- 🔴 Circular biometric scanning interface
- 📊 Loading percentage animation
- 🟢 Fingerprint-style scanning line animation
- 🔊 Success sound on authentication
- ✔ Welcome screen after successful login
- 🌐 Flask-based web application

---

## 🛠 Technologies Used

- Python 3.14
- OpenCV (opencv-contrib-python)
- Flask
- NumPy
- Haarcascade (Face + Eye Detection)
- HTML / CSS / JavaScript

---

## 📂 Project Structure
Facial_Recognition_System/
│
├── dataset/
│ ├── person_name/
│ ├── image1.jpg
│ ├── image2.jpg
│
├── templates/
│ └── blink_login.html
│
├── app.py
├── train_model.py
├── face_model.yml
├── haarcascade_frontalface_default.xml
├── haarcascade_eye.xml
└── README.md

---

## 🧠 How It Works

1. The system loads training images from the `dataset` folder.
2. Faces are detected using Haarcascade.
3. The LBPH model predicts identity.
4. Eye detection monitors blink pattern.
5. Authentication only succeeds when:
   - Face is recognized
   - Blink sequence is detected (Open → Closed → Open)
6. On success:
   - Camera stops
   - Success sound plays
   - Welcome message appears

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Facial-Recognition-System.git
cd Facial-Recognition-System


2️⃣ Create Virtual Environment
python -m venv venv
.\venv\Scripts\activate

3️⃣ Install Dependencies
pip install opencv-contrib-python flask numpy

4️⃣ Prepare Dataset

Create structure:

dataset/
   ├── YourName/
        ├── img1.jpg
        ├── img2.jpg


Use clear front-facing images.

5️⃣ Train Model
python train_model.py


This generates:

face_model.yml

6️⃣ Run Application
python app.py


Open browser:

http://127.0.0.1:5000

🔒 Security Model

This system includes a basic liveness detection mechanism:

Eye detection verifies blink pattern.

Prevents simple photo spoof attacks.

Requires real user presence.

⚠ Note: This is basic Haar-based liveness detection and not production-grade biometric security.

🎯 Future Improvements

MediaPipe-based accurate blink detection

Anti-spoofing using depth analysis

Database integration

Multi-user role system

Cloud deployment

JWT session authentication

👨‍💻 Author

Manoj TK
AI & Machine Learning Enthusiast 🚀
Real-Time Computer Vision Developer
