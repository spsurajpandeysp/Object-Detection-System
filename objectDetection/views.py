from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators import gzip
import cv2
import cvzone
import numpy as np
import math
import time
from ultralytics import YOLO

class VideoStream:
    def __init__(self, cap, model):
        self.cap = cap
        self.model = model
        self.is_streaming = True

    def gen_frames(self):
        classNames = ["person", "bicycle", "car", "hair dryer", "fan", "motorbike", "bus", "train", "truck", "boat",
                      "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                      "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "backpack", "mouse", "laptop bag",
                      "tie", "laptop bag", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                      "baseball glove", "skateboard", "surfboard", "bottle", "tennis racket", "wine glass", "cup",
                      "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                      "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                      "diningtable", "toilet", "laptop", "tv monitor", "pendrive", "remote", "phone", "cell phone",
                      "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                      "teddy bear", "pen", "toothbrush"
                      ]

        prev_frame_time = 0

        while self.is_streaming:
            new_frame_time = time.time()
            success, img = self.cap.read()

            if not success:
                break

            results = self.model(img, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1
                    cvzone.cornerRect(img, (x1, y1, w, h))
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            fps = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            print(fps)

            _, jpeg = cv2.imencode('.jpg', img)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # Pause for a short time to simulate real-time
            time.sleep(0.1)

    def stop_streaming(self):
        self.is_streaming = False
        self.cap.release()

@gzip.gzip_page
def ObjectDetection(request):
    cap = cv2.VideoCapture(0)
    cap.set(3, 1080)
    cap.set(4, 720)

    model = YOLO("../YOLO/yolov8l.pt")

    video_stream = VideoStream(cap, model)

    return StreamingHttpResponse(video_stream.gen_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def stop_stream(request):
    video_stream.stop_streaming()
    return HttpResponse("Stream stopped.")