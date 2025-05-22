import cv2
import time

print(cv2.__version__)

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("카메라 오픈 에러 ")
    exit()

cam.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(1) != 27:
    ret, f = cam.read()
    c1 = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) #Gray 변환
    # c2 = cv2.GaussianBlur(f, (7,7), 0) # Blur 효과
    r, c3 = cv2.threshold(f, 120, 255, cv2.THRESH_BINARY) # 인계효과
    
    cv2.imshow('aa', f)
    cv2.imshow('1', c1)
    # cv2.imshow('2', c2)
    cv2.imshow('3', c3)
    
cv2.imwrite('cvtest.jpg',f)
cv2.waitKey()
cv2.destroyAllWindows()


