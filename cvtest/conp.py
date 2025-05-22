import cv2

s1 = cv2.imread('c2.jpg')
s2 = cv2.imread('c3.jpg')

diff = cv2.absdiff(s1, s2)
gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

r, thre = cv2.threshold(gray_diff, 120, 255, cv2.THRESH_BINARY) # 인계효과
cann = cv2.Canny(diff, 100, 200)
cont, r=cv2.findContours(thre, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(s1, cont, -1, (0, 255, 0), 2)

# cv2.imshow('s1',s1)
# cv2.imshow('s2',s2)

cv2.imshow("diff", diff)
cv2.imshow("Canny", cann)

for a in cont:
    x,y,w,h = cv2.boundingRect(a)
    cv2.rectangle(thre, (x,y), (x+w,y+h), (255, 0, 0), 2)
cv2.imshow("Threashold", thre)

# cv2.imshow("Contours", s1)

cv2.waitKey(0)
cv2.destoryAllWindows()
