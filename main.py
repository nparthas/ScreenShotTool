from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyQt4 import QtCore, QtGui

import time


class Screenshot(QtGui.QWidget):
    def __init__(self):
        super(Screenshot, self).__init__()

        self.screenshotLabel = QtGui.QLabel()
        self.screenshotLabel.setSizePolicy(QtGui.QSizePolicy.Expanding,
                                           QtGui.QSizePolicy.Expanding)
        self.screenshotLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.screenshotLabel.setMinimumSize(240, 160)

        self.createOptionsGroupBox()
        self.createButtonsLayout()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.screenshotLabel)
        mainLayout.addWidget(self.optionsGroupBox)
        mainLayout.addLayout(self.buttonsLayout)
        self.setLayout(mainLayout)

        self.shootScreen()

        self.setWindowTitle("Mushroom Snapshot Tool")
        self.resize(300, 200)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.format = 'png'
        self.setSaveLocation = False
        self.savePath = ""
        self.saveCounter = 0

    def resizeEvent(self, event):
        scaledSize = self.originalPixmap.size()
        scaledSize.scale(self.screenshotLabel.size(), QtCore.Qt.KeepAspectRatio)
        if not self.screenshotLabel.pixmap() or scaledSize != self.screenshotLabel.pixmap().size():
            self.updateScreenshotLabel()

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:

            if event.key() == 87:
                self.y -= self.slideSpeed.value()
            elif event.key() == 65:
                self.x -= self.slideSpeed.value()
            elif event.key() == 83:
                self.y += self.slideSpeed.value()
            elif event.key() == 68:
                self.x += self.slideSpeed.value()
            self.newScreenshot()

            event.accept()
        else:
            event.ignore()

    def newScreenshot(self):

        QtCore.QTimer.singleShot(0, self.shootScreen)

    def saveScreenshotAs(self):

        initialPath = QtCore.QDir.currentPath() + "/untitled." + self.format

        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save As",
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

        self.originalPixmap = QtGui.QPixmap.grabWindow(QApplication.desktop().winId(), self.x, self.y,
                                                       self.width.value(),
                                                       self.height.value())

        self.updateScreenshotLabel()

        self.newScreenshotButton.setDisabled(False)

    def createOptionsGroupBox(self):

        self.x = 100
        self.y = 100

        self.optionsGroupBox = QtGui.QGroupBox("Options")

        self.width = QtGui.QSpinBox()
        self.width.setSuffix(" pixels")
        self.width.setMaximum(10000)
        self.width.setValue(100)

        self.widthLabel = QtGui.QLabel("Width:")

        self.height = QtGui.QSpinBox()
        self.height.setSuffix(" pixels")
        self.height.setMaximum(10000)
        self.height.setValue(100)

        self.heightLabel = QtGui.QLabel("Height")

        self.slideSpeed = QtGui.QSpinBox()
        self.slideSpeed.setSuffix(" pixels")
        self.slideSpeed.setMaximum(100)
        self.slideSpeed.setValue(2)

        self.slideSpeedLabel = QtGui.QLabel("Slide Speed")

        optionsGroupBoxLayout = QtGui.QGridLayout()

        optionsGroupBoxLayout.addWidget(self.widthLabel, 0, 0)
        optionsGroupBoxLayout.addWidget(self.width, 0, 1)  # change to auto update

        optionsGroupBoxLayout.addWidget(self.heightLabel, 1, 0)
        optionsGroupBoxLayout.addWidget(self.height, 1, 1)

        optionsGroupBoxLayout.addWidget(self.slideSpeedLabel, 2, 0)
        optionsGroupBoxLayout.addWidget(self.slideSpeed, 2, 1)

        self.optionsGroupBox.setLayout(optionsGroupBoxLayout)

    def createButtonsLayout(self):

        self.newScreenshotButton = self.createButton("New Screenshot",
                                                     self.newScreenshot)

        self.saveScreenshotAsButton = self.createButton("Save Screenshot As",
                                                        self.saveScreenshotAs)

        self.saveScreenshotButton = self.createButton("Save Screenshot",
                                                      self.saveScreenshot)

        self.quitScreenshotButton = self.createButton("Quit", self.close)

        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.newScreenshotButton)
        self.buttonsLayout.addWidget(self.saveScreenshotAsButton)
        self.buttonsLayout.addWidget(self.saveScreenshotButton)
        self.buttonsLayout.addWidget(self.quitScreenshotButton)

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def updateScreenshotLabel(self):
        self.screenshotLabel.setPixmap(self.originalPixmap.scaled(
            self.screenshotLabel.size(), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation))


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    for i in range(0, 100):
        t = time.time()
        while time.time() < t + 0.01:
            app.processEvents()

    screenshot = Screenshot()
    screenshot.show()
    sys.exit(app.exec_())
