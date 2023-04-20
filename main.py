from ast import In
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtCore import QTimer

import random
import time
from queue import PriorityQueue
import random
from PyQt5.QtCore import QPropertyAnimation, QPoint

class PushButton(QtWidgets.QPushButton):
    def __init__(self, text, style,row,column, color, parent=None):
        super(PushButton, self).__init__(text, parent)
        self.setStyleSheet(style)
        self.setText(text)
        self.setMinimumSize(QSize(35, 35))
        self.setMaximumSize(QSize(35, 35))
        self.color=color
        
def directions(direction, currrow, currcol):
    if(direction == 1):
        currrow = up(currrow)
    elif(direction == 2):
        currrow = down(currrow)
    elif(direction == 3):
        currcol = left(currcol)
    elif(direction == 4):
        currcol = right(currcol)

    return [currrow, currcol]

def up(currrow):
    currrow -= 1
    return currrow
def down(currrow):
    currrow -= 1
    return currrow
def left(currcol):
    currcol -= 1
    return currcol
def right(currcol):
    currcol -= 1
    return currcol




class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        width=1000
        height=700
        self.setFixedSize(width,height)
        self.rows = 20
        self.columns = 30
        self.Buttons = [[0 for _ in range(self.columns)] for __ in range(self.rows)] 

        self.Styles = {
            "White": """
                background-color:white;
                max-height:35px;
                max-width:35px;
                border :0.5px solid white;
                """,
            "WallGray": """
                background-color:#393a3b;
                max-height:35px;
                max-width:35px;
                border :0.5px solid gray;
                """,
            "Orange":"""
                background-color:orange;
                max-height:35px;
                max-width:35px;
                
                border :0.5px solid orange;
                """,
            "Yellow":"""
                background-color:yellow;
                max-height:35px;
                max-width:35px;
                border :0.5px solid yellow;
                """,
            "Gray":"""
                background-color:#423e40;
                max-height:35px;
                max-width:35px;
                border :0.50px solid #423e40;
                """,
            "Green":"""
                background-color:green;
                max-height:35px;
                max-width:35px;
                border :0.5px solid gray;
                """,
            "Blue":"""
                background-color:#03fc77;
                max-height:35px;
                max-width:35px;
                border :0.5px solid #03fc77;
                """,
            "Red":"""
                background-color:red;
                max-height:35px;
                max-width:35px;
                
                border :0.5px solid red;
                """,
                
            }
        
        Widget= QtWidgets.QWidget()
        self.vertical = QtWidgets.QVBoxLayout()
        self.inWidget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(self.inWidget)
        self.vertical.addWidget(self.inWidget)
        self.CreateButtons()
        
        startcell = None

        Widget.setLayout(self.vertical)
        self.setCentralWidget(Widget)
        
        # Combo Boxes
        combobox_algorithm = QtWidgets.QComboBox(self)
        combobox_algorithm.setGeometry(50, 50, 60, 60)
        combobox_algorithm.addItems(['bfs', 'dfs'])
        self.vertical.addWidget(combobox_algorithm)

        combobox_difficulty = QtWidgets.QComboBox(self)
        combobox_difficulty.setGeometry(50, 50, 60, 60)
        combobox_difficulty.addItems(['Easy', 'Standard', 'Hard'])
        self.vertical.addWidget(combobox_difficulty)

        combobox_food = QtWidgets.QComboBox(self)
        combobox_food.setGeometry(50, 50, 60, 60)
        combobox_food.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
        self.vertical.addWidget(combobox_food)
        
        # Build Button
        build_btn = QtWidgets.QPushButton("Build", clicked = lambda: self.buildMap(combobox_difficulty.currentText(), combobox_food.currentText()))
        self.vertical.addWidget(build_btn)

        # Start Button
        start_btn = QtWidgets.QPushButton("Start", clicked = lambda: self.run(combobox_food.currentText(), combobox_algorithm.currentText()))
        self.vertical.addWidget(start_btn)
    
    def CreateButtons(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if (row==0 or row==19) or(column==0 or column==29) :
                    button = PushButton('', style=self.Styles["Gray"],row=row,column=column, color="gray")
                    self.layout.addWidget(button,row + 1, column)
                else:
                    button = PushButton('', style=self.Styles["White"],row=row,column=column, color="white")
                    self.Buttons[row][column]=button
                    button.setEnabled(False)
                    self.layout.addWidget(button,row+1,column)

    def LocateWalls(self, number):
        for i in range(1, number + 1):
            wallRow = random.randint(1,18)
            wallColumn = random.randint(1, 28)
            button = PushButton('', style=self.Styles["Gray"],row=wallRow,column=wallColumn, color="gray")
            self.Buttons[wallRow][wallColumn] = button
            button.setEnabled(False)
            self.layout.addWidget(button,wallRow+1,wallColumn)

    def LocateFoods(self, number):
        for i in range(1, number + 1):
            foodRow = random.randint(1,18)
            foodColumn = random.randint(1, 28)
            button = PushButton('', style=self.Styles["Orange"],row=foodRow,column=foodColumn, color="orange")
            self.Buttons[foodRow][foodColumn] = button
            button.setEnabled(False)
            self.layout.addWidget(button,foodRow+1,foodColumn)
        
    def LocatePacMan(self):
        pacmanRow = random.randint(1,18)
        pacmanColumn = random.randint(1, 28)
        button = PushButton('', style=self.Styles["Yellow"],row=pacmanRow,column=pacmanColumn, color="yellow")
        self.Buttons[pacmanRow][pacmanColumn] = button
        button.setEnabled(False)
        self.layout.addWidget(button,pacmanRow+1,pacmanColumn)
        return [pacmanRow, pacmanColumn]

    def move(self):
        currrow = self.pacmanRow
        currcol = self.pacmanColumn

        for i in range(0 ,10):
            direction = random.randint(1, 4)
            coordinates = directions(direction, currrow, currcol)
            currrow = coordinates[0]
            currcol = coordinates[1]

            button = PushButton('', style=self.Styles["Yellow"],row=currrow,column=currcol, color="yellow")
            currentButton = self.Buttons[currrow][currcol]

            if(currentButton == 0):
                continue
            elif(currentButton.styleSheet().split()[0] == 'background-color:#423e40;'):
                continue
            else:
                self.Buttons[currrow][currcol] = button
                button.setEnabled(False)
                self.layout.addWidget(button,currrow+1,currcol)

    def dfs(self, startcell):
        startrow = startcell[0]
        startcol = startcell[1]
        foodIsFound = False
        explored = [[startrow, startcol]]
        frontier = [[startrow, startcol]]

        dfspath = {}

        while len(frontier) > 0:
            currcell = frontier.pop()
            currentButton = self.Buttons[currcell[0]][currcell[1]]
            visited = [[False]*30]*20

            yellowbutton = PushButton('', style=self.Styles["Yellow"],row=currcell[0],column=currcell[1], color="yellow")

            if currentButton == 0:
                continue
            elif currentButton.styleSheet().split()[0] == 'background-color:orange;':
                redbutton = PushButton('', style=self.Styles["Red"],row=currcell[0],column=currcell[1], color="red")
                self.Buttons[currcell[0]][currcell[1]] = redbutton
                redbutton.setEnabled(False)
                self.layout.addWidget(redbutton,currcell[0]+1,currcell[1])
                foodIsFound = True
                break
            elif currentButton.styleSheet().split()[0] == 'background-color:white;':
                self.Buttons[currcell[0]][currcell[1]] = yellowbutton
                yellowbutton.setEnabled(False)
                self.layout.addWidget(yellowbutton,currcell[0]+1,currcell[1])
                loop = QEventLoop()
                QTimer.singleShot(2, loop.quit)
                loop.exec_()

            elif currentButton.styleSheet().split()[0] == 'background-color:#423e40;':
                continue
                
            for d in 'ESNW':
                
                if d == 'E':
                    childcell = [currcell[0], currcell[1] + 1]
                elif d == 'S':
                    childcell = [currcell[0], currcell[1] - 1]
                elif d == 'N':
                    childcell = [currcell[0] + 1, currcell[1]]
                elif d == 'W':
                    childcell = [currcell[0] - 1, currcell[1]]
                if childcell in explored:
                    continue
                explored.append(childcell)
                frontier.append(childcell)
                dicChild = (childcell[0], childcell[1])
                dicCurr = (currcell[0], currcell[1])
                dfspath[dicChild] = dicCurr

        

        fwdpath = {}
        foodcell = [currcell[0], currcell[1]]
        dicFood = (foodcell[0], foodcell[1])
        startcell = [startrow, startcol]
        dicStart = (startcell[0], startcell[1])
        while(dicFood != dicStart):
            fwdpath[dfspath[dicFood]] = dicFood
            dicFood = dfspath[dicFood]

        return [fwdpath, foodcell, foodIsFound]

    def showpath(self, path):
        for step in path:
            if(step[0] != w.pacmanRow or step[1] != w.pacmanColumn):
                bluebutton = PushButton('', style=w.Styles["Blue"],row=step[0],column=step[1], color="blue")
                if(w.Buttons[step[0]][step[1]].styleSheet().split()[0] == 'background-color:yellow;'):
                    w.Buttons[step[0]][step[1]] = bluebutton
                    bluebutton.setEnabled(False)
                    w.layout.addWidget(bluebutton,step[0]+1,step[1])
                    loop = QEventLoop()
                    QTimer.singleShot(70, loop.quit)
                    loop.exec_()

        # self.timerShowPath.stop()
    def checkNode(self, node):
        currentButton = self.Buttons[node[0]][node[1]]
        if currentButton == 0:
            return 'index'
        elif currentButton.styleSheet().split()[0] == 'background-color:orange;':
            return 'food'
        elif currentButton.styleSheet().split()[0] == 'background-color:red;':
            return 'foundfood'
        elif currentButton.styleSheet().split()[0] == 'background-color:#03fc77;':
            return 'foundpath'
        elif currentButton.styleSheet().split()[0] == 'background-color:yellow;':
            return 'visitedpath'
        elif currentButton.styleSheet().split()[0] == 'background-color:#423e40;':
            return 'wall'
        elif currentButton.styleSheet().split()[0] == 'background-color:white;':
            return 'path'
        elif currentButton.styleSheet().split()[0] == 'background-color:green;':
            return 'start'

    def bfs(self, startcell):
        queue = []
        visited = {}
        bfspath = {}
        foodIsFound = False
        for i in range(0, 20):
            for j in range(0, 30):
                visited[(i, j)] = False
        queue.append(startcell)
        while len(queue) > 0:
            node = queue.pop(0)
            currentButton = self.Buttons[node[0]][node[1]]

            if currentButton == 0:
                continue
            elif currentButton.styleSheet().split()[0] == 'background-color:orange;':
                redbutton = PushButton('', style=self.Styles["Red"],row=node[0],column=node[1], color="red")
                self.Buttons[node[0]][node[1]] = redbutton
                redbutton.setEnabled(False)
                self.layout.addWidget(redbutton,node[0]+1,node[1])
                foodIsFound = True
                break
            elif currentButton.styleSheet().split()[0] == 'background-color:white;':
                yellowbutton = PushButton('', style=self.Styles["Yellow"],row=node[0],column=node[1], color="yellow")
                self.Buttons[node[0]][node[1]] = yellowbutton
                yellowbutton.setEnabled(False)
                self.layout.addWidget(yellowbutton,node[0]+1,node[1])
                loop = QEventLoop()
                QTimer.singleShot(40, loop.quit)
                loop.exec_()
            elif currentButton.styleSheet().split()[0] == 'background-color:#423e40;':
                continue
            dicnode = (node[0], node[1])
            visited[dicnode] = True
            for d in 'ESNW':
                if d == 'E':
                    childnode = [node[0], node[1] + 1]
                elif d == 'S':
                    childnode = [node[0], node[1] - 1]
                elif d == 'N':
                    childnode = [node[0] + 1, node[1]]
                elif d == 'W':
                    childnode = [node[0] - 1, node[1]]

                dicChild = (childnode[0], childnode[1])
                checknode = self.checkNode(childnode)
                if((checknode == 'path' or checknode == 'food' or checknode == 'start' or checknode == 'foundfood' or checknode == 'foundpath' or checknode == 'visitedpath') and visited[dicChild] == False):
                # if checknode != 'index' and checknode != None:
                    bfspath[dicChild] = dicnode
                    if childnode not in queue:
                        queue.append(childnode)
        
        fwdpath = {}
        foodcell = [node[0], node[1]]
        dicFood = (foodcell[0], foodcell[1])
        dicStart = (startcell[0], startcell[1])
        while(dicFood != dicStart):
            fwdpath[bfspath[dicFood]] = dicFood
            dicFood = bfspath[dicFood]

        return [fwdpath, foodcell, foodIsFound]

    def greenPacman(self, startcell):
        greenbutton = PushButton('', style=w.Styles["Green"],row=startcell[0],column=startcell[1], color="green")
        w.Buttons[startcell[0]][startcell[1]] = greenbutton
        greenbutton.setEnabled(False)
        w.layout.addWidget(greenbutton,startcell[0]+1,startcell[1])

    def buildMap(self, difficulty, foodCount):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            # if widget.styleSheet().split()[0] == 'background-color:#393a3b;':
            #     continue
            if widget is not None:
                widget.setParent(None)

        loop = QEventLoop()

        self.CreateButtons()
        wallCount = 100
        if difficulty == 'Standard':
            wallCount = 150
        elif difficulty == 'Hard':
            wallCount = 200
        QTimer.singleShot(500, loop.quit)
        loop.exec_()
        self.LocateWalls(wallCount)
        
        foodCount = int(foodCount)
        QTimer.singleShot(500, loop.quit)
        loop.exec_()
        self.LocateFoods(foodCount)

        QTimer.singleShot(100, loop.quit)
        loop.exec_()
        pacman = self.LocatePacMan()
        self.pacmanRow = pacman[0]
        self.pacmanColumn = pacman[1]
        self.startcell = [pacman[0], pacman[1]]
        self.greenPacman(self.startcell)

    def run(self, foodCount, algorithm):
        foodCount = int(foodCount)
        startcell = self.startcell
        if algorithm == 'bfs':
            for i in range(foodCount):
                res = self.bfs(startcell)
                # self.timerShowPath = QTimer(w, interval=1000)
                # self.timerShowPath.timeout.connect(lambda: self.showpath(res[0]))
                # self.timerShowPath.start()
                if res[2] == True:
                    self.showpath(res[0])
                startcell = res[1]
        elif algorithm == 'dfs':
            for i in range(foodCount):
                res = self.dfs(startcell)
                if res[2] == True:
                    self.showpath(res[0])
                startcell = res[1]

app = QtWidgets.QApplication(sys.argv)
w = MyWindow()
w.setWindowTitle('Searchs Algorithm')
w.show()



# startcell = [w.pacmanRow, w.pacmanColumn]
# w.run(5, 'bfs', startcell)
# w.run(5, 'dfs', startcell)




sys.exit(app.exec_())

