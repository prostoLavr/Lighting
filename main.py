# import serial
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QPixmap


WIDTH = 490
HEIGHT = 400
SUN_SIZE = 200
BUTTON_SIZE = 80


class MySerial:
    def __init__(self, port_name=None):
        self.port = None
        if port_name is not None:
            self.connect(port_name)

    def connect(self, port_name):
        pass

    @staticmethod
    def send(pin, text):
        print('port send:', pin, text)


class Gui(QWidget):
    def __init__(self, serial):
        super().__init__()
        self.init_ui(serial)

    def init_ui(self, serial):
        # self.setGeometry() потом можно использовать его
        self.setFixedSize(WIDTH, HEIGHT)
        LightButton(0, serial, 20, self)
        LightButton(1, serial, 70 + SUN_SIZE, self)
        self.show()


class LightButton:
    def __init__(self, pin, serial, *args, **kwargs):
        self.pin = pin
        self.serial = serial
        self.label = None
        self.is_on = False
        self.pixmap_on = QPixmap('sun_on.png')
        self.pixmap_off = QPixmap('sun_off.png')

        self.draw_me(*args, **kwargs)

    def clicked_button(self):
        print(self)

    def draw_me(self, x_coord, my_parent):
        y_coefficient = 50
        self.label = QLabel(my_parent)
        self.label.setPixmap(self.pixmap_off)
        self.label.move(x_coord, y_coefficient)

        button = QPushButton('ON', my_parent)
        button.setFixedWidth(BUTTON_SIZE)
        button.move((SUN_SIZE - BUTTON_SIZE) // 2 + x_coord, y_coefficient + SUN_SIZE + 30)
        button.clicked.connect(self)

    def __call__(self):
        self.is_on = not self.is_on
        self.serial.send(self.pin, self.is_on)
        self.label.setPixmap(self.pixmap_on if self.is_on else self.pixmap_off)


if __name__ == '__main__':
    my_serial = MySerial()
    app = QApplication(sys.argv)
    master = Gui(my_serial)
    sys.exit(app.exec())
