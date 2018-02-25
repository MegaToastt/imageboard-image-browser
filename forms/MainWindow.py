from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self, api):
        super(MainWindow, self).__init__()
        self.api = api
        self.initUI()

    def initUI(self):
        self.initMenuBar()
        self.initToolBar()

        self.move(300, 200)
        self.setWindowTitle('Window title here')
        self.show()

    def initMenuBar(self):
        # Enable status bar
        self.statusBar()

        # Exit button
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        # Init file menu and add buttons to it
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

    def initToolBar(self):
        # Init toolbar itself
        self.toolbar = self.addToolBar('Main')
        self.toolbar.setMovable(False)

        # Create combo box to select board
        boardLabel = QLabel("Board:")
        boardComboBox = QComboBox(self)
        boardComboBox.setMaxVisibleItems(20)
        # Get board list and populate the combobox
        boardList = self.api.getBoardList()
        for board in boardList:
            boardComboBox.addItem(board['board'])


        # Add widgets, etc to the toolbar
        self.toolbar.addWidget(boardLabel)
        self.toolbar.addWidget(boardComboBox)
