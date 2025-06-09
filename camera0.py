import cv2
import sys

cap0 = cv2.VideoCapture(0)

cap0.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap0.isOpened():
    print("Error : 인덱스 0번 카메라를 열 수 없습니다.")
    cap0.release()
    cv2.destroyAllWindows()
    sys.exit(1)

ret0, frame0 = cap0.read()

if ret0:
    cv2.imshow("Webcam 0 (480x360)", frame0)
    cv2.waitKey(0)
else:
    print("Error: 카메라에서 프레임을 읽지 못했습니다.")

cap0.release()
cv2.destroyAllWindows()
