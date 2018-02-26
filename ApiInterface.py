import requests
import shutil
import os
import sys

"""
        TODO
    - Fix errors when selecting posts and changing boards
    - Get the actual image to download using requests
"""
class ApiInterface():
    def __init__(self):
        # requests session
        self.s = requests.Session()

        self.boardsURL = 'https://a.4cdn.org/boards.json'
        self.boardInfo = {}

        self.downloadPath = 'cache'
        self.downloadedFiles = []

    # return list of dictionaries with board info
    def getBoardList(self):
        if not self.boardInfo:
            boardList = []
            # request board list from board URL
            boardJSON = self.s.get(self.boardsURL).json()['boards']
            for board in boardJSON:
                boardDict = {}
                boardDict['board'] = board['board']
                boardDict['name'] = board['title']
                boardDict['desc'] = board['meta_description']
                boardList.append(boardDict)
            self.boardInfo = boardList
        return self.boardInfo
    
    def getBoardURL(self, boardName):
        return 'https://a.4cdn.org/'+ boardName +'/catalog.json'

    def getThreadList(self, boardName):
        threadList = []
        # Need to compile all the pages into one list and get required info (name and thread number, etc)
        threadJSON = self.s.get(self.getBoardURL(boardName)).json()
        for page in threadJSON:
            threads = page['threads']
            for thread in threads:
                threadDict = {}
                # Thread number
                threadDict['no'] = thread['no']
                # Thread subject (if any)
                if 'sub' in thread: 
                    threadDict['sub'] = thread['sub']
                # Thread comment
                if 'com' in thread:
                    threadDict['com'] = thread['com']

                threadList.append(threadDict)
        return threadList

    def getThreadURL(self, boardName, threadNo):
        return 'https://a.4cdn.org/'+ boardName +'/thread/'+ str(threadNo) +'.json'

    def getThread(self, boardName, threadNo):
        postList = []
        postsJSON = self.s.get(self.getThreadURL(boardName, threadNo)).json()['posts']

        for post in postsJSON:
            # Skip if no image
            if 'ext' not in post:
                continue
            
            postDict = {}
            postDict['no'] = post['no']
            postDict['filename'] = post['filename']
            postDict['ext'] = post['ext']
            postDict['imageURL'] = 'https://i.4cdn.org/'+ boardName +'/'+ str(post['tim']) + post['ext']

            postList.append(postDict)
        return postList

    def downloadImage(self, URL, filename):
        if(filename in self.downloadedFiles):
            return self.downloadPath + '/' + filename
        r = self.s.get(URL)
        path = self.downloadPath + '/' + filename
        open(path, 'wb').write(r.content)
        self.downloadedFiles.append(filename)
        return path
        



a = ApiInterface()
a.getBoardList()
