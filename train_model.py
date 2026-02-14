import cv2
import os
import numpy as np

# Load Haarcascade
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

dataset_path = "dataset"

faces = []
labels = []
label_map = {}
label_id = 0

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)

    if not os.path.isdir(person_folder):
        continue

    label_map[label_id] = person_name

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)

        img = cv2.imread(image_path)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected_faces = cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in detected_faces:
            face = gray[y:y+h, x:x+w]
            faces.append(face)
            labels.append(label_id)

    label_id += 1

# Train LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))

# Save model
recognizer.save("face_model.yml")

print("Training Complete!")
