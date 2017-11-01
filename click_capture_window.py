from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QColor, QCursor

from info_class import InfoClass


class ClickCaptureWindow(QtWidgets.QWidget):
    def __init__(self, info_class):
        super().__init__()
        self.info_class = info_class

        self.resize(400, 400)
        self.setWindowTitle(" ")

        self.setWindowOpacity(0.3)

        self.setMouseTracking(True)

        self.local_width = self.info_class.width.value()
        self.local_height = self.info_class.height.value()

        self.update = False

        self.pixmap = None

        self.local_rectangle_width = 5

        self.updateCursor()

        self.setWindowIcon(QtGui.QIcon('resources/icon.png'))

    def mouseMoveEvent(self, event):

        if self.local_width != self.info_class.width.value():
            self.update = True

        if self.local_height != self.info_class.height.value():
            self.update = True

        if self.local_rectangle_width != self.info_class.rectangle_width.value():
            self.update = True

        if self.update:
            self.updateCursor()
            self.update = False

            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        print("pressed")

    def updateCursor(self):

        self.local_height = self.info_class.height.value()
        self.local_width = self.info_class.width.value()
        self.local_rectangle_width = self.info_class.rectangle_width.value()

        self.pixmap = QPixmap(self.local_width, self.local_height)
        self.pixmap.fill(QColor(0, 0, 0, 0))

        painter_instance = QtGui.QPainter(self.pixmap)

        pen_rectangle = QtGui.QPen(QtCore.Qt.darkBlue)  # can change color of the rectangle here
        pen_rectangle.setWidth(self.local_rectangle_width)

        painter_instance.setPen(pen_rectangle)
        painter_instance.drawRect(0, 0, self.local_width, self.local_height)

        self.setCursor(QCursor(self.pixmap))


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    info_class = InfoClass()
    click_capture = ClickCaptureWindow(info_class)

    click_capture.show()

    sys.exit(app.exec_())
