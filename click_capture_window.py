from PyQt5 import QtGui, QtWidgets

from info_class import InfoClass


class ClickCaptureWindow(QtWidgets.QWidget):
    def __init__(self, info_class):
        super().__init__()
        self.info_class = info_class

        self.resize(400, 400)
        self.setWindowTitle(" ")

        # can change later to make borderless and be able to move around
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(0.3)

        self.setMouseTracking(True)

        self.local_width = self.info_class.width.value()
        self.local_height = self.info_class.height.value()

        self.change_width = False
        self.change_height = False

        self.pixmap = None
        self.update_cursor()

        self.setWindowIcon(QtGui.QIcon('icon.png'))

    def mouseMoveEvent(self, event):

        if event == QtGui.QMouseEvent:

            if self.local_width != self.info_class.width.value():
                self.change_width = True

            if self.local_height != self.info_class.height.value():
                self.change_height = True

            if self.change_width or self.change_height:
                self.update_cursor()
                self.change_width = False
                self.change_height = False

            event.accpet()
        else:
            event.ignore()

    def mousePressEvent(self, QMouseEvent):
        print("pressed")

    def update_cursor(self):

        # self.local_height = self.info_class.height.value()
        # self.local_width = self.info_class.width.value()
        #
        # self.pixmap = QtGui.QPixmap()
        # self.pixmap.height = self.local_height
        # self.pixmap.width = self.local_width
        #
        # self.pixmap.createMaskFromColor()
        # self.pixmap.colo
        pass

        # self.pixmap = QPixmap("test.jpg")
        # QtGui.QPixmap("test.jpg")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    info_class = InfoClass()
    click_capture = ClickCaptureWindow(info_class)

    click_capture.show()

    sys.exit(app.exec_())
