import cv2
import numpy as np


def cv_setup(game):
    cv_init(game)
    cv_update(game)


def cv_init(game):
    game.cap = cv2.VideoCapture()
    if not game.cap.isOpened():
        game.cap.open(-1)
    # rest of init


def cv_update(game):
    cap = game.cap
    if not cap.isOpened():
        cap.open(0)
    ret, image = cap.read()
    image = image[:, ::-1, :]
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    verde_min = np.array([34, 42, 0])
    verde_max = np.array([84, 255, 255])
    verde_mascara = cv2.inRange(image_hsv, verde_min, verde_max)
    verde = cv2.bitwise_and(image, image, mask=verde_mascara)

    vermelho_min = np.array([161, 155, 84])
    vermelho_max = np.array([179, 255, 255])
    vermelho_mascara = cv2.inRange(image_hsv, vermelho_min, vermelho_max)
    vermelho = cv2.bitwise_and(image, image, mask=vermelho_mascara)

    cv_process(verde)
    cv_output2(verde)

    cv_process(image)
    cv_output3(image)

    cv_process(vermelho)
    cv_output(vermelho)

    vermelho_existe = np.sum(vermelho_mascara)
    verde_existe = np.sum(verde_mascara)

    if verde_existe > 200000:
        game.paddle.move(+1)
    else:
        game.paddle.move(0)

    if vermelho_existe > 200000:
        game.paddle.move(-1)
    else:
        game.paddle.move(0)

    game.after(1, cv_update, game)


def cv_process(image):
    # main image processing code
    pass


def cv_output(image):
    cv2.imshow("Vermelho", image)
    # rest of output rendering
    cv2.waitKey(1)


def cv_output2(image):
    cv2.imshow("Verde", image)
    # rest of output rendering
    cv2.waitKey(1)


def cv_output3(image):
    cv2.imshow("Imagem", image)
    # rest of output rendering
    cv2.waitKey(1)