import sys
import os
import shutil
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from forms.MainWindow import MainWindow
from ApiInterface import ApiInterface

class App:
    def __init__(self):
        self.api = ApiInterface()

    def run(self):
        self.initCacheFolder()
        app = QApplication(sys.argv)
        w = MainWindow(self.api)
        sys.exit(app.exec_())

    def initCacheFolder(self):
        # delete the existing cache if existing, then make a new empty one
        if os.path.exists('cache'):
            shutil.rmtree('cache')
        os.mkdir('cache')

if __name__ == '__main__':
    app = App()
    app.run()
