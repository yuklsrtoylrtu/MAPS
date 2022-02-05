import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.sizex = 0.05
        self.sizey = 0.05
        self.corx = 37.622092
        self.cory = 55.7536308
        self.map_request = ''
        self.response = None
        self.getImage()
        self.initUI()


    def getImage(self):
        lon = str(self.sizex)
        lat = str(self.sizey)
        delta = str(self.corx)
        delta2 = str(self.cory)
        self.map_request = "http://static-maps.yandex.ru/1.x/?ll=" + delta + "," + delta2 + "&spn=" + lon + "," + lat +\
                           "&l=map"
        self.response = requests.get(self.map_request)

        if not self.response:
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)
            file.close()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(QPixmap(self.map_file))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.sizex < 0.1:
                self.sizex += 0.01
                self.sizey += 0.01
        if event.key() == Qt.Key_PageDown:
            if self.sizex > 0.02:
                self.sizex -= 0.01
                self.sizey -= 0.01
        if event.key() == Qt.Key_Right:
            if self.corx < 50:
                self.corx += 0.01
        if event.key() == Qt.Key_Left:
            if self.corx > 20.0:
                self.corx -= 0.01
        if event.key() == Qt.Key_Up:
            if self.cory < 70:
                self.cory += 0.01
        if event.key() == Qt.Key_Down:
            if self.cory > 40:
                self.cory -= 0.01
        self.getImage()
        self.image.setPixmap(QPixmap(self.map_file))


    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())