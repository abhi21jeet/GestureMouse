# GestureMouse — Vision-Based Hand Gesture Mouse Control

**A Computer Vision Project for Touch-Free Human–Computer Interaction**

## 1. Project Overview

GestureMouse is a Python-based application that enables users to control the computer mouse through hand gestures captured by a webcam. It uses computer vision and hand landmark detection to interpret finger movements and translate them into mouse operations such as cursor movement, clicking, dragging, and scrolling.

The project is developed using **OpenCV, MediaPipe, NumPy, and PyAutoGUI**. It provides a software-based alternative to conventional mouse interaction without requiring any additional hardware beyond a standard webcam.

The application is designed with a simple and modular structure, making it suitable for academic demonstrations, computer vision experimentation, and further development in gesture-based human–computer interaction.

## 2. Project Objectives

The primary objectives of GestureMouse are:

- To develop a real-time, vision-based mouse control system.
- To detect and interpret hand gestures using webcam input.
- To translate finger movements into accurate cursor positioning.
- To implement mouse operations through intuitive hand gestures.
- To reduce cursor instability using a smoothing mechanism.
- To provide a lightweight and accessible application using commonly available hardware.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Webcam access, frame capture, and image processing |
| MediaPipe | Real-time hand detection and landmark tracking |
| NumPy | Coordinate mapping and numerical operations |
| PyAutoGUI | Operating-system mouse control |
| Python `venv` | Isolated project environment |
| PyInstaller | Optional standalone Windows executable packaging |

## 4. System Requirements

### Hardware Requirements
- A computer running Windows, macOS, or Linux.
- A functional webcam, either built-in or external.
- At least 4 GB RAM recommended for basic operation.
- A functional display and standard desktop environment.

### Software Requirements
- Python 3.9–3.11, preferably a compatible 64-bit installation.
- Pip package manager.
- Webcam access permissions.
- Required Python dependencies listed in `requirements.txt`.

**Operating system note:** The core application is intended to be cross-platform. However, package compatibility, camera access, and mouse-control permissions may vary by operating system.

## 5. Project Structure

The project follows a minimal structure to simplify execution, maintenance, and evaluation.

```text
GestureMouse/
├── main.py              # Main application and gesture logic
├── requirements.txt     # Python dependencies
├── setup_and_run.bat    # Windows setup and launch script
└── README.md            # Project documentation
```

A local `venv/` directory may be created automatically during setup. It contains the isolated Python environment and does not need to be included in the source submission.

## 6. Installation and Execution

### Option A: Windows Quick Setup

1. Extract the GestureMouse project folder.
2. Ensure that a compatible Python installation is available.
3. Double-click `setup_and_run.bat`.
4. Allow the script to create the virtual environment and install the required dependencies.
5. Once initialization is complete, the application launches and opens the webcam window.

For subsequent executions, run the same batch file again. Existing environment setup is reused when available.

### Option B: Manual Installation

Open a terminal in the project directory and execute the following commands.

**Step 1: Create a virtual environment**

```bash
python -m venv venv
```

**Step 2: Activate the environment**

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

**Step 3: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Launch the application**

```bash
python main.py
```

The application initializes the webcam and begins real-time hand tracking. To exit, focus the camera window and press `q` or `Esc`.

## 7. Gesture Recognition and Mouse Operations

GestureMouse maps specific hand configurations to corresponding mouse operations.

| Operation | Gesture | Expected Behaviour |
|---|---|---|
| Cursor movement | Move the index fingertip within the active tracking zone | Moves the mouse cursor |
| Left click | Briefly pinch the thumb and index fingertips together | Performs a left click |
| Double click | Perform the pinch gesture twice within the configured time window | Performs a double click |
| Drag and drop | Hold the thumb and index fingertips together while moving the hand, then release | Holds and releases the mouse button |
| Right click | Bring the thumb and middle fingertips together | Performs a right click |
| Scrolling | Raise the index and middle fingers together and move the hand vertically | Scrolls the active window |

Gesture recognition depends on the thresholds and timing parameters configured in `main.py`. Consistent lighting, a clearly visible hand, and an appropriate distance from the webcam improve tracking reliability.

## 8. System Architecture and Working Methodology

GestureMouse follows a real-time processing pipeline that converts camera input into mouse actions.

### Processing Pipeline

```text
Webcam Input
     |
     v
Frame Capture using OpenCV
     |
     v
Hand Detection using MediaPipe
     |
     v
Hand Landmark Extraction
     |
     v
Gesture Recognition
     |
     v
Coordinate Mapping and Smoothing
     |
     v
Mouse Event Execution using PyAutoGUI
```

### Working Stages

**1. Image Acquisition**

OpenCV captures video frames from the webcam. The application uses a configurable resolution to balance processing speed and tracking accuracy.

**2. Hand Detection and Landmark Extraction**

MediaPipe detects the hand and identifies 21 landmark points representing important locations, including the wrist, finger joints, and fingertips.

**3. Gesture Interpretation**

The application evaluates fingertip distances and finger positions to identify gestures. For example, the distance between the thumb and index fingertips can be used to detect a pinch, while the positions of the index and middle fingers help identify the scrolling gesture.

**4. Coordinate Mapping**

The index fingertip's coordinates are mapped from a predefined active region of the camera frame to the computer screen dimensions. This allows a relatively small hand movement to control a larger screen area.

**5. Cursor Smoothing**

An Exponential Moving Average (EMA) filter reduces sudden cursor fluctuations caused by small, involuntary hand movements. The smoothing factor controls the balance between responsiveness and stability.

**6. Mouse Event Execution**

