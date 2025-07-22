from flask import Flask, render_template, Response
import cv2
import time
import dlib
import numpy as np
from scipy.spatial import distance

# Constants
EAR_THRESHOLD = 0.2
DOT_TIME = 0.5
DASH_TIME = 1.0
SPACE_TIME = 3.0

# Morse Code Dictionary
MORSE_CODE_DICT = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E", "..-.": "F",
    "--.": "G", "....": "H", "..": "I", ".---": "J", "-.-": "K", ".-..": "L",
    "--": "M", "-.": "N", "---": "O", ".--.": "P", "--.-": "Q", ".-.": "R",
    "...": "S", "-": "T", "..-": "U", "...-": "V", ".--": "W", "-..-": "X",
    "-.--": "Y", "--..": "Z"
}

# Load dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor_path = "C:\\Users\\DELL\\OneDrive\\Pictures\\Screenshots\\eye\\blink\\shape_predictor_68_face_landmarks.dat"


try:
    landmark_predictor = dlib.shape_predictor(predictor_path)
except RuntimeError as e:
    print(f"Error loading landmark predictor: {e}")
    print("Ensure the path to 'shape_predictor_68_face_landmarks.dat' is correct.")
    exit(1)

# Flask app setup
app = Flask(__name__)

camera = None
is_running = False
morse_sequence = ""
translated_text = ""

def calculate_ear(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def generate_frames():
    global camera, is_running, morse_sequence, translated_text

    blink_start = None
    blinking = False
    last_blink_time = time.time()

    while is_running:
        ret, frame = camera.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) == 0:
            cv2.putText(frame, "No faces detected!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            for face in faces:
                landmarks = landmark_predictor(gray, face)

                # Get eye landmarks
                left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
                right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])

                left_ear = calculate_ear(left_eye)
                right_ear = calculate_ear(right_eye)
                ear = (left_ear + right_ear) / 2.0

                if ear < EAR_THRESHOLD:
                    if not blinking:
                        blink_start = time.time()
                        blinking = True
                else:
                    if blinking:
                        blink_end = time.time()
                        blink_duration = blink_end - blink_start
                        blinking = False

                        if blink_duration <= DOT_TIME:
                            morse_sequence += '.'
                        elif blink_duration <= DASH_TIME:
                            morse_sequence += '-'

                        last_blink_time = time.time()

        # Handle pauses and translation
        if time.time() - last_blink_time > SPACE_TIME:
            if morse_sequence:
                translated_char = MORSE_CODE_DICT.get(morse_sequence, "?")
                translated_text += translated_char
                print(f"Morse: {morse_sequence} | Translated: {translated_char}")
                morse_sequence = ""

        # Display information on the frame
        cv2.putText(frame, f"Morse: {morse_sequence}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"Translation: {translated_text}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            for n in range(36, 48):
                x, y = landmarks.part(n).x, landmarks.part(n).y
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

        # Encode the frame and send it as a response
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video_feed():
    global camera, is_running
    if not is_running:
        camera = cv2.VideoCapture(0)
        is_running = True
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop_camera():
    global camera, is_running
    if camera:
        is_running = False
        camera.release()
        camera = None
    return "Camera stopped"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) 