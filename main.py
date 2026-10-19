"""
GestureMouse - Control your mouse with hand gestures using a webcam
======================================================================
A beginner-friendly computer vision project built with OpenCV + MediaPipe.

HOW IT WORKS (big picture):
1. We read frames from your webcam using OpenCV.
2. MediaPipe looks at each frame and finds 21 points ("landmarks") on your
   hand (fingertips, knuckles, wrist, etc).
3. We look at the distance between certain fingertips to decide what
   gesture you are making (move / click / drag / scroll).
4. We use PyAutoGUI to actually move the mouse / click / scroll on your PC.

Run with:  python main.py
Quit with: press 'q' or ESC while the camera window is focused.
"""

import time
import math

import cv2
import numpy as np
import mediapipe as mp
import pyautogui

# ----------------------------------------------------------------------
# 1. CONFIGURATION  (tweak these numbers if the app feels too fast/slow)
# ----------------------------------------------------------------------

CAM_INDEX = 0                # 0 = default/built-in webcam
CAM_WIDTH, CAM_HEIGHT = 640, 480

FRAME_MARGIN = 100           # px margin inside the webcam frame that counts
                              # as the "active zone" your finger moves in.
                              # A smaller margin = you can reach screen edges
                              # more easily (less hand travel needed).

SMOOTHING_ALPHA = 0.2         # 0-1. Lower = smoother but laggier cursor.
                               # Higher = snappier but jittery cursor.

PINCH_THRESHOLD = 0.045       # normalized distance (0-1). Smaller value =
                               # you must pinch fingers closer together to
                               # trigger a click.

CLICK_COOLDOWN = 0.3          # seconds between two allowed clicks
DOUBLE_CLICK_WINDOW = 0.35    # seconds allowed between 2 pinches for a
                               # "double click" to register

SCROLL_SPEED = 25             # how many "scroll units" per frame of motion

# Safety: don't let pyautogui panic-abort when cursor hits a screen corner
pyautogui.FAILSAFE = False
# Slightly speeds up pyautogui actions (no artificial delay after each call)
pyautogui.PAUSE = 0

# ----------------------------------------------------------------------
# 2. SETUP: camera, MediaPipe hands model, screen size
# ----------------------------------------------------------------------

SCREEN_W, SCREEN_H = pyautogui.size()
print(f"Detected screen resolution: {SCREEN_W}x{SCREEN_H}")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,   # False = video stream mode (faster, uses tracking)
    max_num_hands=1,            # we only need ONE hand for a mouse
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
)

