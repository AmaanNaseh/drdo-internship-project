# app.py
from flask import Flask, request, Response
from flask_cors import CORS
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

def detect_red_objects(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = cv2.bitwise_or(mask1, mask2)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Red Object', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

    return frame

@app.route('/video_feed', methods=['POST'])
def process_frame():
    file = request.files.get('frame')
    if file is None:
        return "No frame received", 400

    file_bytes = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if frame is None:
        return "Invalid frame", 400

    processed = detect_red_objects(frame)

    _, jpeg = cv2.imencode('.jpg', processed)
    return Response(jpeg.tobytes(), mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(debug=True)
