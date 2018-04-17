import cv2
import numpy as np
# define range of blue color in HSV
#col = (40, 134, 201, 255, 255, 255
lower_blue = np.array([40,134,201])
upper_blue = np.array([255,255,255])
lower_green = np.array([40,134,2011])
upper_green = np.array([255,255,255])
cap = cv2.VideoCapture(0)
while(1):

# Take each frame
     _, frame = cap.read()
# Convert BGR to HSV
     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     #try gaussian filter but this reduces distance of recognition
     #hsv1 = cv2.GaussianBlur(hsv,(7,7),0)

# Threshold the HSV image to get only blue and green colors
     mask1 = cv2.inRange(hsv, lower_blue, upper_blue)
     mask2 = cv2.inRange(hsv, lower_green, upper_green)
     mask = mask1 + mask2
# Bitwise-AND mask and original image
     res = cv2.bitwise_and(frame,frame, mask = mask)  #compare original image with white image which pixe get one are made 1
     kernel = np.ones((5,5))
    # kernelclose = np.ones((20,20))
     maskopen = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
     maskclose = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
     # opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
     #closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
     masknew = maskopen + maskclose
     img, contours, hierarchy = cv2.findContours(masknew, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print (len(contours))  #check number of contours
    # print(contours)
     #print(hierarchy)
     if len(contours)>0:   #procced only if atleast one contour is found
        cv2.drawContours(frame, contours, -1,(0,0,255), 2)    #always draw to original image (0 to 255) is color and 3 is width of contour
        #cnt = contours[-1]
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
        #x,y,w,h = cv2.boundingRect(cnt)
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        #M = cv2.moments(cnt)
            M = cv2.moments(c)
            if M["m00"] != 0:
               cx = int(M["m10"] / M["m00"])
               cy = int(M['m01']/M['m00'])
               cv2.circle(frame,(cx,cy),5,255,-1)
               print (cx,cy)
     cv2.imshow('frame',frame)
     cv2.imshow('mask',mask)
     cv2.imshow('res',res)
     cv2.imshow('maskin',masknew)
    # cv2.imshow('open',maskopen)
     #cv2.imshow('close',maskclose)
     #cv2.imshow('res',thresh)
     k = cv2.waitKey(5) & 0xFF
     if k == 27:
        break
cv2.destroyAllWindows()
cap.release()
