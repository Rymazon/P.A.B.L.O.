from asyncio import sleep
from multiprocessing.connection import wait
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

maxangle = 45

import serial 
import math

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

frame = 0
x = 0
coord = 0
y=0
ids = 1
i = 1

arduino = serial.Serial('COM11', 9600)

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    frame += 1

    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    #### To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
    image_height, image_width, _ = image.shape
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        if frame == 30:
          
          for hand_landmarks in results.multi_hand_landmarks:
            # Here is How to Get All the Coordinates
            #ids = 1
            if (i<2):
                for ids, landmrk in enumerate(hand_landmarks.landmark):
                    x= ids
                    coord=landmrk
                    
                    #cx, cy = landmrk.x * image_width, landmrk.y*image_height
                    # print(cx, cy)
                    # print (ids, cx, cy)
                    i=5
            
            angle = 0

            print(coord.x)
            print(coord.y)
            print(coord.z)

            Horizontal = math.floor(coord.x * 255)
            print (Horizontal)
            arduino.write(Horizontal)
            cap.release()

            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break







