import cv2

cam = cv2.VideoCapture(0)  # подключаем камеру

# указываем координаты
x = 320
y = 240

while True:
    ret, frame = cam.read()  # получаем кадр

    # рисуем квадрат
    cv2.rectangle(frame, (x + 1, y + 1), (x - 1, y - 1), (255, 255, 255), 1)

    # находим цвет пикселя
    color = frame[y][x]

    # печатаем цвет
    print(f'Цвет пикселя с координатами {x} {y}: {color}')

    # вызываем окно "frame from webcam" и показываем кадр
    cv2.imshow("frame from webcam", frame)

    # отслеживаем нажатие клавиши "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()  # разрушить дочерние окна программы
cam.release()  # разрывает соединение с камерой