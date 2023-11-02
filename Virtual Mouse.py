import cv2
import numpy as np
import time
import HandTracking as ht
import pyautogui

### Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 130             # Frame Rate
smoothening = 4         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(10, width)           # Adjusting size
cap.set(12, height)

detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max

while True:
    success, img = cap.read()
    img = detector.findHands(img)                       # Finding the hand
    lmlist, bbox = detector.findPosition(img)           # Getting the position of the hand

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingersUp()      # Checking if fingers are upwards
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)   # Creating a boundary box

        if fingers[1] == 1 and fingers[2] == 0:  # If the forefinger is up and the middle finger is down
            x3 = np.interp(x1, (frameR, width - frameR), (0, pyautogui.size()[0]))
            y3 = np.interp(y1, (frameR, height - frameR), (0, pyautogui.size()[1]))

            curr_x = prev_x + (x3 - prev_x) / smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            pyautogui.moveTo(pyautogui.size()[0] - curr_x, curr_y)  # Moving the cursor
            prev_x, prev_y = curr_x, curr_y

        if fingers[1] == 1 and fingers[2] == 1:  # If the forefinger & middle finger both are up
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:  # If both fingers are really close to each other
                pyautogui.click()  # Perform Click

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

