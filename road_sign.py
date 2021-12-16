import cv2

cam = cv2.VideoCapture(-1)  # подключаем камеру

# ------------------------- подготавливаем исходные картинки -------------------------------------------
right_sign = cv2.imread('right.png')  # открываем изображение
right_sign = cv2.resize(right_sign, (40, 40))  # изменяем размер на 40x40
# ВНИМАНИЕ! Параметр lowerb подбирается вручную!
right_sign = cv2.inRange(right_sign, lowerb=(90, 90, 150), upperb=(255, 255, 255))  # переводим в ЧБ

man_sign = cv2.imread('man.png')  # открываем изображение
man_sign = cv2.resize(man_sign, (40, 40))  # изменяем размер на 40x40
# ВНИМАНИЕ! Параметр lowerb подбирается вручную!
man_sign = cv2.inRange(man_sign, lowerb=(90, 90, 150), upperb=(255, 255, 255))  # переводим в ЧБ
# -------------------------------------------------------------------------------------------------------


while True:
    ret, frame = cam.read()  # получаем кадр

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # переводим картинку в HSV
    hsv = cv2.blur(hsv, (5, 5))  # делаем небольшое размытие

    # переводим картинку в ЧБ
    # ВНИМАНИЕ! Параметр lowerb подбирается вручную!
    mask = cv2.inRange(hsv, lowerb=(80, 80, 80), upperb=(255, 255, 255))

    # Убираем большинство помех
    # ВНИМАНИЕ! параметр iterations настраивается вручную!
    mask = cv2.erode(mask, None, iterations=2)  # делаем эрозию
    mask = cv2.dilate(mask, None, iterations=4)  # увеличиваем области объектов

    # находим контуры
    contours1, hierarchy1 = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # если контуры найдены
    if contours1:
        image_copy1 = frame.copy()  # создаем копью исходного кадра
        c = max(contours1, key=cv2.contourArea)  # находим самый большой объект из контуров
        x, y, w, h = cv2.boundingRect(c)  # получаем начальные координаты, ширину и высоту объекта

        sign_from_image = frame[y:y + h, x:x + w]  # получаем обрезанный объект из исходного кадра
        sign_from_image = cv2.resize(sign_from_image, (40, 40))  # изменяем размер на 40x40

        # ВНИМАНИЕ! Параметр lowerb подбирается вручную!
        sign_from_image = cv2.inRange(sign_from_image, (90, 90, 150), (255, 255, 255))  # переводим в ЧБ

        # выводим в отдельные окна полученный знак и два исходных
        cv2.imshow("sign", sign_from_image)
        cv2.imshow("man", man_sign)
        cv2.imshow("right", right_sign)

        # обнуляем/создаем счетчики
        counter_right = 0
        counter_man = 0

        # цикл проходится по пикселям картинок с помощью координат
        for i in range(40):
            for j in range(40):

                # если пиксель полученного знака совпадает с исходным, то прибавляем к счетчику 1
                if right_sign[i][j] == sign_from_image[i][j]:
                    counter_right += 1
                # аналогичное действие для второго знака
                if man_sign[i][j] == sign_from_image[i][j]:
                    counter_man += 1

        # если значение счетчика выше порогового (1200), то мы определили знак и выведем в консоль
        # ВНИМИНИЕ! Пороговое значение срабатывания подбирается вручную, воспользуйтесь строкой кода под номером 74,
        # чтобы узнать значения для Вашего случая!
        if counter_right > 1200:
            print("Знак \"Поворот направо\"")
        # аналогичное действие для второго знака
        if counter_man > 1200:
            print("Знак \"Пешеходный переход\"")

        # print(f"Вправо:{counter_right}     Пешеход:{counter_man}")

    # отслеживаем нажатие клавиши "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()  # разрушаем дочерние окна программы
cam.release()  # разрываем соединение с камерой
