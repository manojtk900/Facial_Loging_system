from flask import Flask, render_template, Response
import cv2
import os

app = Flask(__name__)

# -----------------------------
# Load Haarcascade
# -----------------------------
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# -----------------------------
# Load Trained Model
# -----------------------------
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face_model.yml")

# -----------------------------
# Load Label Names
# -----------------------------
dataset_path = "dataset"
label_map = {}
label_id = 0

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)
    if os.path.isdir(person_folder):
        label_map[label_id] = person_name
        label_id += 1


# -----------------------------
# Webcam Generator
# -----------------------------
def generate_frames():
    camera = cv2.VideoCapture(0)

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
                name = label_map.get(label, "Unknown")
            else:
                name = "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
