from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Extension of QWidget with a resized signal for ease of use
class ImageWidget(QWidget):
    
    resized = pyqtSignal()

    def __init__(self):
        super(ImageWidget, self).__init__()
    
    def resizeEvent(self, event):
        self.resized.emit()
        return super(ImageWidget, self).resizeEvent(event)
