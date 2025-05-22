import cv2

s_img = cv2.imread('c1.jpg')
gimg = cv2.cvtColor(s_img, cv2.COLOR_BGR2GRAY)
#c_gimg = cv2.GaussianBlur(s_img, (7,7), 0) # Blur 효과
#r, c_img = cv2.threshold(s_img, 120, 255, cv2.THRESH_BINARY)
c_img = cv2.Canny(g_img, 100, 200)


cv2.imshow("",s_img)
cv2.imshow("Converted", c_img)
cv2.waitKey(0)
