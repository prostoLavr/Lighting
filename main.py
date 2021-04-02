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
    def send(text):
        print('port send:', text)


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # self.setGeometry() потом можно использовать его
        self.setFixedSize(WIDTH, HEIGHT)
        l1 = LightButton(self, 20)
        l2 = LightButton(self, 70 + SUN_SIZE)
        self.show()

    def button_click(self):
        print('click', self)


class LightButton:
    def __init__(self, *args, **kwargs):
        self.label = None
        self.is_on = False
        self.pixmap_on = QPixmap('sun_on.png')
        self.pixmap_off = QPixmap('sun_off.png')

        self.draw_me(*args, **kwargs)

    def clicked_button(self):
        print(self)

    def draw_me(self, my_parent, x_coord):
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
        self.label.setPixmap(self.pixmap_on if self.is_on else self.pixmap_off)
        print(f'I ({self}) is {"on" if self.is_on else "off"}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    master = Gui()
    sys.exit(app.exec())
