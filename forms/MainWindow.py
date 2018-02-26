from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pprint
from .ImageWidget import ImageWidget

'''
TODO:
    1. Change image section to be QScrollArea - see https://doc.qt.io/qt-5/qtwidgets-widgets-imageviewer-example.html
    2. Make image viewing experience better
'''

class MainWindow(QMainWindow):
    def __init__(self, api):
        super(MainWindow, self).__init__()
        self.api = api
        self.initUI()
        
        self.currentBoard = None
        self.currentThread = None
        self.currentImageURL = None

    def initUI(self):
        self.initMenuBar()
        self.initToolBar()
        self.initCentralWidget()
        self.initDock()

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
        self.boardComboBox = QComboBox(self)
        self.boardComboBox.setMaxVisibleItems(20)
        # Get board list and populate the combobox
        boardList = self.api.getBoardList()
        for board in boardList:
            self.boardComboBox.addItem(board['board'])
        # Add "go" button to load the board
        boardLoadBtn = QPushButton("Go", self)
        boardLoadBtn.clicked.connect(self.on_boardLoad)
        boardLoadBtn.setMaximumSize(40,40)


        # Add widgets, etc to the toolbar
        self.toolbar.addWidget(boardLabel)
        self.toolbar.addWidget(self.boardComboBox)
        self.toolbar.addWidget(boardLoadBtn)

    def initCentralWidget(self):
        self.centralWidget = ImageWidget()
        layout = QVBoxLayout()

        self.mainImage = QLabel("Image")
        self.mainImagePixmap = QPixmap(1000, 1000)
        self.mainImagePixmap.fill()
        self.mainImage.resize(self.mainImagePixmap.size())
        self.centralWidget.resize(self.mainImagePixmap.size())
        #self.mainImage.setScaledContents(True)
        self.mainImage.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        layout.addWidget(self.mainImage)
        self.centralWidget.setLayout(layout)
        self.centralWidget.resized.connect(self.updateMainImageSize)
        self.setCentralWidget(self.centralWidget)



    def initDock(self):
        ## variable initialization ##
        self.threadPosts = {}
        #####
        sideDock = QDockWidget("Threads", self)
        sideDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        # Removes titlebar on the dock
        sideDock.setTitleBarWidget(QWidget())

        # Parent widget so it is possible to add 2 widgets inside the dock
        dockWidget = QWidget()
        layout = QHBoxLayout()

        self.threadList = QListWidget(sideDock)
        self.threadList.addItems(("Test1", "Test2", "Test3", "Test4"))
        #self.threadList.setSizeAdjustPolicy(QListWidget.AdjustToContents)

        self.imageList = QListWidget(sideDock)
        self.imageList.addItems(("TestImage1", "TestImage2", "TestImage3"))

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(self.threadList)
        splitter.addWidget(self.imageList)

        layout.addWidget(splitter)
        #layout.addWidget(self.threadList)
        #layout.addWidget(self.imageList)
        dockWidget.setLayout(layout)

        sideDock.setWidget(dockWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, sideDock)
        #self.threadList.currentRowChanged.connect(self.on_threadSelect)
        #self.imageList.currentRowChanged.connect(self.on_postSelect)
        self.threadList.itemClicked.connect(self.on_threadSelect)
        self.imageList.itemClicked.connect(self.on_postSelect)

    def updateCurrentSelected(self, boardName=None, threadNo=None, imageURL=None):
        self.currentBoard = boardName
        self.currentThread = threadNo
        self.currentImageURL = imageURL

    def updateThreadList(self, boardName):
        self.threads = self.api.getThreadList(boardName)
        self.threadList.clear()

        for thread in self.threads:
            if 'sub' in thread:
                self.threadList.addItem(thread['sub'][:30])
            elif 'com' in thread:
                self.threadList.addItem(thread['com'][:30])
            else:
                self.threadList.addItem(' ')

    def updatePostList(self, boardName, threadNo):
        self.imageList.clear()
        if (boardName, threadNo) not in self.threadPosts:
            self.threadPosts[(boardName, threadNo)] = self.api.getThread(boardName, threadNo)
        for post in self.threadPosts[(boardName, threadNo)]:
            self.imageList.addItem(post['filename'])
            
    def updateMainImage(self):
        filename = self.threadPosts[(self.currentBoard, self.currentThread)][self.imageList.currentRow()]['filename']
        extension = self.threadPosts[(self.currentBoard, self.currentThread)][self.imageList.currentRow()]['ext']
        path = self.api.downloadImage(self.currentImageURL, filename + extension)
        self.mainImagePixmap = QPixmap(path)
        #self.mainImage.setPixmap(self.mainImagePixmap)
        self.updateMainImageSize()

    def updateMainImageSize(self):
        w = self.mainImage.width()
        h = self.mainImage.height()

        self.mainImage.setPixmap(self.mainImagePixmap.scaled(w,h,Qt.KeepAspectRatio))
        
    def on_threadSelect(self):
        current = self.threadList.currentRow()
        self.updateCurrentSelected(boardName=self.currentBoard, threadNo=self.threads[current]['no'])
        try:
            self.updatePostList(self.currentBoard, self.currentThread)
        except AttributeError:
            print('att err?')

    def on_postSelect(self):
        self.imageList.clearSelection()

        postIndex = self.imageList.currentRow()
        imageURL = self.threadPosts[(self.currentBoard, self.currentThread)][postIndex]['imageURL']
        self.updateCurrentSelected(boardName=self.currentBoard, threadNo=self.currentThread, imageURL=imageURL)
        self.updateMainImage()
        self.imageList.setCurrentRow(postIndex)

    # Event when the "go" button is clicked when selecting a board
    def on_boardLoad(self):
        boardName = self.boardComboBox.currentText()
        self.updateCurrentSelected(boardName=boardName)
        self.updateThreadList(self.currentBoard)
