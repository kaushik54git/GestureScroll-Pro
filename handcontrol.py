# Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
# face_utils for basic operations of conversion
from imutils import face_utils
# to scroll up/down
import pyautogui
# to calculate tan inverse
import math
# to save screen shots
import os
# to scroll/capturing screen shots
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize the hand tracking module
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)



def livevideo():
    cy=0
    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(image)

        # If a hand is detected, get its landmarks and calculate the y-coordinate of the tip of the index finger
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            # Get index finger landmarks
            index_finger_base_landmarks = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            y = int(index_tip.y * frame.shape[0])
            x = int(index_tip.x * frame.shape[1])

            height, width, _ = frame.shape
            bx, by = int(index_finger_base_landmarks.x * width), int(index_finger_base_landmarks.y * height)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            distance = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)

            dis=round(distance,2)
            middle_x, middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        
            indexx_x, indexx_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                

            # Calculate angle between base and tip landmarks
            angle = math.degrees(math.atan2(y - by, x - bx))
            angle1 = math.degrees(math.atan2(indexx_y - middle_y,indexx_x - middle_x))
            


            if(dis>0.25):
                # Scroll up the page if the finger is moved down
                if (angle<=-40 and angle>=-130):
                    if (y >=-200 and y<=200):
                        pyautogui.scroll(400)
                # Scroll down the page if the finger is moved up
                elif (angle>=40 and angle<=130):
                    if y>=300:
                        pyautogui.scroll(-400)

                else :
                    if x <=400:
                        pyautogui.keyDown('shift')
                        pyautogui.hscroll(200)
                        pyautogui.keyUp('shift')
                # Scroll right if the finger is moved left
                    elif x>=200:
                        pyautogui.keyDown('shift')
                        pyautogui.hscroll(-200)
                        pyautogui.keyUp('shift')
                    else: pass

            # Zoom in if the fingers are moved closer together
            if dis>=0.2 and dis<0.25:
                pyautogui.keyDown('ctrl')
                pyautogui.scroll(100)
                pyautogui.keyUp('ctrl')
            # Zoom out if the fingers are moved farther apart
            elif dis<0.2 and dis>0.07:
                pyautogui.keyDown('ctrl')
                pyautogui.scroll(-100)
                pyautogui.keyUp('ctrl')


            # to take screenshot
            if angle>=130 and angle<=150 :
                print("it is inside")
            # take screenshot of entire screen
                im = pyautogui.screenshot()
                # save screenshot to a file
                im.save(os.path.join(os.getcwd(), 'screenshot.png'))
                # display screenshot
                im.show()
                



            # Draw the landmarks on the frame for visualization
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the resulting image
        cv2.imshow('Hand Tracking', frame)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break

        cv2.imshow("Frame", frame)
livevideo()
 