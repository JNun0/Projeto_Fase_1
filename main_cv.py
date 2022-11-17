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
    image = image[:, ::-1, :]   #Inverte Imagem
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Imagem BGR para HSV

    verde_min = np.array([34, 42, 50])  # verde escuro
    verde_max = np.array([84, 255, 255])  # verde claro
    verde_mascara = cv2.inRange(image_hsv, verde_min, verde_max)  # cores entre ambos

    vermelho_min = np.array([161, 155, 84])
    vermelho_max = np.array([180, 255, 255])
    vermelho_mascara = cv2.inRange(image_hsv, vermelho_min, vermelho_max)

    cv_process_green(image, verde_mascara)
    cv_process_red(image, vermelho_mascara)
    cv_output(image)

    vermelho_existe = np.sum(vermelho_mascara)
    verde_existe = np.sum(verde_mascara)

    conditions(game, verde_existe, vermelho_existe)

    game.after(1, cv_update, game)


def cv_process_green(image, verde_mascara):

    verde = cv2.bitwise_and(image, image, mask=verde_mascara)

    kernel = np.ones((5, 5), np.uint8)

    erosion_vr = cv2.erode(verde, kernel, iterations=1)
    dilate_vr = cv2.dilate(erosion_vr, kernel, iterations=1)

    cv_output_green(dilate_vr)


def cv_process_red(image, vermelho_mascara):

    vermelho = cv2.bitwise_and(image, image, mask=vermelho_mascara)

    kernel = np.ones((5, 5), np.uint8)

    erosion_vm = cv2.erode(vermelho, kernel, iterations=1)
    dilate_vm = cv2.dilate(erosion_vm, kernel, iterations=1)

    cv_output_red(dilate_vm)


def cv_output(image):
    cv2.imshow("Imagem", image)
    # rest of output rendering
    cv2.waitKey(1)


def cv_output_red(image):
    cv2.imshow("Vermelho", image)
    # rest of output rendering
    cv2.waitKey(1)


def cv_output_green(image):
    cv2.imshow("Verde", image)
    # rest of output rendering
    cv2.waitKey(1)


def conditions(game, verde_existe, vermelho_existe):

    if verde_existe > 500000: #número de pixeis verdes > 500 000
        game.paddle.move(+3)
    else:
        game.paddle.move(0)

    if vermelho_existe > 500000:
        game.paddle.move(-3)
    else:
        game.paddle.move(0)

