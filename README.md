# 🖐️ AirCursor

AirCursor is a computer vision-based contactless gesture control system that turns your webcam into an **air mouse** — allowing you to control your computer using **just your hands**. Leveraging **MediaPipe**, **OpenCV**, and **PyAutoGUI**, this project enables:

- **Smooth Pointer Movement**
- **Scroll Gestures**
- **Click Gestures**
- **Exit Gesture by Joining Both Hands**

> ✨ Say goodbye to the physical mouse and interact with your system in a futuristic, intuitive way.

---

## 🎯 Features

- 🖱️ **Pointer Mode**  
  Raise only your **index finger (right hand)** to move the mouse pointer.

- 🔄 **Scroll Mode**  
  Raise **index and middle fingers (right hand)** to scroll vertically.

- 👆 **Click Mode**  
  Make a **fist with your left hand** to perform a left-click.

- 🙌 **Exit Gesture**  
  **Bring both hands close together** (index fingertips) to exit the application instantly.

---

## 🛠️ Tech Stack

- Python 🐍
- OpenCV 🎥
- MediaPipe 🤖
- PyAutoGUI 🖱️

---

## ⚙️ How It Works

1. Capture webcam feed using OpenCV.
2. Detect hands using MediaPipe and determine their handedness (left/right).
3. Track landmark positions and classify gestures (e.g., index finger up, fist, etc.).
4. Translate gestures into screen actions using PyAutoGUI.
5. Ensure smooth movement using adjustable **smoothing** and **scaling factors**.

---

## 📦 Installation

```bash
pip install opencv-python mediapipe pyautogui
