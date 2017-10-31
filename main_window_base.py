from PyQt5 import QtCore, QtGui

from info_class import *


class MainWindowBase(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.screenshot_label = QtWidgets.QLabel()
        self.screenshot_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Expanding)
        self.screenshot_label.setAlignment(QtCore.Qt.AlignCenter)
        self.screenshot_label.setMinimumSize(240, 160)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.screenshot_label)

    def resizeEvent(self, event):

        scaled_size = self.originalPixmap.size()
        scaled_size.scale(self.screenshot_label.size(), QtCore.Qt.KeepAspectRatio)
        if not self.screenshot_label.pixmap() or scaled_size != self.screenshot_label.pixmap().size():
            self.updateScreenshotLabel()

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:

            if event.key() == 87:
                self.info_class.y -= self.slideSpeed.value()
            elif event.key() == 65:
                self.info_class.x -= self.slideSpeed.value()
            elif event.key() == 83:
                self.info_class.y += self.slideSpeed.value()
            elif event.key() == 68:
                self.info_class.x += self.slideSpeed.value()
            self.newScreenshot()

            event.accept()
        else:
            event.ignore()

    def updateScreenshotLabel(self):
        self.screenshot_label.setPixmap(self.originalPixmap.scaled(
            self.screenshot_label.size(), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation))
