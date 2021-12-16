import cv2

cam = cv2.VideoCapture(-1)  # подключаем камеру

while True:
    ret, frame = cam.read()  # получаем кадр

    # вызываем окно "frame from webcam" и показываем кадр
    cv2.imshow("frame from webcam", frame)

    # отслеживаем нажатие клавиши "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()  # разрушить дочерние окна программы
cam.release()  # разрывает соединение с камерой
