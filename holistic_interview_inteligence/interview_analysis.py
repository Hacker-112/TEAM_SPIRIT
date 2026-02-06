import cv2
import numpy as np
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

print("🚀 Starting Interview Nervousness Camera")

# ---------------- LOAD FACE LANDMARKER ----------------
base_options = python.BaseOptions(
    model_asset_path="face_landmarker.task"
)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1
)

face_landmarker = vision.FaceLandmarker.create_from_options(options)
print("✅ Face Landmarker loaded")

# ---------------- CAMERA PRIORITY SYSTEM ----------------
print("🎥 Trying to open External/DroidCam first...")

def open_camera_priority():
    camera_order = [2, 1, 0]   # ⭐ PRIORITY ORDER

    for idx in camera_order:
        print(f"Trying camera index {idx}...")
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)

        if not cap.isOpened():
            continue

        # check if camera really gives frames
        for _ in range(20):
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✅ Using camera index {idx}")
                return cap

        cap.release()

    raise RuntimeError("❌ No camera available")

cap = open_camera_priority()

# ---------------- VARIABLES ----------------
blink_count = 0
total_frames = 0
mouth_open_values = []
nose_x_positions = []

EAR_CLOSED = 0.17
EAR_OPEN = 0.22
MIN_CLOSED_FRAMES = 2

eye_closed = False
closed_frames = 0

def eye_aspect_ratio(landmarks):
    left = landmarks[33]
    right = landmarks[133]
    top1 = landmarks[159]
    bottom1 = landmarks[145]
    top2 = landmarks[160]
    bottom2 = landmarks[144]

    vertical = abs(top1.y - bottom1.y) + abs(top2.y - bottom2.y)
    horizontal = abs(left.x - right.x)
    return vertical / (2.0 * horizontal)

# ---------------- MAIN LOOP ----------------
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera frame not received")
        break

    total_frames += 1
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=frame_rgb
    )

    timestamp = int((time.time() - start_time) * 1000)
    result = face_landmarker.detect_for_video(mp_image, timestamp)

    if result.face_landmarks:
        landmarks = result.face_landmarks[0]

        # ----- Blink detection -----
        ear = eye_aspect_ratio(landmarks)

        if ear < EAR_CLOSED:
            closed_frames += 1
        elif ear > EAR_OPEN:
            if eye_closed and closed_frames >= MIN_CLOSED_FRAMES:
                blink_count += 1
            eye_closed = False
            closed_frames = 0

        if closed_frames >= MIN_CLOSED_FRAMES:
            eye_closed = True

        # ----- Mouth movement -----
        mouth_open = abs(landmarks[13].y - landmarks[14].y)
        mouth_open_values.append(mouth_open)

        # ----- Head movement -----
        nose_x_positions.append(landmarks[1].x)

    # ----- Display -----
    cv2.putText(frame, f"Blinks: {blink_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(frame, "Press Q to Quit", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    cv2.imshow("Interview Nervousness Analysis", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()

print("\n🧠 ANALYSIS FINISHED")
print("Frames:", total_frames)
print("Blinks:", blink_count)

avg_mouth_open = np.mean(mouth_open_values) if mouth_open_values else 0
head_movement = np.std(nose_x_positions) if nose_x_positions else 0

blink_rate = blink_count / max(total_frames,1)

blink_score = min(blink_rate / 0.35, 1)
mouth_score = min(avg_mouth_open / 0.06, 1)
head_score = min(head_movement / 0.03, 1)

nervousness_score = (0.4*blink_score + 0.3*mouth_score + 0.3*head_score) * 100

print(f"Nervousness Score: {nervousness_score:.2f}/100")

if nervousness_score < 30:
    print("🙂 You appear calm and confident.")
elif nervousness_score < 60:
    print("😐 Slight nervousness detected.")
else:
    print("😰 High nervousness detected. Practice more!")
