import sys
import time

import qdarkstyle
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, \
    QProgressBar, QComboBox, QFileDialog, QMessageBox, QSplashScreen
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QColor, QFont, QPainter, QIcon, QImage, QPen
from qtwidgets import AnimatedToggle
from padding import *
from segmentation import manual_segmentation
from random import randint


class MyApp(QWidget):
    dictionary = {
        'Avocado': 0,
        'Banana': 0,
        'Lychee': 0,
        'Mangostan': 0,
        'Pineapple': 0,
        'Pitahaya': 0,
        'Rambutan': 0,
        'Strawberry': 0,
        'Walnut': 0,
        'Watermelon': 0
    }

    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1305, 770
        self.setFixedSize(self.window_width, self.window_height)
        self.setWindowTitle("Fruit dataset builder 2.0 - IT worker edition (developed by B19OLP081)")
        self.setWindowIcon(QIcon('icons/object-scanning-6266289-5233903.png'))
        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.theme = "Dark"
        # number of saved images
        rf = open('data.txt')
        for x in self.dictionary:
            self.dictionary[x] = int(rf.readline())
        rf.close()
        # print(self.dictionary['Banana'])
        self.image_path = ""
        self.cv_image = np.zeros((580, 930, 3), np.uint8)
        self.preprocessed_image = np.zeros((100, 100, 3), np.uint8)
        # self.cv_image = cv2.imread(self.image_path)
        self.qt_image = QPixmap("temp/getstarted.jpg")
        # self.qt_image = QPixmap(930, 580)
        # self.qt_image.fill(QColor("#455364"))
        self.temp_qt_image = self.qt_image.copy()
        self.begin, self.destination = QPoint(), QPoint()

        # left GUI
        self.left_groupbox = QGroupBox("PREVIEW", self)
        self.left_groupbox.move(34, 25)
        self.left_groupbox.setFixedSize(960, 725)
        self.left_groupbox.setFont(QFont('Arial', 20))

        vbox = QVBoxLayout()
        self.left_groupbox.setLayout(vbox)
        hbox = QHBoxLayout()
        # add pixmap to vbox
        self.qt_label = QLabel()
        self.qt_label.setPixmap(self.qt_image)
        vbox.addStretch()
        vbox.addWidget(self.qt_label)
        #
        vbox.addStretch()
        vbox.addLayout(hbox)

        toggle_1 = AnimatedToggle(
            checked_color="#FFB000",
            pulse_checked_color="#44FFB000"
        )
        toggle_1.setMinimumHeight(50)
        toggle_1.clicked.connect(self.switch_theme)
        hbox.addWidget(toggle_1)

        self.label_theme = QLabel(self.theme)
        self.label_theme.setFont(QFont('Arial', 14))
        hbox.addWidget(self.label_theme)
        hbox.addStretch()
        btn_upload = QPushButton("  Choose file")
        btn_upload.setIcon(QIcon("icons/upload.png"))
        btn_upload.setFont(QFont('Arial', 14))
        btn_upload.setMinimumSize(200, 50)
        btn_upload.clicked.connect(self.choose_file)
        hbox.addWidget(btn_upload)

        # right GUI
        self.right_groupbox = QGroupBox("RESULT", self)
        self.right_groupbox.move(1025, 25)
        self.right_groupbox.setFixedSize(250, 725)
        self.right_groupbox.setFont(QFont('Arial', 20))

        vbox = QVBoxLayout()
        self.right_groupbox.setLayout(vbox)
        self.qt_result_image = QPixmap(200, 200)
        self.qt_result_image.fill(QColor("#455364"))
        self.qt_result_label = QLabel()
        self.qt_result_label.setPixmap(self.qt_result_image)
        # vbox.addSpacing(25)
        self.custom_spacing = QLabel(self)
        self.custom_spacing.setMinimumHeight(20)
        self.custom_spacing.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        vbox.addWidget(self.custom_spacing)
        # vbox.addStretch()
        vbox.addWidget(self.qt_result_label, alignment=Qt.AlignCenter)
        self.pbar = QProgressBar(self)
        # self.pbar.setValue(50)
        vbox.addWidget(self.pbar)
        # class and combo box classes
        hbox = QHBoxLayout()
        label = QLabel("Class:")
        label.setFont(QFont('Arial', 12))
        hbox.addWidget(label)
        self.combo_box = QComboBox(self)
        self.combo_box.addItems([
            "Avocado", "Banana", "Lychee", "Mangostan", "Pineapple",
            "Pitahaya", "Rambutan", "Strawberry", "Walnut", "Watermelon"
        ])
        self.combo_box.setFont(QFont('Arial', 12))
        hbox.addWidget(self.combo_box)
        vbox.addLayout(hbox)
        #
        vbox.addStretch()
        label = QLabel("Crop only ONE fruit object per time. "
                       "Seriously choose the CORRECT class before saving the image. "
                       "We need your co-operation as a good worker. So... hope the cropped image in a good quality")
        label.setFont(QFont('Arial', 12))
        label.setWordWrap(True)
        # label.setAlignment(Qt.AlignJustify)
        vbox.addWidget(label)
        btn_save = QPushButton("  Save")
        btn_save.setIcon(QIcon("icons/diskette.png"))
        btn_save.setFont(QFont('Arial', 14))
        btn_save.setMinimumSize(200, 50)
        btn_save.clicked.connect(self.save_image)
        vbox.addWidget(btn_save)

    def choose_file(self):
        path, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "Jpg Files (*.jpg);;Png Files (*.png)")
        if check:
            self.image_path = path
            print(self.image_path)
            self.cv_image = cv2.imread(self.image_path)
            # cv2.imshow("f", self.cv_image)
            (x, y, z) = self.cv_image.shape
            if x <= 580 and y <= 930:
                self.cv_image = padding_only(self.cv_image)
                print("padding only")
            else:
                self.cv_image = resize_and_padding(self.cv_image)
                print("resize and padding")
            self.cv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
            # cv2.imshow("g", cv2.cvtColor(self.cv_image, cv2.COLOR_RGB2BGR))
            height, width, channel = self.cv_image.shape
            bytes_per_line = 3 * width
            self.qt_image = QPixmap(QImage(self.cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888))
            self.qt_label.setPixmap(self.qt_image)
            #
            self.preprocessed_image[:, :] = (0, 0, 0)
            temp_image = cv2.resize(self.preprocessed_image, (200, 200))
            height, width, channel = temp_image.shape
            bytes_per_line = 3 * width
            self.qt_result_image = QPixmap(QImage(temp_image.data, width, height, bytes_per_line, QImage.Format_RGB888))
            self.qt_result_label.setPixmap(self.qt_result_image)

    def save_image(self):
        if np.mean(self.preprocessed_image) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("There is no image to save! You have to crop the image first")
            msg.setWindowTitle("Blank image exception")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        print(self.combo_box.currentText())
        cv2.imwrite("train/" + str(self.combo_box.currentText()) + "/"
                    + str(self.dictionary[self.combo_box.currentText()]) + "_100.jpg",
                    cv2.cvtColor(self.preprocessed_image, cv2.COLOR_RGB2BGR))
        self.dictionary[self.combo_box.currentText()] += 1
        wf = open('data.txt', 'w')
        for x in self.dictionary:
            wf.writelines(str(self.dictionary[x]) + '\n')
        wf.close()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Saved image at: train/" + str(self.combo_box.currentText()) + "/"
                    + str(self.dictionary[self.combo_box.currentText()] - 1) + "_100.jpg")
        msg.setWindowTitle("Image saved successfully")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def switch_theme(self):
        if self.theme == 'Dark':
            self.theme = 'Light'
            self.setStyleSheet("")
            self.qt_label.hide()
            # self.qt_result_label.hide()
            self.custom_spacing.hide()
            if self.image_path == '':
                # self.qt_image.fill(QColor("#fdfdfd"))
                self.qt_result_image.fill(QColor("#fdfdfd"))
        else:
            self.theme = 'Dark'
            self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
            self.qt_label.show()
            # self.qt_result_label.show()
            self.custom_spacing.show()
            if self.image_path == '':
                # self.qt_image.fill(QColor('#455364'))
                self.qt_result_image.fill(QColor('#455364'))
        self.label_theme.setText(self.theme)
        self.qt_label.setPixmap(self.qt_image)
        self.qt_result_label.setPixmap(self.qt_result_image)
        # self.image_path = "1"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green, 3, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawPixmap(QPoint(50, 70), self.qt_image)
        # painter.drawPixmap(QPoint(1050, 73), self.qt_result_image)
        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin + QPoint(50, 70), self.destination + QPoint(50, 70))
            painter.drawRoundedRect(rect.normalized(), 20.0, 15.0)

    def mousePressEvent(self, event):
        if self.image_path == "":
            return
        if event.buttons() & Qt.LeftButton:
            # print('left mouse downed')
            self.begin = event.pos() - QPoint(50, 70)
            self.destination = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if self.image_path == "":
            return
        # print(event.pos())
        if event.buttons() & Qt.LeftButton:
            #
            self.temp_qt_image = self.qt_image.copy()
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.temp_qt_image)
            painter.setPen(QPen(Qt.green, 3, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawRoundedRect(rect.normalized(), 20.0, 15.0)
            self.qt_label.setPixmap(self.temp_qt_image)
            # print('left mouse moving')
            self.destination = event.pos() - QPoint(50, 70)
            self.update()

    def mouseReleaseEvent(self, event):
        if self.image_path == "":
            return
        if event.button() & Qt.LeftButton:
            if min(self.begin.x(), self.destination.x()) < 0 \
                    or max(self.begin.x(), self.destination.x()) > 930 \
                    or min(self.begin.y(), self.destination.y()) < 0 \
                    or max(self.begin.y(), self.destination.y()) > 580:
                return
            # print('left mouse up')
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.qt_image)
            painter.setPen(QPen(Qt.green, 3, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawRoundedRect(rect.normalized(), 20.0, 15.0)
            self.qt_label.setPixmap(self.qt_image)
            print(self.begin, self.destination)
            self.pbar.setValue(randint(1, 100))
            self.grabcut()
            self.pbar.setValue(100)
            self.begin, self.destination = QPoint(), QPoint()
            self.update()

    def grabcut(self):
        bounding_box = (
            min(self.begin.x(), self.destination.x()),
            min(self.begin.y(), self.destination.y()),
            abs(self.begin.x() - self.destination.x()),
            abs(self.begin.y() - self.destination.y())
        )
        self.preprocessed_image = resize_and_padding(manual_segmentation(self.cv_image, bounding_box), 100, 100,
                                                     color=(255, 255, 255))
        # print(self.preprocessed_image.shape)
        temp_image = cv2.resize(self.preprocessed_image, (200, 200))
        height, width, channel = temp_image.shape
        bytes_per_line = 3 * width
        self.qt_result_image = QPixmap(QImage(temp_image.data, width, height, bytes_per_line, QImage.Format_RGB888))
        self.qt_result_label.setPixmap(self.qt_result_image)


class PlashSpeed(QSplashScreen):
    def __init__(self, q_pixel_map):
        super(PlashSpeed, self).__init__(q_pixel_map)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        vbox = QVBoxLayout()
        label_spacing = QLabel()
        label_spacing.setFixedHeight(360)
        label_spacing.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        vbox.addWidget(label_spacing)
        self.pbar = QProgressBar(self)
        vbox.addWidget(self.pbar)
        self.setLayout(vbox)

    def progress(self):
        for i in range(70):
            time.sleep(0.01)
            self.pbar.setValue(i)
        time.sleep(1)
        for i in range(30):
            time.sleep(0.01)
            self.pbar.setValue(i+71)


if __name__ == '__main__':
    # don't auto-scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    # app.setStyle('windowsvista')
    # app.setStyleSheet('''
    #     QWidget {
    #         font-size: 30px;
    #     }
    # ''')
    # splash = QSplashScreen(QPixmap("temp/getstarted.jpg"))
    # vbox = QVBoxLayout()
    # label = QLabel("Fruit Dataset Builder - IT worker edition")
    # label.setMinimumWidth(650)
    # vbox.addWidget(label)
    # vbox.addWidget(QProgressBar())
    # splash.setLayout(vbox)
    splash = PlashSpeed(QPixmap("temp/plashSpeed.jpg"))
    splash.show()
    splash.progress()
    myApp = MyApp()
    myApp.show()
    splash.finish(myApp)

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