cap = cv2.VideoCapture(CAM_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

if not cap.isOpened():
    raise RuntimeError(
        "Could not open the webcam. Check CAM_INDEX or close other apps "
        "that might be using the camera (Zoom, Teams, etc)."
    )

# Landmark IDs we care about (see MediaPipe hand landmark reference)
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12

# ----------------------------------------------------------------------
# 3. STATE VARIABLES (things that change frame-to-frame)
# ----------------------------------------------------------------------

prev_screen_x, prev_screen_y = SCREEN_W // 2, SCREEN_H // 2  # smoothed cursor pos
is_dragging = False
last_click_time = 0.0
last_pinch_time = 0.0
prev_scroll_y = None
current_state = "IDLE"

prev_frame_time = time.time()


# ----------------------------------------------------------------------
# 4. HELPER FUNCTIONS
# ----------------------------------------------------------------------

def landmark_pixel(landmark, frame_w, frame_h):
    """Convert a MediaPipe normalized landmark (0-1 range) into pixel
    coordinates for the given frame size."""
    return int(landmark.x * frame_w), int(landmark.y * frame_h)


def normalized_distance(lm1, lm2):
    """Euclidean distance between two MediaPipe landmarks, using their
    normalized (0-1) x/y coordinates. This keeps the threshold independent
    of camera resolution or how far your hand is from the camera."""
    return math.hypot(lm1.x - lm2.x, lm1.y - lm2.y)


def map_to_screen(x_px, y_px, frame_w, frame_h):
    """Map a point from the 'active zone' inside the camera frame to full
    screen coordinates, using linear interpolation."""
    screen_x = np.interp(
        x_px, [FRAME_MARGIN, frame_w - FRAME_MARGIN], [0, SCREEN_W]
    )
    screen_y = np.interp(
        y_px, [FRAME_MARGIN, frame_h - FRAME_MARGIN], [0, SCREEN_H]
    )
    return int(screen_x), int(screen_y)


def draw_hud(frame, state, fps):
    """Draw the on-screen dashboard: active zone box, state text, FPS."""
    h, w, _ = frame.shape

    # Semi-transparent active zone rectangle
    overlay = frame.copy()
    cv2.rectangle(
        overlay,
        (FRAME_MARGIN, FRAME_MARGIN),
        (w - FRAME_MARGIN, h - FRAME_MARGIN),
        (0, 255, 0),
        2,
    )
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # State text (top-left, neon green)
    cv2.putText(
        frame, f"STATE: {state}", (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (57, 255, 20), 2,
    )

    # FPS counter (top-right)
    fps_text = f"FPS: {int(fps)}"
    text_size = cv2.getTextSize(fps_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
    cv2.putText(
        frame, fps_text, (w - text_size[0] - 20, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (57, 255, 20), 2,
    )


# ----------------------------------------------------------------------
# 5. MAIN LOOP
# ----------------------------------------------------------------------

print("GestureMouse is starting... press 'q' or ESC in the camera window to quit.")

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to read frame from webcam. Exiting.")
        break

    # Mirror the frame so movement feels natural (like looking in a mirror)
    frame = cv2.flip(frame, 1)
    frame_h, frame_w, _ = frame.shape

    # MediaPipe expects RGB images, OpenCV gives us BGR by default
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_state = "IDLE"

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        lm = hand_landmarks.landmark
        index_x, index_y = landmark_pixel(lm[INDEX_TIP], frame_w, frame_h)
        middle_x, middle_y = landmark_pixel(lm[MIDDLE_TIP], frame_w, frame_h)

        # Distances used to detect gestures
        pinch_dist = normalized_distance(lm[THUMB_TIP], lm[INDEX_TIP])
        right_click_dist = normalized_distance(lm[THUMB_TIP], lm[MIDDLE_TIP])
        index_middle_dist = normalized_distance(lm[INDEX_TIP], lm[MIDDLE_TIP])

        now = time.time()

        # --- SCROLL GESTURE: index + middle fingers up & close together ---
        fingers_together = index_middle_dist < 0.06
        # "up together" roughly means both tips are above their middle
        # knuckles (landmark 6 for index, 10 for middle)
        fingers_up = lm[INDEX_TIP].y < lm[6].y and lm[MIDDLE_TIP].y < lm[10].y

        if fingers_together and fingers_up:
            current_state = "SCROLLING"
            avg_y = (index_y + middle_y) / 2
            if prev_scroll_y is not None:
                delta = prev_scroll_y - avg_y
                if abs(delta) > 2:  # ignore tiny noise
                    pyautogui.scroll(int(delta * (SCROLL_SPEED / 20)))
            prev_scroll_y = avg_y

        else:
            prev_scroll_y = None

            # --- DRAG / LEFT CLICK (pinch thumb + index) ---
            if pinch_dist < PINCH_THRESHOLD:
                if not is_dragging:
                    # Just started pinching -> could be a click or a drag
                    if now - last_pinch_time < DOUBLE_CLICK_WINDOW:
                        pyautogui.doubleClick()
                        current_state = "DOUBLE CLICK"
                        last_pinch_time = 0  # reset so we don't triple-trigger
                    else:
                        pyautogui.mouseDown()
                        is_dragging = True
                        last_pinch_time = now
                        current_state = "DRAGGING"
                else:
                    current_state = "DRAGGING"

                # Move cursor while pinched (covers both click-hold and drag)
                screen_x, screen_y = map_to_screen(index_x, index_y, frame_w, frame_h)
                smooth_x = prev_screen_x + SMOOTHING_ALPHA * (screen_x - prev_screen_x)
                smooth_y = prev_screen_y + SMOOTHING_ALPHA * (screen_y - prev_screen_y)
                pyautogui.moveTo(smooth_x, smooth_y)
                prev_screen_x, prev_screen_y = smooth_x, smooth_y

            else:
                # Released the pinch
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False
                    current_state = "IDLE"

                # --- RIGHT CLICK (pinch thumb + middle) ---
                elif right_click_dist < PINCH_THRESHOLD:
                    if now - last_click_time > CLICK_COOLDOWN:
                        pyautogui.click(button="right")
                        last_click_time = now
                    current_state = "RIGHT CLICK"

                # --- PLAIN CURSOR MOVEMENT ---
                else:
                    current_state = "MOVING"
                    screen_x, screen_y = map_to_screen(index_x, index_y, frame_w, frame_h)
                    smooth_x = prev_screen_x + SMOOTHING_ALPHA * (screen_x - prev_screen_x)
                    smooth_y = prev_screen_y + SMOOTHING_ALPHA * (screen_y - prev_screen_y)
                    pyautogui.moveTo(smooth_x, smooth_y)
                    prev_screen_x, prev_screen_y = smooth_x, smooth_y

    else:
        # No hand visible: release any drag in progress so it doesn't get stuck
        if is_dragging:
            pyautogui.mouseUp()
            is_dragging = False

    # ---- FPS calculation ----
    curr_frame_time = time.time()
    fps = 1 / (curr_frame_time - prev_frame_time) if curr_frame_time != prev_frame_time else 0
    prev_frame_time = curr_frame_time

    draw_hud(frame, current_state, fps)
    cv2.imshow("GestureMouse Controller - Active Session", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # 27 = ESC key
        break

# ----------------------------------------------------------------------
# 6. CLEANUP
# ----------------------------------------------------------------------
if is_dragging:
    pyautogui.mouseUp()

cap.release()
cv2.destroyAllWindows()
hands.close()
print("GestureMouse closed. Bye!")
