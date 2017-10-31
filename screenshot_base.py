from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QFileDialog)


class ScreenShotBase(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.format = 'png'
        self.setSaveLocation = False
        self.savePath = ""
        self.saveCounter = 0

    def newScreenshot(self):

        QtCore.QTimer.singleShot(0, self.shootScreen)

    def saveScreenshotAs(self):
        initialPath = QtCore.QDir.currentPath() + "/untitled." + self.format

        fileName, _ = QFileDialog.getSaveFileName(self, "Save As",
                                                  initialPath,
                                                  "%s Files (*.%s);;All Files (*)" % (
                                                      self.format.upper(), self.format))

        if fileName:
            self.originalPixmap.save(fileName, self.format)
            self.setSaveLocation = True
            self.savePath = fileName

    def saveScreenshot(self):
        if not self.setSaveLocation:
            self.saveScreenshotAs()
        else:
            try:
                lastNum = int(self.savePath.split("(")[-1].replace(').png', ""))

            except ValueError:
                lastNum = 0

            if lastNum != self.saveCounter:
                self.saveCounter = lastNum

            self.saveCounter += 1

            if self.saveCounter == 1:
                self.savePath = self.savePath.replace(".png", "(1).png")
                self.originalPixmap.save(self.savePath, self.format)

            else:
                self.savePath = self.savePath.replace(str(self.saveCounter - 1), str(self.saveCounter))
                self.originalPixmap.save(self.savePath, self.format)

    def shootScreen(self):

        # Garbage collect any existing image first.
        self.originalPixmap = None

        self.originalPixmap = QApplication.primaryScreen().grabWindow(0, self.info_class.x, self.info_class.y,
                                                                      self.info_class.width.value(),
                                                                      self.info_class.height.value())

        self.updateScreenshotLabel()

        self.newScreenshotButton.setDisabled(False)