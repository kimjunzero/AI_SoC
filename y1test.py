import cv2
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

cap = cv2.VideoCapture(0)

def nothing(x):
    pass


cv2.namedWindow("Webcam YOLO")
cv2.createTrackbar("Confidence", "Webcam YOLO", 60, 100, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    conf = cv2.getTrackbarPos("Confidence", "Webcam YOLO") / 100.0

    results = model(frame)
    df = results.pandas().xyxy[0]
    
    filtered = df[df['confidence'] > conf]

    for _, row in filtered.iterrows():
        x1, y1 = int(row['xmin']), int(row['ymin'])
        x2, y2 = int(row['xmax']), int(row['ymax'])
        label = f"{row['name']} {row['confidence']:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow("Webcam YOLO", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()


