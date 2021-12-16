import cv2

cam = cv2.VideoCapture(-1)  # подключаем камеру

# указываем разрешение камеры
camera_height = 480
camera_width = 640

start_point = 0  # заводим переменную старта линии
end_point = camera_width  # заводим переменную конца линии

while True:
    ret, frame = cam.read()  # получаем кадр

    # получаем картинку из серых тонов
    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # переводим картинку в черно-белую
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

    # получим нижнюю строчку картинки
    crop_img = blackAndWhiteImage[camera_height-1:camera_height, 0:camera_width]

    # проходимся циклом по пикселям в нижней строчке
    for index in range(camera_width):

        # если встретили черный, то заходим во второй цикл и запоминаем старт линии
        # выходим из цикла, если достигнем конца черной линии
        if crop_img[0][index] == 0:
            start_point = index
            while crop_img[0][index] == 0:
                end_point = index  # запоминаем конечное положение линии
                index += 1

                # если мы достигли конца, то выходим из цикла
                if index == camera_width:
                    break
            break

    # находим координату центра линии
    center_point = (start_point + end_point)//2

    # указываем точки для отрисовки пометки
    pt1 = (center_point-2, camera_height - 10)
    pt2 = (center_point+2, camera_height - 6)
    color = (255, 255, 255) # цвет белый
    thickness = -1  # с заполнением внутри
    cv2.rectangle(frame, pt1, pt2, color, thickness)  # рисуем квадрат-пометку

    # вызываем окно "frame from webcam" и показываем кадр
    cv2.imshow('cam', frame)

    # отслеживаем нажатие клавиши "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()  # разрушаем дочерние окна программы
cam.release()  # разрываем соединение с камерой
