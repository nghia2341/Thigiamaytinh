import cv2 as cv
import numpy as np
import math

cap = cv.VideoCapture("bang_chuyen.mp4")

count = 0
vat_the = []
next_id = 0

line_x = 600
DIST_THRESHOLD = 50
MAX_MISSING = 10  # số frame cho phép mất dấu

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)

    circles = cv.HoughCircles(
        gray,
        cv.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=5,
        maxRadius=50
    )

    detected_centers = []

    if circles is not None:
        circles = np.round(circles).astype(int)

        for circle in circles[0, :]:
            x, y, r = circle
            detected_centers.append((x, y))

            # vòng tròn vừa vật thể
            cv.circle(frame, (x, y), r, (0, 0, 255), 2)

            # vòng tròn nhỏ bên trong
            cv.circle(frame, (x, y), int(r * 0.5), (0, 0, 255), 2)

            # tâm
            cv.circle(frame, (x, y), 3, (0, 255, 255), -1)

            # hình vuông vừa với vật thể
            cv.rectangle(frame,
                        (x - r, y - r),
                        (x + r, y + r),
                        (0, 255, 0), 2)

            # hình vuông nhỏ bên trong
            small_r = int(r * 0.5)
            cv.rectangle(frame,
                        (x - small_r, y - small_r),
                        (x + small_r, y + small_r),
                        (255, 0, 0), 2)


            

    # đánh dấu tất cả object là chưa match
    for obj in vat_the:
        obj["matched"] = False

    # matching
    for (x, y) in detected_centers:
        matched = False

        for obj in vat_the:
            dist = math.hypot(obj["x"] - x, obj["y"] - y)

            if dist < DIST_THRESHOLD:
                obj["x"] = x
                obj["y"] = y
                obj["missing"] = 0
                obj["matched"] = True

                # đếm
                if not obj["counted"] and x > line_x:
                    count += 1
                    obj["counted"] = True
                    print(f"Vat the thu {count} da di qua")

                matched = True
                break

        # nếu không match → tạo object mới
        if not matched:
            vat_the.append({
                "id": next_id,
                "x": x,
                "y": y,
                "counted": x > line_x,
                "missing": 0,
                "matched": True
            })
            next_id += 1

    # xử lý object mất dấu
    new_vat_the = []
    for obj in vat_the:
        if not obj["matched"]:
            obj["missing"] += 1

        # giữ lại nếu chưa mất quá lâu
        if obj["missing"] < MAX_MISSING:
            new_vat_the.append(obj)

    vat_the = new_vat_the

    # vẽ line
    cv.line(frame, (line_x, 0), (line_x, frame.shape[0]), (0, 0, 255), 2)

    # hiển thị count
    cv.putText(frame, f"Count: {count}", (20, 40),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv.imshow("Frame", frame)

    if cv.waitKey(10) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()