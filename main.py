"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/NAI/
    Mateusz Olstowski: https://github.com/Matieus/NAI/

---
"""
import os

import cv2 as cv
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

FILES_DIR = os.path.join(os.getcwd(), 'files')
DATA_DIR = os.path.join(os.getcwd(), 'data')
MODELS_DIR = os.path.join(os.getcwd(), 'models')
CROSS_HAIR = os.path.join(FILES_DIR, 'crosshair.png')
FRONTAL_FACE = os.path.join(FILES_DIR, 'haarcascade_frontalface_default.xml')
FULL_BODY = os.path.join(FILES_DIR, 'haarcascade_fullbody.xml')


class FaceDetector:
	def __init__(self):
		self.face_cascade = cv.CascadeClassifier(FRONTAL_FACE)
		self.cap = cv.VideoCapture(0)
		self.mp_pose = mp.solutions.pose
		self.pose = self.mp_pose.Pose()
		self.drawing = mp.solutions.drawing_utils

		self.cross_hair = cv.imread(CROSS_HAIR)
		self.prev_pose = None
		self.size = 50
		self.cross_hair = cv.resize(self.cross_hair, (self.size, self.size))

	def _shot(self, current_pose, frame):
		"""
		Adds a cross_hair to the target
		"""
		X = current_pose.landmark[0].x
		Y = current_pose.landmark[0].y

		# Calculate the position to place the crosshair
		x = int(frame.shape[0] * Y) - self.cross_hair.shape[0] // 2
		y = int(frame.shape[1] * X) - self.cross_hair.shape[1] // 2

		frame[y:y + self.size, x:x + self.size] = self.cross_hair

	def _detect_movement(self, current_pose, prev_pose, threshold):
		"""
		Returns that pose has moved or not

		RETURNS
		-------
		s: bool - returns that pose has moved or not
		"""
		s = np.sqrt(
			(prev_pose.landmark[0].x - current_pose.landmark[0].x) ** 2 -
			(prev_pose.landmark[0].y - current_pose.landmark[0].y) ** 2
		)
		return s > threshold

	def start(self):
		while True:
			_, frame = self.cap.read()
			gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			gray_cross_hair = cv.cvtColor(self.cross_hair, cv.COLOR_BGR2GRAY)
			_, mask = cv.threshold(gray_cross_hair, 1, 255, cv.THRESH_BINARY)
			rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
			current_pose = self.pose.process(rgb_frame)

			faces = self.face_cascade.detectMultiScale(gray_frame, 1.1, 11)

			if self.prev_pose is not None:
				if self._detect_movement(current_pose.pose_landmarks, self.prev_pose, .005):
					try:
						for (x, y, w, h) in faces:
							cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
							self._shot(current_pose, frame)
					except Exception as e:
						print("Couldn't draw a rectangle")
				else:
					for (x, y, w, h) in faces:
						cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

			self.prev_pose = current_pose.pose_landmarks

			"""
			Show current frame.
			"""
			cv.imshow("stream", frame)
			if cv.waitKey(1) & 0xFF == ord('q'):
				break

		""" 
		Clean variables and destroy windows.
		"""
		self.cap.release()
		cv.destroyAllWindows()


class HandGesture:
	def __init__(self):
		self.cap = cv.VideoCapture(0)
		self.mp_hands = mp.solutions.hands
		self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
		self.drawing = mp.solutions.drawing_utils
		self.model = load_model(os.path.join(MODELS_DIR, "hand_gesture_model"))
		self.gesture_names = self._get_gesture_name()

	def _get_gesture_name(self):
		"""
		Loads gesture names

		RETURNS
		-------
		class_names: list - list of gesture names
		"""
		f = open(os.path.join(DATA_DIR, "gesture.names"), "r")
		gesture_names = f.read().split('\n')
		f.close()
		return gesture_names

	def start(self):
		while True:
			_, frame = self.cap.read()
			x, y, c = frame.shape
			rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
			result = self.hands.process(rgb_frame)

			# Flip the frame vertically
			# frame = cv.flip(frame, 1)

			# post process the result
			if result.multi_hand_landmarks:
				landmarks = []
				for handslms in result.multi_hand_landmarks:
					for lm in handslms.landmark:
						lmx = int(lm.x * x)
						lmy = int(lm.y * y)

						landmarks.append([lmx, lmy])

						"""
						Drawing landmarks on frames
						"""
						self.drawing.draw_landmarks(frame, handslms, self.mp_hands.HAND_CONNECTIONS)

				if landmarks:
					prediction = self.model.predict([landmarks])
					# print("prediction", prediction)

					"""
					np.argmax() returns the index of the maximum value in the list.
					"""

					class_id = np.argmax(prediction)
					gesture_names = self.gesture_names[class_id]

					"""
					show the prediction on the frame
					"""
					cv.putText(frame, gesture_names, (10, 50), cv.FONT_HERSHEY_SIMPLEX,1,
					           (0, 255, 0), 2, cv.LINE_AA)

			cv.imshow("Output", frame)
			if cv.waitKey(1) == ord('q'):
				break

		"""
		release the webcam and destroy all active windows
		"""
		self.cap.release()
		cv.destroyAllWindows()


def main():
	# fd = FaceDetector()
	# fd.start()

	hg = HandGesture()
	hg.start()


if __name__ == '__main__':
	main()
