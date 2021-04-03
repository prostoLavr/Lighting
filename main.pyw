import serial
# from serial.tools import list_ports # Может быть нужен для проверки доступности портов
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QPixmap


WIDTH = 490
HEIGHT = 350
SUN_SIZE = 200
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 70


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
            pass

    def send(self, pin, text):
        if self.port is not None and self.port.is_open:
            print('port send:', int(pin) * 3 + int(text))
            self.port.write(str(int(pin) * 3 + int(text)).encode())

    def get_port(self, pin):
        if self.port is not None and self.port.is_open:
            self.send(pin, 2)
            res = self.port.read()
            print('port return:', res, 'for pin:', pin)
            return int(res)


class Gui(QWidget):
    def __init__(self, serial_obj):
        super().__init__()
        self.init_ui(serial_obj)

    def init_ui(self, serial_obj):
        # self.setGeometry() потом можно использовать его
        self.setFixedSize(WIDTH, HEIGHT)
        LightButton(0, serial_obj, 20, self)
        LightButton(1, serial_obj, 70 + SUN_SIZE, self)
        self.show()


class LightButton:
    def __init__(self, pin, serial_obj, *args, **kwargs):
        self.pin = pin
        self.serial = serial_obj
        self.label = None
        self.button = None
        self.is_on = False
        self.pixmap_on = QPixmap('sun_on.png')
        self.pixmap_off = QPixmap('sun_off.png')

        self.draw_me(*args, **kwargs)
        self.set_as_com()

    def set_as_com(self):
        if self.serial.get_port(self.pin):
            self.set_on()
        else:
            self.set_off()

    def draw_me(self, x_coord, my_parent):
        y_coefficient = 50
        self.label = QLabel(my_parent)
        self.label.setPixmap(self.pixmap_off)
        self.label.move(x_coord, y_coefficient)

        self.button = QPushButton('OFF', my_parent)
        self.button.setFixedWidth(BUTTON_WIDTH)
        self.button.setFixedHeight(BUTTON_HEIGHT)
        self.button.move((SUN_SIZE - BUTTON_WIDTH) // 2 + x_coord, y_coefficient + SUN_SIZE + 30)
        self.button.clicked.connect(self)

    def __call__(self):
        self.is_on = not self.is_on
        self.serial.send(self.pin, self.is_on)
        if self.is_on:
            self.set_on()
        else:
            self.set_off()

    def set_on(self):
        self.is_on = True
        self.label.setPixmap(self.pixmap_on)
        self.button.setText('ON')

    def set_off(self):
        self.is_on = False
        self.label.setPixmap(self.pixmap_off)
        self.button.setText('OFF')


if __name__ == '__main__':
    my_serial = MySerial('/dev/ttyUSB0')
    app = QApplication(sys.argv)
    master = Gui(my_serial)
    sys.exit(app.exec())
