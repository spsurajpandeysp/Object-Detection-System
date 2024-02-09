from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render
import cv2
import numpy as np
import math
from ultralytics import YOLO
from sort import *
import cvzone
import os

class VideoStream:
    def __init__(self, cap, model):
        self.cap = cap
        self.model = model
        self.is_streaming = True
        
    def gen_frames(self):
        limits = [400, 297, 673, 297]
        totalCount = []

        mask_path = os.path.join(os.path.dirname(__file__), "mask.png")
        graphics_path = os.path.join(os.path.dirname(__file__), "graphics.png")
        mask = cv2.imread(mask_path)
        graphics = cv2.imread(graphics_path, cv2.IMREAD_UNCHANGED)

        tracker = Sort()

        while self.is_streaming:
            ret, frame = self.cap.read()
            if not ret:
                break

            frameRegion = cv2.bitwise_and(frame, mask)
            results = self.model(frameRegion, stream=True)
            detections = np.empty((0, 5))

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1

                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])

                    if cls in [2, 5, 7, 9] and conf > 0.3:
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))

            resultsTracker = tracker.update(detections)

            cv2.line(frame, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)

            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
                    if totalCount.count(id) == 0:
                        totalCount.append(id)
                        cv2.line(frame, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

            car_count_text = str(len(totalCount))

            graphics_position = (0, 0)
            frame = cvzone.overlayPNG(frame, graphics, graphics_position)
            cv2.putText(frame, car_count_text, (graphics_position[0] + 250, graphics_position[1] + 80), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 3)

            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def stop_streaming(self):
        self.is_streaming = False

@gzip.gzip_page
def CarCounting(request):
    cap_path = os.path.join(os.path.dirname(__file__), "cars.mp4")
    cap = cv2.VideoCapture(cap_path)
    model = YOLO("../YOLO/yolov8l.pt")

    video_stream = VideoStream(cap, model)

    return StreamingHttpResponse(video_stream.gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')