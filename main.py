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

FILES_DIR = os.path.join(os.getcwd(), 'files')
CROSS_HAIR = os.path.join(FILES_DIR, 'crosshair.png')
FRONTAL_FACE = os.path.join(FILES_DIR, 'haarcascade_frontalface_default.xml')
FULL_BODY = os.path.join(FILES_DIR, 'haarcascade_fullbody.xml')

class MoveDetector:
	def __init__(self):
		self.face_cascade = cv.CascadeClassifier(FRONTAL_FACE)
		self.cap = cv.VideoCapture(0)
		self.mp_pose = mp.solutions.pose
		self.pose = self.mp_pose.Pose()
		self.drawing = mp.solutions.drawing_utils

		self.cross_hair = cv.imread(CROSS_HAIR)
		self.cross_hair = cv.resize(self.cross_hair, (10, 10))
		self.prev_pose = None
		self.size = 50

	def _shot(self, current_pose, frame):
		# TODO wyliczyc pozycje
		head_top_x = int(current_pose.head_top.x)
		head_top_y = int(current_pose.head_top.y)

		""" 
		Calculate the position of the forehead
		"""
		cross_hair_x = head_top_x - 5
		cross_hair_y = head_top_y - 5

		frame[cross_hair_x, cross_hair_y] = self.cross_hair

	def _detect_movement(self, current_pose, prev_pose, threshold):
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
			self.drawing.draw_landmarks(frame, current_pose.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

			if self.prev_pose is not None:
				if self._detect_movement(current_pose.pose_landmarks, self.prev_pose, .005):
					for (x, y, w, h) in faces:
						cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
						self._shot(current_pose, frame)
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

# class MoveDetectorBody:
# 	def __init__(self):
# 		pass


class HandGesture:
	def __init__(self):
		self.cap = cv.VideoCapture(0)
		self.mp_hands = mp.solutions.hands
		self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
		self.drawing = mp.solutions.drawing_utils

	def start(self):
		while True:
			_, frame = self.cap.read()
			x, y, c = frame.shape
			rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
			result = self.hands.process(rgb_frame)
			# Flip the frame vertically
			# frame = cv.flip(frame, 1)

			className = ''

			# post process the result
			if result.multi_hand_landmarks:
				landmarks = []
				for handslms in result.multi_hand_landmarks:
					for lm in handslms.landmark:
					# print(id, lm)
						lmx = int(lm.x * x)
						lmy = int(lm.y * y)

						landmarks.append([lmx, lmy])

						# Drawing landmarks on frames
						self.drawing.draw_landmarks(frame, handslms, self.mp_hands.HAND_CONNECTIONS)
			# Show the final output
			cv.imshow("Output", frame)
			if cv.waitKey(1) == ord('q'):
				break

		# release the webcam and destroy all active windows
		self.cap.release()
		cv.destroyAllWindows()


def main():
	# md = MoveDetector()
	# md.start()

	hg = HandGesture()
	hg.start()


if __name__ == '__main__':
	main()
