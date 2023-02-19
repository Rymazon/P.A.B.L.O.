from sre_constants import SUCCESS
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

import serial 
import math
from time import sleep
i = 0
arduino = serial.Serial('COM11', 9600)
loop = True

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened() and loop:
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        average = 0
        nums = 0
        for ids, landmrk in enumerate(hand_landmarks.landmark):
            average += landmrk.x
            nums += 1
        
        average = average/nums
        Horizontal = max(min(math.floor(average * 225),225),0)
        i += 1
        if (i % 10) == 0:
            msg_to_send = str(Horizontal)
            msg_to_send += '\n'
            print (f'Sending: {msg_to_send}')
            msg_to_send = msg_to_send.encode('ASCII')
            arduino.write(msg_to_send)
            loop = False

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()