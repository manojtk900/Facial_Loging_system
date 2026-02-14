from flask import Flask, render_template, Response, redirect, url_for
import cv2
import os

app = Flask(__name__)

# Load cascade
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

# Load labels
dataset_path = "dataset"
label_map = {}
label_id = 0

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)
    if os.path.isdir(person_folder):
        label_map[label_id] = person_name
        label_id += 1


# -------------------------
# Facial Login Function
# -------------------------
def check_face():
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    camera.release()

    if not success:
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face)

        if confidence < 80:
            return label_map.get(label)

    return None


# -------------------------
# Routes
# -------------------------

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    user = check_face()

    if user:
        return redirect(url_for('dashboard', username=user))
    else:
        return "<h2>Face Not Recognized. Try Again.</h2>"


@app.route('/dashboard/<username>')
def dashboard(username):
    return f"<h1>Welcome {username} 🎉 Facial Login Successful!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
