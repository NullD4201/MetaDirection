import cv2
import mediapipe as mp
import numpy as np
import serial

# port = input('Enter Arduino Port: ')

# ser = serial.Serial('COM' + str(port), 9600, timeout=1)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0)


with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        # arduinoText = ser.readline().decode('utf-8')
        # if len(arduinoText) != 0:
        #     print('<Arduino> ' + arduinoText)

        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        results = holistic.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
                                  mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                                  mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
                                  )
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                                  )
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                                  )
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Debug Screen', image)

        head_center_x = (results.pose_landmarks.landmark[11].x + results.pose_landmarks.landmark[12].x) / 2
        if round(head_center_x, 2) < round(results.pose_landmarks.landmark[0].x, 2):
            print('Head Turn Right [' + str(abs(results.pose_landmarks.landmark[0].x - head_center_x)) + ']')
        elif round(head_center_x, 2) > round(results.pose_landmarks.landmark[0].x, 2):
            print('Head Turn Left [' + str(abs(results.pose_landmarks.landmark[0].x - head_center_x)) + ']')
        else:
            print('Head Center [' + str(abs(results.pose_landmarks.landmark[0].x - head_center_x)) + ']')
        head_center_y = (results.pose_landmarks.landmark[4].y + results.pose_landmarks.landmark[10].y) / 2
        if round(head_center_y, 2) < round(results.pose_landmarks.landmark[0].y, 2):
            print('Head Up [' + str(abs(results.pose_landmarks.landmark[0].y - head_center_y)) + ']')
        elif round(head_center_y, 2) > round(results.pose_landmarks.landmark[0].y, 2):
            print('Head Down [' + str(abs(results.pose_landmarks.landmark[0].y - head_center_y)) + ']')
        else:
            print('Head Mid [' + str(abs(results.pose_landmarks.landmark[0].y - head_center_y)) + ']')

        if cv2.waitKey(10) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()