import requests

class ApiInterface():
    def __init__(self):
        # requests session
        self.s = requests.Session()

        self.boardsURL = 'https://a.4cdn.org/boards.json'
        self.boardInfo = {}

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


a = ApiInterface()
a.getBoardList()
