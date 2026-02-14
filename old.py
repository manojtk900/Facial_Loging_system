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


camera = cv2.VideoCapture(0)
recognized_user = None


def generate_frames():
    global recognized_user

    while True:
        success, frame = camera.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face)

            if confidence < 80:
                name = label_map.get(label)
                recognized_user = name
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame, "Login Success!", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                cv2.putText(frame, "Scanning...", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def home():
    return render_template("login.html")


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/check_login')
def check_login():
    global recognized_user
    if recognized_user:
        user = recognized_user
        recognized_user = None
        return redirect(url_for('dashboard', username=user))
    return ""


@app.route('/dashboard/<username>')
def dashboard(username):
    return f"<h1>Welcome {username} 🎉 Facial Login Successful!</h1>"


if __name__ == "__main__":
    app.run(debug=True)
