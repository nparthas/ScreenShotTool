from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from click_capture_window import ClickCaptureWindow
from info_class import *
from main_window_base import MainWindowBase
from screenshot_base import ScreenShotBase


class ScreenshotMainWindow(MainWindowBase, ScreenShotBase):
    def __init__(self, info_class, click_capture_window):
        MainWindowBase.__init__(self)
        ScreenShotBase.__init__(self)

        self.info_class = info_class

        self.createOptionsGroupBox()
        self.createButtonsLayout()

        self.main_layout.addWidget(self.options_group_box)
        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

        self.shootScreen()

        self.resize(400, 250)
        self.setWindowTitle("Mushroom Snapshot Tool")

        self.setWindowIcon(QtGui.QIcon('resources/icon.png'))

        self.click_capture_window = click_capture_window

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

    def createOptionsGroupBox(self):

        self.options_group_box = QtWidgets.QGroupBox("Options")

        self.width_label = QtWidgets.QLabel("Width:")

        self.height_label = QtWidgets.QLabel("Height")

        self.slide_speed = QtWidgets.QSpinBox()
        self.slide_speed.setSuffix(" pixels")
        self.slide_speed.setMaximum(100)
        self.slide_speed.setValue(2)

        self.slide_speed_label = QtWidgets.QLabel("Slide Speed")

        self.rectangle_width_label = QtWidgets.QLabel("Click Capture Rectangle Width")

        options_group_box_layout = QtWidgets.QGridLayout()

        options_group_box_layout.addWidget(self.width_label, 0, 0)
        options_group_box_layout.addWidget(self.info_class.width, 0, 1)  # change to auto-update

        options_group_box_layout.addWidget(self.height_label, 1, 0)
        options_group_box_layout.addWidget(self.info_class.height, 1, 1)

        options_group_box_layout.addWidget(self.slide_speed_label, 2, 0)
        options_group_box_layout.addWidget(self.slide_speed, 2, 1)

        options_group_box_layout.addWidget(self.rectangle_width_label, 3, 0)
        options_group_box_layout.addWidget(self.info_class.rectangle_width, 3, 1)

        self.options_group_box.setLayout(options_group_box_layout)

    def createButtonsLayout(self):

        self.new_screenshot_button = self.createButton("New Screenshot",
                                                       self.newScreenshot)

        self.save_screenshot_as_button = self.createButton("Save Screenshot As",
                                                           self.saveScreenshotAs)

        self.save_screenshot_button = self.createButton("Save Screenshot",
                                                        self.saveScreenshot)

        self.quit_screenshot_button = self.createButton("Quit", self.close)

        self.buttons_layout = QtWidgets.QHBoxLayout()

        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.new_screenshot_button)
        self.buttons_layout.addWidget(self.save_screenshot_as_button)
        self.buttons_layout.addWidget(self.save_screenshot_button)
        self.buttons_layout.addWidget(self.quit_screenshot_button)

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def closeEvent(self, q_close_event):
        self.close()
        self.click_capture_window.close()

    def showEvent(self, q_show_event):
        self.show()
        self.click_capture_window.show()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # print(QtWidgets.QStyleFactory.keys())  # For checking the list of available styles
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))

    info_class = InfoClass()
    click_capture = ClickCaptureWindow(info_class)
    screenshot = ScreenshotMainWindow(info_class=info_class, click_capture_window=click_capture)

    screenshot.show()
    sys.exit(app.exec_())
