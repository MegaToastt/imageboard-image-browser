import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from forms.MainWindow import MainWindow
from ApiInterface import ApiInterface

class App:
    def __init__(self):
        self.api = ApiInterface()

    def run(self):
        app = QApplication(sys.argv)
        w = MainWindow(self.api)
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = App()
    app.run()
