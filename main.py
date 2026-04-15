import cv2
import os
import time
from datetime import datetime
from ultralytics import YOLO
import winsound

print("SMART SECURITY SYSTEM DANG CHAY")
print("Dang tai model...")
model = YOLO("yolov8n.pt")
print("Tai model xong")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Khong mo duoc webcam")
    input("Nhan Enter de thoat...")
    exit()

# Tao thu muc neu chua co
os.makedirs("captures", exist_ok=True)
os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/intrusion_log.txt"

SAVE_COOLDOWN = 5      # so giay giua 2 lan luu anh
ALARM_COOLDOWN = 3     # so giay giua 2 lan beep

last_save_time = 0
last_alarm_time = 0

ZONE_X1 = 150
ZONE_Y1 = 100
ZONE_X2 = 500
ZONE_Y2 = 400

print("Webcam da mo. Nhan q de thoat.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Khong doc duoc frame")
        break

    cv2.rectangle(frame, (ZONE_X1, ZONE_Y1), (ZONE_X2, ZONE_Y2), (0, 0, 255), 2)
    cv2.putText(
        frame,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    results = model(frame, verbose=False)
    intrusion_detected = False

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())

            if cls_id != 0 or conf < 0.5:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            inside_zone = (ZONE_X1 <= cx <= ZONE_X2) and (ZONE_Y1 <= cy <= ZONE_Y2)

            color = (0, 0, 255) if inside_zone else (0, 255, 0)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, (cx, cy), 5, color, -1)

            text = f"Person {conf:.2f}"
            if inside_zone:
                text += " - INTRUSION"
                intrusion_detected = True

            cv2.putText(
                frame,
                text,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

    if intrusion_detected:
        cv2.putText(
            frame,
            "INTRUSION DETECTED!",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        current_time = time.time()

        if current_time - last_alarm_time >= ALARM_COOLDOWN:
            winsound.Beep(1500, 500)
            last_alarm_time = current_time

        if current_time - last_save_time >= SAVE_COOLDOWN:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"captures/intrusion_{timestamp}.jpg"

            cv2.imwrite(image_path, frame)

            log_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Intrusion detected - saved: {image_path}"

            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_message + "\n")

            print(log_message)
            last_save_time = current_time

    cv2.imshow("Smart Security System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()