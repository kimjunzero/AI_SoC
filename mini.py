import os
import cv2
import torch
import subprocess
#from playsound import playsound

warned = False
FIFO = '/tmp/py2c_fifo'

# playsound("warning.wav")

if not os.path.exists(FIFO):
    os.mkfifo(FIFO)

pipe = open(FIFO, 'w')

model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
model.conf = 0.4
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

ret, tmp = cap.read()
if not ret:
    print("fail...camera open")
    cap.release()
    exit()
    
frame_area = tmp.shape[0] * tmp.shape[1]
detect_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)
    df = results.pandas().xyxy[0]

    filtered = df[df['name'] == 'person']

    if len(filtered) > 0:
        detect_count += 1

        filtered = filtered.copy()
        filtered['area'] = (filtered['xmax'] - filtered['xmin']) * (filtered['ymax'] - filtered['ymin'])
        biggest = filtered.sort_values('area', ascending=False).iloc[0]

        x1, y1 = int(biggest['xmin']), int(biggest['ymin'])
        x2, y2 = int(biggest['xmax']), int(biggest['ymax'])
        box_area = (x2 - x1) * (y2 - y1)
        norm = box_area / frame_area
        level = max(1, min(int(norm * 10), 10))

        if detect_count >= 3:
            pipe.write(f"{level}\n")
            pipe.flush()

            if level >= 3 and not warned:
 #               playsound("warning.wav")
                warned = True
            else:
                warned = False

        for idx, row in filtered.iterrows():
            px1, py1 = int(row['xmin']), int(row['ymin'])
            px2, py2 = int(row['xmax']), int(row['ymax'])

            cv2.rectangle(frame, (px1, py1), (px2, py2), (0, 255, 0), 2)
            cv2.putText(frame,f"P:{row['confidence']:.2f}",
                (px1, py1 - 10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0, 255, 0),1)
    else:
        level = 0
        detect_count = 0
        warned = False
        pipe.write(f"{level}\n")
        pipe.flush()

    #  cv2.imshow("Webcam YOLO", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
pipe.close()
cv2.destroyAllWindows()
