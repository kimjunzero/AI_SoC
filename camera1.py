import cv2
import sys
cap2 = cv2.VideoCapture(2)

cap2.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap2.isOpened():
    print("Error : 인덱스 2번 카메라를 열 수 없습니다.")
    cap2.release()
    cv2.destroyAllWindows()
    sys.exit(1)

ret2, frame2 = cap2.read()

if ret2:
    cv2.imshow("Webcam 2 (480x360)", frame2)
    cv2.waitKey(0)
else:
    print("Error: 카메라에서 프레임을 읽지 못했습니다.")

cap2.release()
cv2.destroyAllWindows()
