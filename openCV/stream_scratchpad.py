from flask import Flask,Response,render_template
import numpy as np
import cv2

app = Flask(__name__)

cap = cv2.VideoCapture('vid.mp4')

def vid():
    while cap.isOpened():
        ret, frame = cap.read();
        yield frame;
    cap.release();
    cv2.destroyAllWindows();

@app.route('/')
def stream():
    return Response(vid(), mimetype='multipart/x-mixed-replace; boundary = frame')

if __name__ == "__main__":
    app.run()
