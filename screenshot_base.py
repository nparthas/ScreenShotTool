from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QFileDialog)

import os


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
            result = self.originalPixmap.save(fileName, self.format)

            if result is False:
                raise Exception("Save Screen Shot As failed to save")

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

            if self.saveCounter == 0:
                self.savePath = self.savePath.replace(".png", "(1).png")

            while os.path.exists(self.savePath):
                self.savePath = self.savePath.replace(str(self.saveCounter), str(self.saveCounter + 1))
                self.saveCounter += 1

            result = self.originalPixmap.save(self.savePath, self.format)
            if result is False:
                raise Exception("Save Screenshot failed to save")

            self.saveCounter += 1

    def shootScreen(self):

        # Garbage collect any existing image first.
        self.originalPixmap = None

        self.originalPixmap = QApplication.primaryScreen().grabWindow(0, self.info_class.x, self.info_class.y,
                                                                      self.info_class.width.value(),
                                                                      self.info_class.height.value())

        self.updateScreenshotLabel()

        self.new_screenshot_button.setDisabled(False)
