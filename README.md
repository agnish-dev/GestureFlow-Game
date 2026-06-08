# GestureFlow Game

**GestureFlow Game** is an interactive, computer-vision based controller that lets you play the web version of Subway Surfers using only hand gestures. It uses your webcam to track your hand movements in real-time, mapping specific finger counts to in-game actions like jumping, sliding, and dodging left or right.

## 🚀 Features

- **Zero-Setup Play**: No need to install Python or dependencies. Just download the executable and play!
- **Auto-Launch**: Automatically opens the Subway Surfers website in your default browser.
- **Real-Time Hand Tracking**: Powered by Google's MediaPipe for fast and accurate hand detection.
- **Intuitive Controls**: Maps natural finger gestures to keyboard arrow keys seamlessly.

## 🎮 How to Play

1. Download the latest `Play Game.exe` from the **Releases** section.
2. Double-click the downloaded file to run it.
3. Your default web browser will automatically open the Subway Surfers web game.
4. A webcam window will pop up. Bring your hand into the frame and use the gestures below to control your character!

### 🖐️ Gesture Controls

- **1 Finger:** Move Left (Left Arrow)
- **2 Fingers:** Move Right (Right Arrow)
- **3 Fingers:** Slide / Roll (Down Arrow)
- **5 Fingers (Open Hand):** Jump (Up Arrow)

*(Make sure to keep your hand stable for a brief moment for the gesture to register accurately!)*

## 🛠️ Built With

- **Python**: Core programming language.
- **OpenCV (`cv2`)**: For accessing the webcam and displaying the live video feed.
- **MediaPipe**: For advanced, real-time hand landmark detection and tracking.
- **Keyboard Module**: For simulating hardware keystrokes to control the game.
- **PyInstaller**: For packaging the entire Python environment into a single, easy-to-distribute `.exe` file.

## 💻 For Developers

If you want to run the source code yourself or modify the gestures:

1. Clone this repository.
2. Ensure you have Python installed.
3. Install the required dependencies:
   ```bash
   pip install opencv-python mediapipe keyboard
   ```
4. Run the main script:
   ```bash
   python main.py
   ```

To build your own executable:
```bash
pyinstaller main.spec --clean -y
```

## ⚠️ Notes

- Ensure you are in a well-lit environment for optimal hand tracking.
- The program requires camera permissions to function correctly. If the webcam does not turn on, check your OS privacy settings to ensure desktop apps are allowed to access the camera.
- Press **'q'** while focused on the webcam window to exit the application completely.
