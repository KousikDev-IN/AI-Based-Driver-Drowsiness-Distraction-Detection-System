import cv2
import numpy as np
import threading
import time
import os
import winsound
from playsound import playsound

# Load cascade classifiers for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to detect if eyes are open
def detect_eyes_open(eye_roi):
    """Detect if eyes are open by checking brightness"""
    if eye_roi.size == 0:
        return False
    
    # Convert to grayscale
    gray = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2GRAY)
    
    # Open eyes are brighter than closed eyes
    avg_brightness = np.mean(gray)
    
    # If average brightness is high, eye is open
    # Closed eyes are very dark (~5-40), Open eyes are brighter (~100-180)
    return avg_brightness > 40

# Alarm function using alarm.wav file
def play_alarm():
    alarm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alarm.wav')
    try:
        if os.path.exists(alarm_path):
            playsound(alarm_path)
        else:
            # Fallback to system beep if file not found
            winsound.Beep(1000, 500)
    except Exception as e:
        # Fallback to system beep on error
        try:
            winsound.Beep(1000, 500)
        except:
            pass

# Start webcam
cap = cv2.VideoCapture(0)

drowsy_counter = 0
FRAME_THRESHOLD = 5  # Very sensitive - trigger quickly
alarm_on = False
last_alarm_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    eyes_open_count = 0
    eyes_detected_count = 0
    face_detected = False
    brightness_values = []
    
    for (x, y, w, h) in faces:
        face_detected = True
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        
        # Detect eyes within face region
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4)
        eyes_detected_count += len(eyes)
        
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            
            # Check if eye is open
            eye_roi = roi_color[ey:ey + eh, ex:ex + ew]
            eye_gray = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(eye_gray)
            brightness_values.append(brightness)
            
            if detect_eyes_open(eye_roi):
                eyes_open_count += 1
    
    # Update drowsy counter
    # Eyes are considered OPEN only if:
    # 1. Face is detected
    # 2. Both eyes (2) are detected
    # 3. Both eyes are bright (open)
    # If any condition fails, increment drowsy counter
    
    if face_detected and eyes_detected_count >= 2 and eyes_open_count >= 2:
        # Eyes are open - reset counter
        drowsy_counter = 0
        alarm_on = False
    else:
        # Eyes are closed or not detected - increment counter
        drowsy_counter += 1
    
    # Trigger alarm if drowsy for enough frames
    if drowsy_counter >= FRAME_THRESHOLD:
        cv2.putText(frame, "DROWSY ALERT!", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        
        # Play alarm sound repeatedly every 1 second
        current_time = time.time()
        if not alarm_on or (current_time - last_alarm_time >= 1.0):
            alarm_on = True
            last_alarm_time = current_time
            threading.Thread(target=play_alarm).start()
    
    # Display status text only
    status_text = "OPEN" if drowsy_counter == 0 else "CLOSED"
    cv2.putText(frame, f"Status: {status_text}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0) if drowsy_counter == 0 else (0, 0, 255), 2)
    
    cv2.imshow("Driver Drowsiness Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()