import multiprocessing
import sys
from socket import *
import cv2
import mediapipe as mp
import serial
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

def conn(): 
    host = '127.0.0.1'
    port = 22927
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind((host, port))
    except:
        print(f'Bind failed. Error : {sys.exc_info()}')
        sys.exit()
    serverSocket.listen(5)
    print('Waiting...')
    
    connection, address = serverSocket.accept()
    ip, port = str(address[0]), str(address[1])
    print(f'Connected with {ip}:{port}')

    return connection

tcp_data = 'tt'

def tcp():
    global tcp_data

    connection = conn()

    while True:
        data = connection.recv(8192)
        print(data.decode('utf-8'))
        if data.decode('utf-8') == 'close':
            connection.close()
            break
        else:
            connection.send(tcp_data.encode('utf-8'))
            print(tcp_data)

sensor_data = 'ss'

def sensor():
    global sensor_data

    arduino = serial.Serial('COM9', 9600)

    while True:
        a = arduino.readline()
        sensor_data = a.decode()
        # print(serial_data)
        # sensor_data = serial_data
        # print(sensor_data)

if __name__ == '__main__':
    tcp_data = ''
    sensor_data = ''
    # p1 = multiprocessing.Process(target=conn)
    proc_tcp = multiprocessing.Process(target=tcp)
    proc_sensor = multiprocessing.Process(target=sensor)
    # p1.start()
    proc_tcp.start()
    proc_sensor.start()

    cap = cv2.VideoCapture(0)
    with mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            # que.clear()
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = holistic.process(image)

            # Draw landmark annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles
                .get_default_pose_landmarks_style())
            mp_drawing.draw_landmarks(
                image,
                results.left_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles
                .get_default_hand_landmarks_style(),
                connection_drawing_spec=mp_drawing_styles
                .get_default_hand_connections_style())
            mp_drawing.draw_landmarks(
                image,
                results.right_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles
                .get_default_hand_landmarks_style(),
                connection_drawing_spec=mp_drawing_styles
                .get_default_hand_connections_style())
            cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))

            if sensor_data != '':
                print(sensor_data)

            tcp_data = f'sensor : {sensor_data}'

            # print(z1>z2)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
                
    proc_tcp.join()
    proc_sensor.join()
