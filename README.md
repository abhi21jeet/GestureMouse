# GestureMouse 🖐️🖱️

Control your computer's mouse using just hand gestures in front of your webcam —
no extra hardware needed. Built with **OpenCV**, **MediaPipe**, and **PyAutoGUI**.

This project is intentionally kept simple (single `main.py` file, clearly
commented) so it's easy to read, modify, and explain — great for a college
mini-project / demo.

---

## 1. What You Need

- A laptop/PC with a **webcam** (built-in is fine).
- **Python 3.9 – 3.11** installed. (MediaPipe does not yet support the very
  latest Python versions, so avoid 3.12+.)
- Windows, macOS, or Linux — the Python code itself is cross-platform. The
  `.bat` script is for Windows one-click setup; Mac/Linux users can just run
  the manual commands in Section 3.

Check your Python version:
```
python --version
```

---

## 2. Quick Start (Windows — Easiest Way)

1. Unzip the project folder anywhere (e.g., Desktop).
2. Double-click **`setup_and_run.bat`**.
3. The first run will:
   - Create a local `venv` folder (a self-contained Python environment, so
     this project's packages never mess with other projects on your PC).
   - Install all required packages automatically.
   - Launch the app and open your webcam window.
4. To run it again later, just double-click `setup_and_run.bat` again — setup
   will be skipped since `venv` already exists, so it starts instantly.
5. Press **`q`** or **`ESC`** inside the camera window to quit.

---

## 3. Manual Setup (Windows / macOS / Linux)

If you're not on Windows, or prefer typing commands yourself:

```bash
# 1. Go into the project folder
cd GestureMouse

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python main.py
```

---

## 4. Gesture Cheat Sheet

| Gesture | What to do | Result |
| :--- | :--- | :--- |
| **Move cursor** | Move your **index finger** inside the green box shown on screen | Cursor follows your fingertip |
| **Left click** | Quickly touch **thumb tip** to **index tip** and release | Single left click |
| **Double click** | Do the pinch gesture **twice quickly** (within ~0.35s) | Double click |
| **Drag & Drop** | **Hold** thumb + index pinched together, then move your hand, then release | Click-and-drag |
| **Right click** | Touch **thumb tip** to **middle finger tip** | Single right click |
| **Scroll** | Hold **index + middle fingers up and together**, move hand up/down | Scrolls the active window |

**Tip:** Keep your hand roughly 30–60 cm from the webcam, with good lighting,
for the most reliable tracking. The green rectangle on screen is your
"active zone" — you only need to move your finger within that box to reach
the whole screen, so you don't have to stretch your arm to the frame edges.

---

## 5. Tuning / Customization

All the important settings are grouped at the top of `main.py` under
**"1. CONFIGURATION"**. A few you might want to play with:

- `SMOOTHING_ALPHA` — lower this (e.g. `0.1`) if the cursor feels jittery;
  raise it (e.g. `0.4`) if it feels laggy.
- `PINCH_THRESHOLD` — lower this if clicks trigger too easily by accident;
  raise it if you find it hard to trigger a click at all.
- `FRAME_MARGIN` — controls the size of the active tracking zone.
- `CLICK_COOLDOWN` / `DOUBLE_CLICK_WINDOW` — timing windows for click
  detection, in seconds.

---

## 6. Performance Notes

- Runs comfortably within ~250–300MB RAM and low CPU usage on modest
  hardware (dual-core CPU, 4–8GB RAM, integrated graphics) because:
  - Camera capture is kept at a modest 640x480 resolution.
  - MediaPipe's lightweight hand-tracking model (`max_num_hands=1`) is used
    instead of heavier full-body/multi-hand models.
  - No unnecessary image copies or extra processing are done per frame.
- If you experience lag on very old hardware, try lowering
  `CAM_WIDTH`/`CAM_HEIGHT` in `main.py` to `480x360`.

---

## 7. Packaging as a Standalone Windows `.exe` (Optional)

If you want to share the app with someone who doesn't have Python
installed, you can freeze it into a single `.exe` using **PyInstaller**.

```bash
# 1. Activate your venv first (see Section 3)
# 2. Install PyInstaller
pip install pyinstaller

# 3. Build the executable
pyinstaller --onefile --noconsole --name GestureMouse main.py
```

- The finished `.exe` will appear inside a new `dist/` folder as
  `dist/GestureMouse.exe`.
- `--onefile` bundles everything into a single executable file.
- `--noconsole` hides the black terminal window (remove this flag while
  testing if you want to see error messages/logs).
- Double-clicking `GestureMouse.exe` on a Windows machine will run the app
  directly — no Python installation required on that machine.

**Note:** MediaPipe bundles fairly large model files, so the resulting
`.exe` may be 150–300MB. This is normal.

---

## 8. Packaging the Project Folder for Submission

To share the source project (not the `.exe`), zip up the folder while
**excluding** the `venv/` and `dist/`/`build/` folders (they're large and
regenerated automatically):

```bash
# From one level above the GestureMouse folder:
# Windows (PowerShell):
Compress-Archive -Path GestureMouse -DestinationPath GestureMouse.zip -CompressionLevel Optimal
```

Or simply, in File Explorer: right-click the `GestureMouse` folder →
"Send to" → "Compressed (zipped) folder" — just delete the `venv`, `dist`,
and `build` folders first if they exist, since a grader can always
regenerate them via `setup_and_run.bat`.

**Recommended files to include in your submission ZIP:**
```
GestureMouse/
├── main.py
├── requirements.txt
├── setup_and_run.bat
└── README.md
```

---

## 9. Troubleshooting

| Problem | Likely Fix |
| :--- | :--- |
| `Could not open the webcam` | Close other apps using the camera (Zoom/Teams/Skype); check `CAM_INDEX` is `0`; check Windows camera privacy settings allow desktop apps to use the camera. |
| Cursor doesn't move | Make sure your whole hand is visible in frame with decent lighting; check the console for "hand detected" — try moving closer/farther from camera. |
| Clicks trigger too often / not enough | Adjust `PINCH_THRESHOLD` in `main.py` (see Section 5). |
| `pip install` fails on `mediapipe` | Make sure you're using Python 3.9–3.11 (not 3.12+ or 3.8-), 64-bit. |
| App is laggy | Lower `CAM_WIDTH`/`CAM_HEIGHT`, ensure no other heavy apps are running, or reduce webcam resolution in `main.py`. |

---

## 10. How It Works (For Your Viva/Presentation)

1. **Capture:** OpenCV grabs frames from the webcam.
2. **Detect:** MediaPipe's Hands model finds 21 landmark points per hand
   (fingertips, joints, wrist) from each frame.
3. **Interpret:** We measure distances between specific landmarks (e.g.
   thumb tip ↔ index tip) to recognize gestures like pinch (click), or
   check finger positions relative to knuckles for gestures like scroll.
4. **Map:** The index fingertip's position inside a defined "active zone"
   is linearly interpolated (`np.interp`) to full screen coordinates.
5. **Smooth:** An Exponential Moving Average filter smooths out natural
   hand tremors so the cursor doesn't jitter.
6. **Act:** PyAutoGUI translates the recognized gesture into a real OS-level
   mouse event (move / click / drag / scroll).

Enjoy, and feel free to extend it — e.g. add gestures for volume control,
window switching (Alt+Tab), or a "pause tracking" hand pose!
