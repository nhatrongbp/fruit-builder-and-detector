from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage
from padding import *
import imutils


def auto_segmentation(image, rf):
    image = resize_only(image)
    # print(image.shape)

    shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
    # cv2.imshow("shifted", shifted)
    # cv2.waitKey()

    gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv2.imshow("thresh", thresh)
    # cv2.waitKey()

    edt = ndimage.distance_transform_edt(thresh)
    # cv2.imshow("edt", edt)
    # cv2.waitKey()

    local_max = peak_local_max(edt, indices=False, min_distance=40, labels=thresh)
    # perform a connected component analysis on the local peaks,
    # using 8-connectivity, then appy the Watershed algorithm
    markers = ndimage.label(local_max, structure=np.ones((3, 3)))[0]
    labels = watershed(-edt, markers, mask=thresh)
    print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))
    # cv2.imshow("labels", labels)
    # cv2.waitKey()

    # use labels as a mask to masking the image,
    # so that we got only foreground image, with a white background
    labels = np.uint8(labels)
    ret, bg_mask = cv2.threshold(labels, 1, 255, cv2.THRESH_BINARY_INV)
    fg_mask = cv2.bitwise_not(bg_mask)
    white_bg = image.copy()
    white_bg[:, :, :] = 255
    white_bg = cv2.bitwise_and(white_bg, white_bg, mask=bg_mask)
    color_fg = cv2.bitwise_and(image, image, mask=fg_mask)
    image_with_white_bg = cv2.add(white_bg, color_fg)

    for label in np.unique(labels):
        # if the label is zero, we are examining the 'background'
        # so simply ignore it
        if label == 0:
            continue
        # otherwise, allocate memory for the label region and draw
        # it on the mask
        mask = np.zeros(gray.shape, dtype="uint8")
        mask[labels == label] = 255
        # detect contours in the mask and grab the largest one
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        # draw a circle enclosing the object
        # ((x, y), r) = cv2.minEnclosingCircle(c)
        # cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(c)
        if w < 60 or h < 60:
            continue
        # give the "image with white background" to the model for prediction
        print("label", label)
        print("default size", image_with_white_bg[y:y+h, x:x+w].shape)
        print("box", x, y, w, h)
        temp_img = resize_and_padding(image_with_white_bg[y:y+h, x:x+w], 200, 200, color=(255, 255, 255))
        # cv2.imshow("temp", temp_img)
        # draw the prediction to original image
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 1)
        cv2.putText(image, "#{}: {}".format(label, rf.detect_fruit(temp_img)), (int(x), int(y) + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    # show the output image
    # cv2.imshow("final", image)
    # cv2.waitKey()
    return image


def manual_segmentation(original_image, bounding_boxx):
    # print(original_image.shape, bounding_boxx)
    # 2 statements below are to resize 1:2 (to run faster):
    # original_image = cv2.resize(original_image, (int(original_image.shape[1]/2), int(original_image.shape[0]/2)))
    # bounding_box = (
    #     int(bounding_boxx[0]/2),
    #     int(bounding_boxx[1]/2),
    #     int(bounding_boxx[2]/2),
    #     int(bounding_boxx[3]/2)
    # )
    bounding_box = bounding_boxx
    # print(original_image.shape, bounding_boxx)
    #
    segment = np.zeros(original_image.shape[:2], np.uint8)

    x, y, width, height = bounding_box
    segment[y:y + height, x:x + width] = 1

    background_mdl = np.zeros((1, 65), np.float64)
    foreground_mdl = np.zeros((1, 65), np.float64)

    cv2.grabCut(original_image, segment, bounding_box, background_mdl, foreground_mdl, 5,
                cv2.GC_INIT_WITH_RECT)

    new_mask = np.where((segment == 2) | (segment == 0), 0, 1).astype('uint8')

    original_imagee = original_image * new_mask[:, :, np.newaxis]

    background = original_image - original_imagee
    background[np.where((background > [0, 0, 0]).all(axis=2))] = [255, 255, 255]
    original_imagee = background + original_imagee

    # if cv2.getWindowProperty('Result', cv2.WND_PROP_VISIBLE):
    #     cv2.destroyWindow('Result')
    # cv2.imshow('Result', original_imagee[
    #                      bounding_box[1]:bounding_box[1]+bounding_box[3],
    #                      bounding_box[0]:bounding_box[0]+bounding_box[2]])
    # cv2.moveWindow('Result', 0, 0)
    up = bounding_box[1]
    down = bounding_box[3]
    left = bounding_box[0]
    right = bounding_box[2]
    # print(np.mean(original_imagee[up, left: left+right]))

    # remove top rows which are full of white
    while np.mean(original_imagee[up, left:left+right]) == 255:
        up += 1
        down -= 1

    # remove bottom rows which are full of white
    while np.mean(original_imagee[up+down-1, left:left + right]) == 255:
        down -= 1

    # remove left cols which are full of white
    while np.mean(original_imagee[up:up+down, left]) == 255:
        left += 1
        right -= 1
    # remove left cols which are full of white
    while np.mean(original_imagee[up:up + down, left+right-1]) == 255:
        right -= 1

    # cv2.imshow("bug", original_imagee[up:up+down, left:left+right])
    return original_imagee[up:up+down, left:left+right]
