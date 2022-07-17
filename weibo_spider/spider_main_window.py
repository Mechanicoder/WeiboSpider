from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QTime, QDateTime

import sys
import random

class SpiderMainWindow():
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load("spider_main_window.ui")
        self.ui.show()

        self.ui.pushButton_start.clicked.connect(self.on_start)

    @QtCore.Slot()
    def on_start(self):
        self.ui.textEdit_log.append("start")
        self.ui.label_showStart.setText(QDateTime.currentDateTime().toString())

    @QtCore.Slot()
    def on_test(self):
        self.ui.label.setText("test")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    mainWnd = SpiderMainWindow()

    sys.exit(app.exec())