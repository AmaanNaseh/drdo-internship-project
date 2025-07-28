import cv2
import numpy as np
import serial
import time

arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = cv2.bitwise_or(mask1, mask2)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    object_detected = False
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Red Object', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)
            object_detected = True
            break

    # Automatic trigger
    if object_detected:
        print("[INFO] Red object detected. Sending command to Arduino.")
        arduino.write(b'P')  # Also triggers LED blink in Arduino
        time.sleep(5) 

    # Manual trigger by pressing 'm'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('m'):
        print("[INFO] Manual trigger pressed. Sending command to Arduino.")
        arduino.write(b'P')  
        time.sleep(5)

    # Quit by pressing 'q'
    if key == ord('q'):
        print("[INFO] Quitting...")
        break

    cv2.imshow("Red Object Detection", frame)

cap.release()
cv2.destroyAllWindows()
arduino.close()
