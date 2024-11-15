import cv2
import numpy as np
import mediapipe as mp
from math import dist
import winsound
from selenium import webdriver
import time 
from threading import Thread
import requests
import keyboard

data = None
server = "http://localhost:8000"
duration = requests.get(server+"/duration").json()["duration"]
detector = mp.solutions.face_detection.FaceDetection(model_selection=1,min_detection_confidence=0.5)
camera = cv2.VideoCapture(0)
warning = 0
old = 0

def proctor(duration,st):
	global warning,old,camera,detector
	while time.time()-st<duration:
		ret, frame = camera.read()
		if not ret:
			break
		if int(warning)>old:
			print("warning")
			old=old+1
			winsound.MessageBeep()
		h,w,c = frame.shape
		frame = cv2.flip(frame, 1)
		rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		results = detector.process(rgb_frame)
		if results.detections:
			for face in results.detections:
				face_react = np.multiply(
	                    [
	                        face.location_data.relative_bounding_box.xmin,
	                        face.location_data.relative_bounding_box.ymin,
	                        face.location_data.relative_bounding_box.width,
	                        face.location_data.relative_bounding_box.height,
	                    ],[w,h,w,h]).astype(int)
				key_points = np.array([(p.x, p.y) for p in face.location_data.relative_keypoints])
				key_points_coords = np.multiply(key_points,[w,h]).astype(int)
				for p in key_points_coords:
					cv2.circle(frame, p, 4, (255, 255, 0))
				thresh = dist(key_points_coords[0],key_points_coords[1])
				cv2.putText(frame,f"{thresh}",(30, 30),cv2.FONT_HERSHEY_DUPLEX,0.7,(0, 255, 255),2,)
				cv2.putText(frame,f"{warning}",(30, 70),cv2.FONT_HERSHEY_DUPLEX,0.7,(0, 0, 255),2,)
				if 65<thresh<120:
					cv2.rectangle(frame, face_react, color=(255, 255, 255), thickness=2)
				else:
					cv2.rectangle(frame, face_react, color=(0, 0, 255), thickness=2)
					warning=warning+0.01
		if cv2.waitKey(1) == ord("q"):
			break
		# cv2.waitKey(1)
		cv2.imshow("proctor", frame)
	camera.release()
	cv2.destroyAllWindows()

def upload():
	global warning,data
	requests.post(server+"/studentdata",json={"name":data[0],"regno":data[1],"warning":warning})
	print(warning,data)

def test(link,duration):
	keyboard.block_key("windows")
	driver = webdriver.Chrome(executable_path="chromedriver.exe")
	driver.get(link)
	driver.fullscreen_window()
	time.sleep(duration)
	upload()

def Tapp(link,user_data):
	global data,duration
	data = user_data
	t1 = Thread(target=test,args=(link,duration,))
	t2 = Thread(target=proctor,args=(duration+15,time.time()))
	t2.start()
	time.sleep(15)
	t1.start()

if __name__ == "__main__":
	proctor(60,time.time())