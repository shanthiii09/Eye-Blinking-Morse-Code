# Real-Time Blink-to-Speak Morse Code Translator  

This project implements a real-time Morse code translator using eye blinks. The system detects eye blinks through a webcam, calculates blink durations, and translates the pattern of blinks into corresponding Morse code and then into text.  

## Features  
- Detects eye blinks using a webcam.  
- Converts blink durations into Morse code (`.` for short blinks, `-` for long blinks).  
- Translates Morse code into text using a predefined dictionary.  
- Real-time feedback displayed on the video feed.  

---

## How It Works  
1. **Eye Aspect Ratio (EAR) Calculation**:  
   - The system calculates the EAR using facial landmarks to detect if the eye is open or closed.  
   - If EAR falls below a threshold, it identifies the eye as closed.  

2. **Blink Duration Classification**:  
   - Blinks shorter than 0.5 seconds are classified as `.` (dot).  
   - Blinks between 0.5 and 1.5 seconds are classified as `-` (dash).  

3. **Morse Code Translation**:  
   - The detected Morse code is matched to corresponding letters or numbers using a predefined Morse code dictionary.  

4. **Real-Time Output**:  
   - The system displays the detected Morse code and translated text in real-time on the video feed.  

---

## Installation  

### Prerequisites  
- Python 3.8 or higher.  
- A webcam for real-time blink detection.  

### Required Libraries  
Install the necessary libraries using:  
```bash  
pip install opencv-python dlib numpy scipy scikit-learn  
```  

### Additional Files  
Download the required facial landmark predictor file from [Dlib's shape predictor](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2). Extract the file and place it in the project directory.  

---

## Usage  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-username/real-time-morse-code-translator.git  
   cd real-time-morse-code-translator  
   ```  

2. Run the script:  
   ```bash  
   python real_time_morse.py  
   ```  

3. Look into the webcam and blink to form Morse code:  
   - Short blink (≤ 0.5 seconds): Dot (`.`).  
   - Long blink (> 0.5 and ≤ 1.5 seconds): Dash (`-`).  
   - Pause (> 3 seconds): Space between letters.  

4. Press `q` to quit the program.  

---

## Output Example  
- Blink Pattern: `... --- ...`  
- Morse Code: `SOS`  
- Translated Text: **SOS**  

---

## Troubleshooting  
1. **Webcam Not Detected**:  
   - Ensure your webcam is properly connected and accessible.  

2. **Dependencies Issues**:  
   - Check that all required libraries are installed.  

3. **Blink Not Detected**:  
   - Adjust the `EAR_THRESHOLD` or ensure proper lighting and position.  

---

## Credits  
- **OpenCV** for real-time video processing.  
- **Dlib** for facial landmark detection.  
- **Scipy** for spatial distance calculations.  
- **Morse Code Reference**: [Wikipedia](https://en.wikipedia.org/wiki/Morse_code).  

---



Let me know if you'd like me to help refine this or include additional details!
