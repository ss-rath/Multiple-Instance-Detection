#PD Lab Group 5 Spring 2017-18
#Code written by SSR
#rath.soumyasambit@gmail.com
#This code detects multiple instances of the same ROI from different sources

import cv2


cv2.namedWindow("Multi Source")
cap = cv2.VideoCapture(0)  #1st Source
cap2 = cv2.VideoCapture(1) #2nd Source

ok, image=cap.read()
ok2, image2=cap2.read()

tracker = cv2.TrackerMIL_create()
tracker2 = cv2.TrackerMIL_create()
flag = False
flag2 = False
while cap.isOpened():
	ok, image=cap.read()
	ok2, image2=cap2.read()
	#image=cv2.flip(image,1)
    #image2=cv2.flip(image2,1)
	k = cv2.waitKey(1) & 0xff
	if k == ord('p'):
		if not flag:
			bbox = cv2.selectROI("Pause and Track", image) #change this according to the frame from which ROI has to be selected
			ok = tracker.init(image, bbox)
			print(ok)
			ok2 = tracker2.init(image2, bbox)
			flag = True

	ok, newbox = tracker.update(image)
	ok2, newbox2 = tracker2.update(image2)

	if ok:
		p1 = (int(newbox[0]), int(newbox[1]))
		p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
		#cv2.rectangle(image, p1, p2, (0,0,200),2)
		centre = (int((p1[0]+p2[0])/2),int((p1[1]+p2[1])/2))
		cv2.circle(image,centre, 4, (0,0,255), -1)
	
	if ok2:
		p1 = (int(newbox2[0]), int(newbox2[1]))
		p2 = (int(newbox2[0] + newbox2[2]), int(newbox2[1] + newbox2[3]))
		#cv2.rectangle(image2, p1, p2, (0,0,200),2)
		centre = (int((p1[0]+p2[0])/2),int((p1[1]+p2[1])/2))
		cv2.circle(image2,centre, 4, (0,0,255), -1)

	cv2.imshow("DELL Webcam", image)
	cv2.imshow("Logitech C310", image2)
	if k == 27 : break # esc pressed
    
cv2.destroyAllWindows()
