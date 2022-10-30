import cv2
import numpy as np


def resize_and_padding(image, new_image_width=930, new_image_height=580, color=(0, 0, 0)):
    image = resize_only(image, new_image_width, new_image_height)
    print("after resize only", image.shape)
    image = padding_only(image, new_image_width, new_image_height, color)
    print("after padding only", image.shape)
    # cv2.imshow("res", image)
    # cv2.waitKey()
    return image


def resize_only(image, new_image_width=930, new_image_height=580):
    (x, y, z) = image.shape
    # print(x, y, "1")
    if x > new_image_height and y <= new_image_width:
        image = cv2.resize(image, (int(y * new_image_height / x), new_image_height))
    elif x <= new_image_height and y > new_image_width:
        image = cv2.resize(image, (new_image_width, int(x * new_image_width / y)))
        print("bug")
    (x, y, z) = image.shape
    # print(x, y, "2")
    if (x > new_image_height and y > new_image_width) or (x < new_image_height and y < new_image_width):
        if x / y >= new_image_height / new_image_width:
            image = cv2.resize(image, (int(y * new_image_height / x), new_image_height))
        elif x / y < new_image_height / new_image_width:
            image = cv2.resize(image, (new_image_width, int(x * new_image_width / y)))
    # print(original_image.shape)
    # image = original_image.copy()
    # return image
    return image


def padding_only(image, new_image_width=930, new_image_height=580, color=(0, 0, 0)):
    # image = original_image.copy()
    old_image_height, old_image_width, channels = image.shape

    # create new image of desired size and color (black) for padding
    # new_image_width = 930
    # new_image_height = 580
    # color = (0, 0, 0)
    result = np.full((new_image_height, new_image_width, channels), color, dtype=np.uint8)

    # compute center offset
    x_center = (new_image_width - old_image_width) // 2
    y_center = (new_image_height - old_image_height) // 2

    # copy img image into center of result image
    result[y_center:y_center + old_image_height, x_center:x_center + old_image_width] = image
    # print(result.shape)
    return result
