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

    verde_min = np.array([25, 52, 72])
    verde_max = np.array([102, 255, 255])
    verde_mascara = cv2.inRange(image_hsv, verde_min, verde_max)
    # mete a mascára por cima da image para apenas aparecer a cor
    verde = cv2.bitwise_and(image, image, mask=verde_mascara)

    vermelho_min = np.array([161, 155, 84])
    vermelho_max = np.array([179, 255, 255])
    vermelho_mascara = cv2.inRange(image_hsv, vermelho_min, vermelho_max)
    vermelho = cv2.bitwise_and(image, image, mask=vermelho_mascara)

    cv_process2(verde)
    cv_output2(verde)

    cv_process(vermelho)
    cv_output(vermelho)
    # game.paddle.move(-1)
    game.after(1, cv_update, game)


def cv_process(image):
    # main image processing code
    pass


def cv_process2(image):
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