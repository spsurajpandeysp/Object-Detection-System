from django.http import StreamingHttpResponse,HttpResponse
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
        limitsUp = [103, 161, 296, 161]
        limitsDown = [527, 489, 735, 489]
        totalCountUp = []
        totalCountDown = []

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
            frame = cvzone.overlayPNG(frame, graphics, (730, 260))

            results = self.model(frameRegion, device="mps")
            detections = np.empty((0, 5))

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2 - x1, y2 - y1

                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    currentClass = self.model.names[cls]

                    if currentClass == "person" and conf > 0.3:
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))

            resultsTracker = tracker.update(detections)

            cv2.line(frame, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 0, 255), 5)
            cv2.line(frame, (limitsDown[0], limitsDown[1]), (limitsDown[2], limitsDown[3]), (0, 0, 255), 5)

            for result in resultsTracker:
                x1, y1, x2, y2, id = result
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.circle(frame, (x1 + w // 2, y1 + h // 2), 5, (255, 0, 255), cv2.FILLED)

                cx, cy = x1 + w // 2, y1 + h // 2
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if limitsUp[0] < cx < limitsUp[2] and limitsUp[1] - 15 < cy < limitsUp[1] + 15:
                    if id not in totalCountUp:
                        totalCountUp.append(id)
                        cv2.line(frame, (limitsUp[0], limitsUp[1]), (limitsUp[2], limitsUp[3]), (0, 255, 0), 5)

                if limitsDown[0] < cx < limitsDown[2] and limitsDown[1] - 15 < cy < limitsDown[1] + 15:
                    if id not in totalCountDown:
                        totalCountDown.append(id)
                        cv2.line(frame, (limitsDown[0], limitsDown[1]), (limitsDown[2], limitsDown[3]), (0, 255, 0), 5)

            cv2.putText(frame, str(len(totalCountUp)), (929, 345), cv2.FONT_HERSHEY_PLAIN, 5, (139, 195, 75), 7)
            cv2.putText(frame, str(len(totalCountDown)), (1191, 345), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 230), 7)

            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def stop_streaming(self):
        self.is_streaming = False

@gzip.gzip_page
def PeopleCounting(request):
    cap_path = os.path.join(os.path.dirname(__file__), "people.mp4")
    cap = cv2.VideoCapture(cap_path)
    model = YOLO("../YOLO/yolov8l.pt")

    video_stream = VideoStream(cap, model)

    return StreamingHttpResponse(video_stream.gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def stop_stream(request):
    VideoStream.stop_streaming()
    return HttpResponse("Stream stopped.")