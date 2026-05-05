# AI-Based Driver Drowsiness & Distraction Detection System

## Overview
This is a real-time drowsiness detection system that uses computer vision to monitor a driver's eyes and alert them when signs of drowsiness are detected. The system uses OpenCV for face and eye detection and generates an audio alarm when the driver's eyes are closed.

## Features
- **Real-time Eye Detection**: Uses OpenCV cascade classifiers to detect faces and eyes in video stream
- **Brightness-based Analysis**: Detects eye closure by analyzing the brightness level of detected eye regions
- **Audio Alert**: Plays an alarm sound when drowsiness is detected
- **Live Status Display**: Shows real-time "OPEN" or "CLOSED" status on the video feed
- **Face and Eye Visualization**: Displays detection boxes on the video stream

## Requirements
- Python 3.8 or higher
- OpenCV (`opencv-python`)
- NumPy (`numpy`)
- playsound (`playsound`)

## Installation

### 1. Clone or Download the Project
```bash
cd "D:\AI-Based Driver Drowsiness & Distraction Detection System"
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install opencv-python numpy playsound
```

## Running the System

### Start the Application
```bash
python main.py
```

The system will:
1. Open your webcam
2. Display a window with face and eye detection
3. Show "Status: OPEN" in green when eyes are open
4. Show "Status: CLOSED" in red when eyes are closed
5. Play an alarm sound when eyes are closed for ~5 frames (~150ms)

### Exit the Application
Press **ESC** key to stop the system and close the window.

## How It Works

### Detection Algorithm
1. **Face Detection**: Uses Haar Cascade classifier to detect faces in the video stream
2. **Eye Detection**: Detects eyes within the detected face region
3. **Eye State Analysis**: Analyzes the brightness of the detected eye region:
   - **Open eye**: High brightness (~100-180)
   - **Closed eye**: Low brightness (~5-50)
4. **Drowsiness Trigger**: Increments drowsy counter when eyes are closed or not detected
5. **Alarm Activation**: Triggers alarm when counter reaches threshold (5 frames)

### Visual Indicators
- **Blue Rectangle**: Face detection boundary
- **Green Rectangle**: Eye detection boundary
- **Green "Status: OPEN"**: Eyes are open
- **Red "Status: CLOSED"**: Eyes are closed
- **Red "DROWSY ALERT!"**: Alarm activated

## Configuration

You can adjust the system sensitivity by modifying these parameters in `main.py`:

```python
# Brightness threshold for detecting open eyes (lower = more sensitive)
return avg_brightness > 40

# Frames to trigger alarm (lower = faster trigger)
FRAME_THRESHOLD = 5  

# Alarm sound file path
alarm_path = 'alarm.wav'
```

## Files
- `main.py` - Main application script
- `alarm.wav` - Audio alarm sound file
- `README.md` - This documentation file

## Troubleshooting

### Issue: Camera not detected
- Ensure your webcam is connected and not in use by another application
- Check camera permissions in system settings

### Issue: Eyes not detected
- Ensure adequate lighting
- Position face directly toward camera
- Avoid sunglasses or large items covering eyes

### Issue: False alarms
- Adjust `FRAME_THRESHOLD` (increase to reduce sensitivity)
- Adjust brightness threshold in `detect_eyes_open()` function

### Issue: Alarm not playing
- Verify `alarm.wav` file exists in the project directory
- Check system volume settings
- System will fall back to a system beep if audio file fails

## Future Enhancements
- Add head position detection
- Implement gaze direction tracking
- Add distraction detection (looking away from road)
- Save detection logs and reports
- Add timestamps to alert events
- Support for multiple detection metrics

## License
This project is provided as-is for educational and safety purposes.

## Safety Notice
⚠️ **This system should be used as a supplementary safety tool only and not as a replacement for proper rest while driving. Always maintain alertness while operating a vehicle.**
