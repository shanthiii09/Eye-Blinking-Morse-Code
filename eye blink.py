import cv2
import dlib
import numpy as np
from scipy.spatial import distance
from sklearn.svm import SVC
import time

# Constants for blink classification
EAR_THRESHOLD = 0.2
DOT_TIME = 0.5  # 0.5 seconds for dot
DASH_TIME = 1.0  # 1.5 seconds for dash
SPACE_TIME = 3.0  # 3 seconds for space (pause between letters)
FRAME_RATE = 30  # Approx. webcam frame rate

# Morse Code to Text Dictionary
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9'
}

# Calculate Eye Aspect Ratio (EAR)
def calculate_ear(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Initialize Dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Real-time Blink Detection and Morse Code Translation
def real_time_morse():
    print("Starting real-time Morse code detection... Press 'q' to stop.")
    cap = cv2.VideoCapture(0)
    blink_start = None
    blinking = False
    last_blink_time = time.time()
    morse_sequence = ""
    translated_text = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = landmark_predictor(gray, face)

            # Get coordinates of left and right eye
            left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
            right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])

            # Calculate EAR for both eyes
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

                    print(f"Blink Duration: {blink_duration:.2f} seconds")  # Debugging output

                    if blink_duration <= DOT_TIME:
                        morse_sequence += '.'
                        print("Detected: Dot (.)")
                    elif blink_duration <= DASH_TIME:
                        morse_sequence += '-'
                        print("Detected: Dash (-)")

                    last_blink_time = time.time()

        # Check for space (pause between Morse code sequences)
        if time.time() - last_blink_time > SPACE_TIME:
            if morse_sequence:
                # Translate Morse to Text
                translated_char = MORSE_CODE_DICT.get(morse_sequence, "?")
                translated_text += translated_char
                print(f"Morse: {morse_sequence} | Translated: {translated_char}")
                morse_sequence = ""

        # Display the frame with text
        cv2.putText(frame, f"Morse: {morse_sequence}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"Translator: {translated_text}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Blink to Speak", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Call the real-time detection function
real_time_morse()