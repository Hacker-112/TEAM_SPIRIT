import cv2
import numpy as np
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import threading

MODEL_PATH = "face_landmarker.task"

# ---------------- MODEL ----------------
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1
)

face_landmarker = vision.FaceLandmarker.create_from_options(options)

# ---------------- GLOBAL SESSION DATA ----------------
_session_running = False
_thread = None

blink_count = 0
total_frames = 0
mouth_vals = []
nose_x_vals = []

EAR_CLOSED = 0.17
EAR_OPEN = 0.22
MIN_CLOSED_FRAMES = 2

SYSTEM_CAMERA_INDEX = 0   # ✅ FORCE SYSTEM CAMERA


# ---------------- EAR ----------------
def eye_aspect_ratio(lm):
    left = lm[33]
    right = lm[133]
    top1 = lm[159]
    bottom1 = lm[145]
    return abs(top1.y - bottom1.y) / max(abs(left.x - right.x), 1e-6)


# ---------------- CAMERA OPEN ----------------
def open_camera():
    cap = cv2.VideoCapture(SYSTEM_CAMERA_INDEX, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ System camera failed to open")
        return None

    print("✅ System camera opened (index 0)")
    return cap


# ---------------- BACKGROUND LOOP ----------------
def _camera_loop():

    global blink_count, total_frames, mouth_vals, nose_x_vals

    cap = open_camera()
    if cap is None:
        return

    closed_frames = 0
    eye_closed = False
    start = time.time()

    while _session_running:

        ret, frame = cap.read()
        if not ret:
            continue

        total_frames += 1
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_img = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        ts = int((time.time() - start) * 1000)
        res = face_landmarker.detect_for_video(mp_img, ts)

        if res.face_landmarks:

            lm = res.face_landmarks[0]

            # ----- BLINK -----
            ear = eye_aspect_ratio(lm)

            if ear < EAR_CLOSED:
                closed_frames += 1
            elif ear > EAR_OPEN:
                if eye_closed and closed_frames >= MIN_CLOSED_FRAMES:
                    blink_count += 1
                eye_closed = False
                closed_frames = 0

            if closed_frames >= MIN_CLOSED_FRAMES:
                eye_closed = True

            # ----- MOUTH -----
            mouth_vals.append(abs(lm[13].y - lm[14].y))

            # ----- HEAD MOVE -----
            nose_x_vals.append(lm[1].x)

    cap.release()


# ============================
# PUBLIC API
# ============================

def start_camera_session():
    global _session_running, _thread
    if _session_running:
        return

    print("📷 Camera session started")

    # reset counters
    reset_metrics()

    _session_running = True
    _thread = threading.Thread(target=_camera_loop, daemon=True)
    _thread.start()


def stop_camera_session():
    global _session_running
    _session_running = False
    print("📷 Camera session stopped")


def reset_metrics():
    global blink_count, total_frames, mouth_vals, nose_x_vals
    blink_count = 0
    total_frames = 0
    mouth_vals = []
    nose_x_vals = []


def run_nervousness_analysis():

    if total_frames < 15:
        print("⚠️ Not enough frames captured")
        return 5.0

    avg_mouth = np.mean(mouth_vals) if mouth_vals else 0.01
    head_move = np.std(nose_x_vals) if nose_x_vals else 0.01
    blink_rate = blink_count / max(total_frames, 1)

    blink_score = min(blink_rate / 0.35, 1)
    mouth_score = min(avg_mouth / 0.06, 1)
    head_score = min(head_move / 0.03, 1)

    score = (0.4*blink_score + 0.3*mouth_score + 0.3*head_score) * 100

    print("Frames:", total_frames)
    print("Blinks:", blink_count)
    print("Score:", score)

    return round(score, 2)