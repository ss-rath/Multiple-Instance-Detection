#PD LAB Group 5 Spring 2017-18
#Code written by SSR
#rath.soumyasambit@gmail.com
#Code for saving the detected features as BLOB in MongoDB and also as .jpg in the local dir

import cv2
import os
from time import gmtime, strftime
from pymongo import MongoClient
import base64

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['Templates']
collection = db[strftime("%d_%m_%Y_%H_%M_%S", gmtime())]
posts = db.posts

cv2.namedWindow("Save Templates")
cap = cv2.VideoCapture("sample_1.mp4") # change this for different source
ok, image=cap.read()


tracker = cv2.TrackerMIL_create()
flag = False
count=0

while cap.isOpened():
	ok, image=cap.read()
	#image=cv2.flip(image,1) #use it to flip horizontally
    
	k = cv2.waitKey(1) & 0xff
	if k == ord('p'):
		if not flag:
			bbox = cv2.selectROI("Pause and Track", image)
			ok = tracker.init(image, bbox)
			crop_image = image[int(bbox[1]):int(bbox[1])+int(bbox[3]), int(bbox[0]):int(bbox[0])+int(bbox[2])]
			cv2.imshow("Object to be tracked", crop_image)
			path = os.getcwd()
			path += "/Templates_%s" %strftime("%d_%m_%Y_%H_%M_%S", gmtime())
			os.mkdir(path)
			os.chdir(path)
			flag = True

	ok, newbox = tracker.update(image)

	if ok:
		p1 = (int(newbox[0]), int(newbox[1]))
		p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
		template= image[int(newbox[1]):int(newbox[1])+int(newbox[3]),int(newbox[0]):int(newbox[0])+int(newbox[2])]
		filename= str(count) + ".jpg"
		cv2.imwrite(filename, template)
		
		filename = filename+ "_" + strftime("%d_%m_%Y_%H_%M_%S", gmtime())
		post = { "filename" : filename, "image" : base64.b64encode(template[0]) }
		post_id = posts.insert_one(post).inserted_id
		
		#cv2.rectangle(image, p1, p2, (0,0,200),2)
		centre = (int((p1[0]+p2[0])/2),int((p1[1]+p2[1])/2))
		cv2.circle(image,centre, 4, (0,0,255), -1)
		count+=1

	cv2.imshow("Pause and Track", image)
	if k == 27 : break # esc pressed
    
cv2.destroyAllWindows()
