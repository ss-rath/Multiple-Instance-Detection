#PD LAB Group 5 Spring 2017-18
#Code written by SSR
#rath.soumyasambit@gmail.com
#Code for tracking a feature by selecting ROI.
#Press 'P' to pause, drag to select the ROI using mouse and then hit enter to track


import cv2
b_box=[]
new_box=[]
tracker_ok=[]
p1=[]
p2=[]
centre=[]
tracker=[]
max_trackers=3

cv2.namedWindow("Multiple ROI Tracking")
cap = cv2.VideoCapture(0) #path of the video/camera #Replace with appropriate path
ok, image=cap.read()


#tracker = cv2.TrackerMIL_create()
flag = 0

i=0
#initialise all the lists with zeroes
while(i<max_trackers):
	b_box.append(0)
	new_box.append(0)
	tracker_ok.append(0)
	p1.append(0)
	p2.append(0)
	centre.append(0)
	tracker.append(0)
	i+=1

while cap.isOpened():
	ok, image=cap.read()
	#image=cv2.flip(image,1)
    
	k = cv2.waitKey(1) & 0xff
	if k == ord('p'):
		if flag < max_trackers:
			tracker[flag]=cv2.TrackerMIL_create()
			b_box[flag] = cv2.selectROI("Select ROI", image)
			tracker_ok[flag] = tracker[flag].init(image, b_box[flag])
			flag +=1
			#print flag

	i=0
	while(i<flag):		
		tracker_ok[i], new_box[i] = tracker[i].update(image)

		if tracker_ok[i]:
			p1[i] = (int(new_box[i][0]), int(new_box[i][1]))
			p2[i] = (int(new_box[i][0] + new_box[i][2]), int(new_box[i][1] + new_box[i][3]))
			#cv2.rectangle(image, p1, p2, (0,0,200),2)
			centre[i] = (int((p1[i][0]+p2[i][0])/2),int((p1[i][1]+p2[i][1])/2))
			cv2.circle(image,centre[i], 4, (0,0,255), -1)
		i+=1
		
	cv2.imshow("Pause and Track", image)
	if k == 27 : break # esc pressed
    
cv2.destroyAllWindows()
