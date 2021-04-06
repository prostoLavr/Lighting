#!/usr/bin/env python
import sys

from PIL import Image
import serial
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon


DEBUG = False
LAMP_SIZE = 200
BUTTON_WIDTH = 70
BUTTON_HEIGHT = 90
COUNT = 2
WIDTH = 20 + (LAMP_SIZE + 50) * COUNT - 30
HEIGHT = 550
SHIT_SIZE = 130


class ResizeImg:
    def __init__(self, filename, w=None, h=None):
        self.filename = filename
        img = Image.open(filename)
        if w is not None and h is None:
            ratio = (w / float(img.size[0]))
            height = int((float(img.size[1]) * float(ratio)))
            img = img.resize((w, height), Image.AFFINE)
        elif w is None and h is not None:
            ratio = (h / float(img.size[1]))
            width = int((float(img.size[0]) * float(ratio)))
            img = img.resize((h, width), Image.AFFINE)
        img.save('resize_' + filename)

    def get_filename(self):
        return 'resize_' + self.filename


class MySerial:
    def __init__(self, port_name=None):
        self.port_name = port_name
        self.port = None
        if port_name is not None:
            self.connect(port_name)

    def connect(self, port_name):
        try:
            self.port = serial.Serial(port_name, 9600)
        except serial.SerialException:
            self.port = None

    def send(self, pin, text):
        self.connect(self.port_name)
        if self.port is not None and self.port.is_open:
            if DEBUG:
                print('port send:', int(pin) * 3 + int(text))
            self.port.write(str(int(pin) * 3 + int(text)).encode())
            return True
        return False

    def get_port(self, pin):
        if self.port is not None and self.port.is_open:
            self.send(pin, 2)
            res = self.port.read()
            if DEBUG:
                print('port return:', res, 'for pin:', pin)
            return int(res)


class Gui(QWidget):
    def __init__(self, serial_obj):
        super().__init__()
        self.init_ui(serial_obj)

    def init_ui(self, serial_obj):
        self.setFixedSize(WIDTH, HEIGHT)
        for i in range(COUNT):
            LightButton(i, serial_obj, 20 + 50 * i + LAMP_SIZE * i, self)
        btn = QPushButton( QIcon(ResizeImg('Icons/shit.png', SHIT_SIZE).get_filename()), '', self )
        btn.setFixedSize(130, 130)
        btn.setIconSize(QSize(130, 130))
        btn.clicked.connect(self.port_sottengs)
        btn.move(30, LAMP_SIZE + BUTTON_HEIGHT + 100)
        self.show()

    def port_sottengs(self):
        print('settings')


class LightButton:
    def __init__(self, pin, serial_obj, *args, **kwargs):
        self.pin = pin
        self.serial = serial_obj
        self.label = None
        self.button = None
        self.is_on = False

        self.draw_me(*args, **kwargs)
        self.set_as_com()

    def set_as_com(self):
        if self.serial.get_port(self.pin):
            self.set_on()
        else:
            self.set_off()

    def draw_me(self, x_coord, my_parent):
        self.label_pixmap_on = QPixmap(ResizeImg('Icons/lamp_on.png', LAMP_SIZE).get_filename())
        self.label_pixmap_off = QPixmap(ResizeImg('Icons/lamp_off.png', LAMP_SIZE).get_filename())
        self.label_pixmap_no_work = QPixmap(ResizeImg('Icons/lamp_no_work.png', LAMP_SIZE).get_filename())
        self.button_icon_on = QIcon(ResizeImg('Icons/r_on.png', BUTTON_WIDTH).get_filename())
        self.button_icon_off = QIcon(ResizeImg('Icons/r_off.png', BUTTON_WIDTH).get_filename())

        y_coefficient = 10
        self.label = QLabel(my_parent)
        self.label.setPixmap(self.label_pixmap_off)
        self.label.move(x_coord, y_coefficient)

        self.button = QPushButton(my_parent)

        self.button.setIcon(self.button_icon_on)
        self.button.setIconSize(QSize(BUTTON_WIDTH, BUTTON_HEIGHT))

        self.button.setFixedWidth(BUTTON_WIDTH)
        self.button.setFixedHeight(BUTTON_HEIGHT)
        self.button.setStyleSheet('')
        self.button.move((LAMP_SIZE - BUTTON_WIDTH) // 2 + x_coord, y_coefficient + LAMP_SIZE + 30)
        self.button.clicked.connect(self)

    def __call__(self):
        self.is_on = not self.is_on
        if self.serial.send(self.pin, self.is_on):
            self.set_as_com()
        else:
            self.set_no_work()

    def set_on(self):
        self.is_on = True
        self.label.setPixmap(self.label_pixmap_on)
        self.button.setIcon(self.button_icon_on)

    def set_off(self):
        self.is_on = False
        self.label.setPixmap(self.label_pixmap_off)
        self.button.setIcon(self.button_icon_off)

    def set_no_work(self):
        self.is_on = False
        self.label.setPixmap(self.label_pixmap_no_work)
        self.button.setIcon(self.button_icon_off)


if __name__ == '__main__':
    my_serial = MySerial('/dev/ttyUSB0')
    app = QApplication(sys.argv)
    master = Gui(my_serial)
    sys.exit(app.exec())
