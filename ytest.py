import cv2
import torch

# 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 이미지 경로
img_path = '/home/kjy/Pictures/two.jpg'
img = cv2.imread(img_path)

# YOLO 탐지
r = model(img_path)
d = r.pandas().xyxy[0]

def nothing(x):
    pass
    
cv2.namedWindow("Result")
cv2.createTrackbar("Confidence", "Result", 60, 100, nothing)

while True:
    
    conf = cv2.getTrackbarPos("Confidence", "Result") / 100.0

    temp = img.copy()
    f = d[d['confidence'] > conf]

    for _, row in f.iterrows():
        x1, y1 = int(row['xmin']), int(row['ymin'])
        x2, y2 = int(row['xmax']), int(row['ymax'])
        label = f"{row['name']} {row['confidence']:.2f}"
        cv2.rectangle(temp, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(temp, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow("Result", temp)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
