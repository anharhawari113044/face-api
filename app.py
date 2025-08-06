from flask import Flask, request, jsonify
from flask_cors import CORS  # ⬅️ Tambahkan ini
import face_recognition
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # ⬅️ Aktifkan CORS

known_face_encodings = []
known_face_names = []

def load_known_faces():
    for filename in os.listdir("known_faces"):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image = face_recognition.load_image_file(f"known_faces/{filename}")
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_face_encodings.append(encoding[0])
                known_face_names.append(os.path.splitext(filename)[0])

load_known_faces()

@app.route('/api/recognize', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image = face_recognition.load_image_file(file)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        return jsonify({"nama": "Wajah tidak terdeteksi"}), 404

    encoding = face_encodings[0]
    distances = face_recognition.face_distance(known_face_encodings, encoding)

    if len(distances) == 0:
        return jsonify({"nama": "Tidak Dikenali"})

    min_distance = min(distances)
    min_index = distances.tolist().index(min_distance)

    if min_distance < 0.6:
        return jsonify({
            "nama": known_face_names[min_index],
            "jarak": round(float(min_distance), 4)
        })
    else:
        return jsonify({
            "nama": "Tidak Dikenali",
            "jarak": round(float(min_distance), 4)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # ⬅️ port ditentukan eksplisit
