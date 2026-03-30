import cv2
from ultralytics import YOLO

# Load model
model = YOLO("yolov8n.pt")

# Mở video
cap = cv2.VideoCapture("plate_test.mp4")

# Vị trí line
line_y = 300

# Lưu vị trí ID
track_history = {}

# Tránh đếm trùng
counted_ids = set()

# Biến đếm
in_count = 0
out_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame, persist=True)

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()

        for box, track_id, cls in zip(boxes, ids, classes):
            if int(cls) in [2, 5, 7]:  # car, bus, truck
                x1, y1, x2, y2 = map(int, box)

                # Tâm xe
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                # Loại xe + màu
                if int(cls) == 2:
                    name = "Car"
                    color = (0, 255, 0)
                elif int(cls) == 5:
                    name = "Bus"
                    color = (255, 0, 0)
                else:
                    name = "Truck"
                    color = (0, 165, 255)

                # ===== Vẽ box mảnh =====
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)

                # ===== Text nhỏ, gọn =====
                label = f"{name} {int(track_id)}"
                cv2.putText(frame, label,
                            (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 1)

                # ===== Theo dõi vị trí =====
                prev_cy = track_history.get(track_id, cy)

                if track_id not in counted_ids:
                    if prev_cy < line_y and cy >= line_y:
                        in_count += 1
                        counted_ids.add(track_id)
                    elif prev_cy > line_y and cy <= line_y:
                        out_count += 1
                        counted_ids.add(track_id)

                track_history[track_id] = cy

    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (255, 0, 0), 2)

    total = in_count + out_count

    cv2.putText(frame, f"IN: {in_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.putText(frame, f"OUT: {out_count}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(frame, f"TOTAL: {total}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # ===== HIỂN THỊ =====
    cv2.imshow("Car Counting IN/OUT", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

print("IN:", in_count)
print("OUT:", out_count)
print("TOTAL:", total)