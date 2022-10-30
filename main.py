# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from segmentation import *
from classifier import RandomForest
from drawer import *
from tkinter import *
from tkinter import filedialog, messagebox

global x_pt, y_pt, drawing, top_left_point, bottom_right_point, original_image, image, xx, yy, mode, filename, root, rf


def draw_bounding_box(click, x, y, flag_param, parameters):
    global x_pt, y_pt, top_left_point, bottom_right_point, drawing, xx, yy, mode, original_image, filename, root
    xx = x
    yy = y
    if x <= 50 or x >= 980 or y <= 100 or y >= 680:
        # print("out of bound")
        if click == cv2.EVENT_LBUTTONUP and 1030 < xx < 1230 and 400 < yy < 450:
            if np.mean(original_image) == 0:
                print("choose an image first")
                messagebox.showinfo("choose an image first", "choose an image first")
                return
            mode = "manual"
            print("clicked manual")
            image[100:680, 50:980] = original_image
        elif click == cv2.EVENT_LBUTTONUP and 1030 < xx < 1230 and 470 < yy < 520:
            print("clicked auto")
            if np.mean(original_image) == 0:
                print("choose an image first")
                messagebox.showinfo("choose an image first", "choose an image first")
            else:
                mode = "auto"
                cv2.rectangle(image, (1030, 100), (1230, 350), (255, 255, 255), -1)
                root.deiconify()
                image[100:680, 50:980] = resize_and_padding(auto_segmentation(cv2.imread(filename), rf))
                root.withdraw()
        elif click == cv2.EVENT_LBUTTONUP and 1030 < xx < 1230 and 540 < yy < 590:
            if np.mean(original_image) == 0:
                print("choose an image first")
                messagebox.showinfo("choose an image first", "choose an image first")
                return
            elif cv2.imread(filename).shape != (100, 100, 3):
                messagebox.showinfo("your image was not preprocessed",
                                    "preprocessed image must contain only one fruit, max scale to the center of a "
                                    "100x100 rectangle, and filled with white background")
                return
            else:
                mode = "preprocessed"
                cv2.rectangle(image, (465, 340), (565, 440), (255, 255, 0), 1)
                cv2.putText(image, rf.detect_fruit(cv2.imread(filename)), (465, 335),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            print("clicked preprocess")
        elif click == cv2.EVENT_LBUTTONUP and 1030 < xx < 1230 and 630 < yy < 680:
            filename = filedialog.askopenfilename(initialdir="images", title="Select A File",
                                                  filetypes=(("jpg files", "*.jpg"), ("png files", "*.png")))
            if filename:
                mode = "upload"
                print(filename)
                original_image = cv2.imread(filename, cv2.IMREAD_COLOR)
                if original_image.shape == (100, 100, 3):
                    original_image = padding_only(original_image)
                else:
                    original_image = resize_and_padding(original_image)
                image[100:680, 50:980] = original_image
                cv2.rectangle(image, (1030, 100), (1230, 350), (255, 255, 255), -1)
        return

    if click == cv2.EVENT_LBUTTONDOWN and mode == "manual":
        drawing = True
        x_pt, y_pt = x, y

    elif click == cv2.EVENT_LBUTTONUP and mode == "manual":
        drawing = False
        # top_left_point, bottom_right_point = (x_pt, y_pt), (x, y)
        top_left_point, bottom_right_point = (min(x_pt, x), min(y_pt, y)), (max(x_pt, x), max(y_pt, y))
        # cv2.rectangle(image, top_left_point, bottom_right_point, (0, 255, 0), 2)
        draw_border(image, (min(x_pt, x), min(y_pt, y)), (min(x_pt, x) + abs(x - x_pt), min(y_pt, y) + abs(y - y_pt)),
                    (0, 255, 0), 2, 5, 10)
        bounding_box = (min(x_pt, x) - 50, min(y_pt, y) - 100, abs(x - x_pt), abs(y - y_pt))
        # print(x_pt, y_pt, x - x_pt, y - y_pt)
        root.deiconify()
        temp_img = resize_and_padding(manual_segmentation(original_image, bounding_box), 200, 200,
                                      color=(255, 255, 255))
        cv2.putText(image, rf.detect_fruit(temp_img), top_left_point, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        image[100:300, 1030:1230, :] = temp_img
        # cv2.imshow("f", temp_img)
        root.withdraw()


def my_main():
    global drawing, image, original_image, top_left_point, bottom_right_point, xx, yy, mode, x_pt, y_pt, root, rf
    # initialize
    drawing = False
    top_left_point, bottom_right_point = (-1, -1), (-1, -1)
    xx, yy = -1, -1
    x_pt, y_pt = -1, -1
    mode = "upload"
    rf = RandomForest()

    # original_image = cv2.imread("grant.jpg")
    # original_image = padding_image(original_image)
    original_image = np.zeros((580, 930, 3), np.uint8)
    cv2.namedWindow('Frame', cv2.WND_PROP_VISIBLE)
    cv2.moveWindow('Frame', 250, 0)
    image = np.zeros((720, 1280, 3), np.uint8)
    image[:, :] = (255, 255, 255)
    # image[100:680, 50:980] = original_image
    # print(image[0:580, 0:930].shape)
    # print(original_image.shape)

    cv2.setMouseCallback('Frame', draw_bounding_box)

    root = Tk()
    root.title('Image is being processing. Please wait')
    root.geometry("400x40+560+360")
    root.withdraw()

    while True:
        if drawing:
            draw_gui(image.copy(), drawing, mode, x_pt, y_pt, xx, yy)
        else:
            draw_gui(image, drawing, mode, x_pt, y_pt, xx, yy)

        c = cv2.waitKey(1)
        if c == 27:
            break
    root.destroy()
    cv2.destroyAllWindows()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    my_main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