PyAutoGUI converts recognized gestures into mouse events, including movement, clicking, button holding, releasing, and scrolling.

## 9. Configuration and Customization

The main configuration parameters are grouped near the beginning of `main.py`. Their exact names and supported values depend on the implementation.

| Parameter | Function |
|---|---|
| `SMOOTHING_ALPHA` | Controls cursor smoothing and responsiveness |
| `PINCH_THRESHOLD` | Determines the fingertip distance used for pinch detection |
| `FRAME_MARGIN` | Defines the margins of the active tracking region |
| `CLICK_COOLDOWN` | Controls the minimum interval between eligible click events |
| `DOUBLE_CLICK_WINDOW` | Defines the time window for double-click recognition |
| `CAM_WIDTH` / `CAM_HEIGHT` | Set the webcam frame resolution |
| `CAM_INDEX` | Selects the camera device |

### Tuning Guidelines

- Reduce `SMOOTHING_ALPHA` if the cursor is unstable; increase it if smoother but slower movement is preferred.
- Adjust `PINCH_THRESHOLD` according to the camera distance and tracking conditions.
- Modify `FRAME_MARGIN` to change the effective cursor-control region.
- Tune the click timing parameters to reduce unintended clicks.
- Reduce the camera resolution if the application experiences performance issues.

The suggested adjustments should be tested against the actual implementation and the available hardware.

## 10. Performance Considerations

The application is designed to limit unnecessary processing while maintaining real-time interaction.

- A default camera resolution of 640 × 480 pixels helps control processing requirements.
- Tracking a single hand reduces the computational workload.
- Landmark-based gesture recognition avoids the need for a more complex full-body tracking pipeline.
- Cursor smoothing improves usability during continuous movement.
- Camera resolution and tracking parameters can be adjusted for systems with limited resources.

Actual CPU usage, memory consumption, and frame rate depend on the computer, webcam, Python environment, and installed library versions. Performance should be measured on the target system rather than assumed to be identical across devices.

## 11. Troubleshooting

| Issue | Possible Cause | Recommended Action |
|---|---|---|
| Webcam cannot be opened | Incorrect camera index, camera already in use, or missing permissions | Close other camera applications, verify `CAM_INDEX`, and enable camera access |
| Cursor does not move | Hand not detected or tracking conditions are poor | Improve lighting, keep the hand visible, and check application output |
| Cursor movement is unstable | Landmark fluctuations or insufficient smoothing | Adjust `SMOOTHING_ALPHA` |
| Clicks trigger unintentionally | Pinch threshold or timing settings are unsuitable | Tune `PINCH_THRESHOLD` and click timing parameters |
| MediaPipe installation fails | Unsupported Python version or incompatible package | Use a compatible 64-bit Python installation and verify dependency versions |
| Application runs slowly | Limited processing resources or excessive frame resolution | Reduce camera resolution and close unnecessary applications |
| Mouse control is restricted | Operating-system permissions or accessibility restrictions | Review the relevant permissions and application security settings |

## 12. Building a Standalone Windows Executable

PyInstaller can be used to package the application into a Windows executable, allowing distribution without requiring a separate Python installation on the target computer.

Activate the project virtual environment and install PyInstaller:

```bash
pip install pyinstaller
```

Build the executable:

```bash
pyinstaller --onefile --noconsole --name GestureMouse main.py
```

The generated executable is normally placed at:

```text
dist/GestureMouse.exe
```

The `--onefile` option packages the application into a single executable, while `--noconsole` suppresses the terminal window.

**Packaging considerations:**
- Test the executable on a clean Windows environment before distribution.
- Verify that MediaPipe model resources and other required dependencies are correctly bundled.
- Use a console-enabled build during debugging if startup errors need to be inspected.
- The executable may be considerably larger than the source code because of its bundled dependencies.
- Packaging does not guarantee compatibility with every Windows system.

## 13. Source Code Distribution

For academic submission or source-code sharing, distribute the project files without generated environments and build artifacts.

Recommended submission structure:

```text
GestureMouse/
├── main.py
├── requirements.txt
├── setup_and_run.bat
└── README.md
```

On Windows PowerShell, create a ZIP archive from the directory containing the project:

```powershell
Compress-Archive -Path GestureMouse -DestinationPath GestureMouse.zip -CompressionLevel Optimal
```

Before archiving, remove the `venv/`, `dist/`, and `build/` directories if they exist. These can be regenerated during installation or packaging.

## 14. Applications and Future Enhancements

GestureMouse demonstrates how computer vision can support alternative methods of human–computer interaction.

Potential application areas include:
- Touch-free desktop interaction.
- Academic demonstrations of computer vision and gesture recognition.
- Experimental accessibility-oriented interaction interfaces.
- Prototyping alternative input mechanisms for interactive systems.

Potential future enhancements include:
- Additional gestures for media and volume control.
- Keyboard shortcuts and window-management operations.
- A pause/resume gesture to temporarily disable tracking.
- Improved gesture classification and accidental-activation prevention.
- User-configurable gesture mappings.
- Enhanced tracking stability under varying lighting conditions.

These features are possible extensions and are not necessarily part of the current implementation.

## 15. Conclusion

GestureMouse demonstrates the integration of real-time computer vision, hand landmark detection, gesture interpretation, coordinate transformation, and operating-system mouse control in a single Python application.

By combining OpenCV, MediaPipe, NumPy, and PyAutoGUI, the project translates natural hand movements into practical desktop interactions without requiring specialized input hardware. Its compact architecture makes the implementation accessible for academic study while providing a foundation for further experimentation with gesture-based interfaces.

**Project focus:** Real-time computer vision, hand gesture recognition, and touch-free human–computer interaction.
