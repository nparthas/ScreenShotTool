from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyQt4 import QtCore, QtGui

import time
import webbrowser

# txt = open('config.txt')
# lines = txt.readlines()


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
        # self.delaySpinBox.setValue(int(lines[1]))

        self.setWindowTitle("Screeney Screenshot Utility")
        self.resize(300, 200)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

    def resizeEvent(self, event):
        scaledSize = self.originalPixmap.size()
        scaledSize.scale(self.screenshotLabel.size(), QtCore.Qt.KeepAspectRatio)
        if not self.screenshotLabel.pixmap() or scaledSize != self.screenshotLabel.pixmap().size():
            self.updateScreenshotLabel()

    def aboutButton(self):
        webbrowser.open('http://starlightgraphics.tuxfamily.org/product/screeney/')

    def newScreenshot(self):
        if self.hideThisWindowCheckBox.isChecked():
            self.hide()
        self.newScreenshotButton.setDisabled(True)

        QtCore.QTimer.singleShot(self.delaySpinBox.value() * 1000,
                                 self.shootScreen)

    def saveScreenshot(self):
        format = 'png'
        initialPath = QtCore.QDir.currentPath() + "/untitled." + format

        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save As",
                                                     initialPath,
                                                     "%s Files (*.%s);;All Files (*)" % (format.upper(), format))
        if fileName:
            self.originalPixmap.save(fileName, format)

    def shootScreen(self):
        if self.delaySpinBox.value() != 0:
            QtGui.qApp.beep()

        # Garbage collect any existing image first.
        self.originalPixmap = None
        self.originalPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
        self.updateScreenshotLabel()

        self.newScreenshotButton.setDisabled(False)
        if self.hideThisWindowCheckBox.isChecked():
            self.show()

    def updateCheckBox(self):
        if self.delaySpinBox.value() == 0:
            self.hideThisWindowCheckBox.setDisabled(True)
        else:
            self.hideThisWindowCheckBox.setDisabled(False)

    def createOptionsGroupBox(self):
        self.optionsGroupBox = QtGui.QGroupBox("Options")

        self.delaySpinBox = QtGui.QSpinBox()
        self.delaySpinBox.setSuffix(" s")
        self.delaySpinBox.setMaximum(60)
        self.delaySpinBox.valueChanged.connect(self.updateCheckBox)

        self.delaySpinBoxLabel = QtGui.QLabel("Screenshot Delay:")

        self.hideThisWindowCheckBox = QtGui.QCheckBox("Hide This Window")

        optionsGroupBoxLayout = QtGui.QGridLayout()
        optionsGroupBoxLayout.addWidget(self.delaySpinBoxLabel, 0, 0)
        optionsGroupBoxLayout.addWidget(self.delaySpinBox, 0, 1)
        optionsGroupBoxLayout.addWidget(self.hideThisWindowCheckBox, 1, 0, 1, 2)
        self.optionsGroupBox.setLayout(optionsGroupBoxLayout)

    def createButtonsLayout(self):
        self.aboutButton = self.createButton("About",
                                             self.aboutButton)

        self.newScreenshotButton = self.createButton("New Screenshot",
                                                     self.newScreenshot)

        self.saveScreenshotButton = self.createButton("Save Screenshot",
                                                      self.saveScreenshot)

        self.quitScreenshotButton = self.createButton("Quit", self.close)

        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.aboutButton)
        self.buttonsLayout.addWidget(self.newScreenshotButton)
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
    # Create and display the splash screen
    splash_pix = QPixmap('splash.png')

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    # adding progress bar
    progressBar = QProgressBar(splash)
    progressBar.resize(800, 25)
    progressBar.move(0, 475)

    splash.setMask(splash_pix.mask())

    splash.show()
    for i in range(0, 100):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.01:
            app.processEvents()

    # Simulate something that takes time
    time.sleep(1)

    screenshot = Screenshot()
    screenshot.show()
    splash.finish(screenshot)
    sys.exit(app.exec_())
