from PyQt5 import QtWidgets


class InfoClass(object):
    def __init__(self):
        self.x = 100
        self.y = 100

        self.width = QtWidgets.QSpinBox()
        self.width.setSuffix(" Pixels")
        self.width.setMaximum(10000)
        self.width.setValue(100)

        self.height = QtWidgets.QSpinBox()
        self.height.setSuffix(" pixels")
        self.height.setMaximum(10000)
        self.height.setValue(100)

        self.rectangle_width = QtWidgets.QSpinBox()
        self.rectangle_width.setMaximum(20)
        self.rectangle_width.setValue(5)
