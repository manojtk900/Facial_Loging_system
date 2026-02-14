from flask import Flask, render_template, Response
import cv2
import os
import time

app = Flask(__name__)

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

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

scan_start = None
authenticated_user = None


def generate_frames():
    global scan_start, authenticated_user

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
                if scan_start is None:
                    scan_start = time.time()

                elapsed = time.time() - scan_start

                if elapsed > 2:
                    authenticated_user = label_map.get(label)

                    # GREEN BOX
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)

                    # TICK
                    cx = x + w//2
                    cy = y + h//2
                    cv2.line(frame, (cx-20, cy), (cx-5, cy+20), (0,255,0), 4)
                    cv2.line(frame, (cx-5, cy+20), (cx+25, cy-15), (0,255,0), 4)

                    cv2.putText(frame, "Authenticated",
                                (x, y-15),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0,255,0), 2)

                    camera.release()
                    break
                else:
                    # RED SCAN
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 3)
                    cv2.putText(frame, "Scanning...",
                                (x, y-15),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0,0,255), 2)
            else:
                scan_start = None

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


@app.route('/status')
def status():
    global authenticated_user
    if authenticated_user:
        user = authenticated_user
        authenticated_user = None
        return user
    return ""


if __name__ == "__main__":
    app.run(debug=True)
