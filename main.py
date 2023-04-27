import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtCore import QTimer

import random
from queue import PriorityQueue
import random
from PyQt5.QtCore import QPropertyAnimation, QPoint


class PushButton(QtWidgets.QPushButton):
    def __init__(self, text, style, row, column, color, parent=None):
        super(PushButton, self).__init__(text, parent)
        self.setStyleSheet(style)
        self.setText(text)
        self.setMinimumSize(QSize(35, 35))
        self.setMaximumSize(QSize(35, 35))
        self.color = color


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
        width = 1000
        height = 700
        self.setFixedSize(width, height)
        self.rows = 20
        self.columns = 30
        self.Buttons = [[0 for _ in range(self.columns)]
                        for __ in range(self.rows)]
        self.count = 1
        self.foods = []

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
            "Orange": """
                background-color:orange;
                max-height:35px;
                max-width:35px;

                border :0.5px solid orange;
                """,
            "Yellow": """
                background-color:yellow;
                max-height:35px;
                max-width:35px;
                border :0.5px solid yellow;
                """,
            "Gray": """
                background-color:#423e40;
                max-height:35px;
                max-width:35px;
                border :0.50px solid gray;
                """,
            "Green": """
                background-color:green;
                max-height:35px;
                max-width:35px;
                border :0.5px solid gray;
                """,
            "Blue": """
                background-color:#03fc77;
                max-height:35px;
                max-width:35px;
                border :0.5px solid #03fc77;
                """,
            "Red": """
                background-color:red;
                max-height:35px;
                max-width:35px;

                border :0.5px solid red;
                """,

        }

        Widget = QtWidgets.QWidget()
        self.vertical = QtWidgets.QVBoxLayout()
        self.inWidget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(self.inWidget)
        self.vertical.addWidget(self.inWidget)
        self.CreateButtons()

        startcell = None

        Widget.setLayout(self.vertical)
        self.setCentralWidget(Widget)

        # Combo Boxes
        self.combobox_algorithm = QtWidgets.QComboBox(self)
        self.combobox_algorithm.setGeometry(50, 50, 60, 60)
        self.combobox_algorithm.addItems(['bfs', 'dfs', 'A*'])
        self.vertical.addWidget(self.combobox_algorithm)

        self.combobox_difficulty = QtWidgets.QComboBox(self)
        self.combobox_difficulty.setGeometry(50, 50, 60, 60)
        self.combobox_difficulty.addItems(['Easy', 'Standard', 'Hard'])
        self.vertical.addWidget(self.combobox_difficulty)

        self.combobox_food = QtWidgets.QComboBox(self)
        self.combobox_food.setGeometry(50, 50, 60, 60)
        self.combobox_food.addItems(
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
        self.vertical.addWidget(self.combobox_food)

        # Build Button
        self.build_btn = QtWidgets.QPushButton("Build", clicked=lambda: self.buildMap(
            self.combobox_difficulty.currentText(), self.combobox_food.currentText()))
        self.vertical.addWidget(self.build_btn)

        # Start Button
        self.start_btn = QtWidgets.QPushButton("Start", clicked=lambda: self.run(
            self.combobox_food.currentText(), self.combobox_algorithm.currentText()))
        self.vertical.addWidget(self.start_btn)
        self.start_btn.hide()

    def CreateButtons(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if (row == 0 or row == 19) or (column == 0 or column == 29):
                    button = PushButton(
                        '', style=self.Styles["Gray"], row=row, column=column, color="gray")
                    self.layout.addWidget(button, row + 1, column)
                else:
                    button = PushButton(
                        '', style=self.Styles["White"], row=row, column=column, color="white")
                    self.Buttons[row][column] = button
                    button.setEnabled(False)
                    self.layout.addWidget(button, row+1, column)

    def LocateWalls(self, number):
        for i in range(1, number + 1):
            wallRow = random.randint(1, 18)
            wallColumn = random.randint(1, 28)
            button = PushButton(
                '', style=self.Styles["Gray"], row=wallRow, column=wallColumn, color="gray")
            self.Buttons[wallRow][wallColumn] = button
            button.setEnabled(False)
            self.layout.addWidget(button, wallRow+1, wallColumn)

    def LocateFoods(self, number):
        for i in range(1, number + 1):
            foodRow = random.randint(1, 18)
            foodColumn = random.randint(1, 28)
            self.foods.append([foodRow, foodColumn, False])
            button = PushButton(
                '', style=self.Styles["Orange"], row=foodRow, column=foodColumn, color="orange")
            self.Buttons[foodRow][foodColumn] = button
            button.setEnabled(False)
            self.layout.addWidget(button, foodRow+1, foodColumn)

    def LocatePacMan(self):
        pacmanRow = random.randint(1, 18)
        pacmanColumn = random.randint(1, 28)
        button = PushButton(
            '', style=self.Styles["Yellow"], row=pacmanRow, column=pacmanColumn, color="yellow")
        self.Buttons[pacmanRow][pacmanColumn] = button
        button.setEnabled(False)
        self.layout.addWidget(button, pacmanRow+1, pacmanColumn)
        return [pacmanRow, pacmanColumn]

    def move(self):
        currrow = self.pacmanRow
        currcol = self.pacmanColumn

        for i in range(0, 10):
            direction = random.randint(1, 4)
            coordinates = directions(direction, currrow, currcol)
            currrow = coordinates[0]
            currcol = coordinates[1]

            button = PushButton(
                '', style=self.Styles["Yellow"], row=currrow, column=currcol, color="yellow")
            currentButton = self.Buttons[currrow][currcol]

            if(currentButton == 0):
                continue
            elif(currentButton.styleSheet().split()[0] == 'background-color:#423e40;'):
                continue
            else:
                self.Buttons[currrow][currcol] = button
                button.setEnabled(False)
                self.layout.addWidget(button, currrow+1, currcol)

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

            yellowbutton = PushButton(
                '', style=self.Styles["Yellow"], row=currcell[0], column=currcell[1], color="yellow")

            if currentButton == 0:
                continue
            elif currentButton.styleSheet().split()[0] == 'background-color:orange;':
                redbutton = PushButton(
                    '', style=self.Styles["Red"], row=currcell[0], column=currcell[1], color="red")
                self.Buttons[currcell[0]][currcell[1]] = redbutton
                redbutton.setEnabled(False)
                self.layout.addWidget(redbutton, currcell[0]+1, currcell[1])
                foodIsFound = True
                break
            elif currentButton.styleSheet().split()[0] == 'background-color:white;':
                self.Buttons[currcell[0]][currcell[1]] = yellowbutton
                yellowbutton.setEnabled(False)
                self.layout.addWidget(yellowbutton, currcell[0]+1, currcell[1])
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
        showedPath = []
        for step in path:
            if(step[0] != self.pacmanRow or step[1] != self.pacmanColumn):
                bluebutton = PushButton(
                    '', style=self.Styles["Blue"], row=step[0], column=step[1], color="blue")
                if(self.Buttons[step[0]][step[1]].styleSheet().split()[0] == 'background-color:yellow;' or
                   self.Buttons[step[0]][step[1]].styleSheet().split()[0] == 'background-color:#03fc77;'):
                    self.Buttons[step[0]][step[1]] = bluebutton
                    bluebutton.setEnabled(False)
                    self.layout.addWidget(bluebutton, step[0]+1, step[1])
                    loop = QEventLoop()
                    QTimer.singleShot(70, loop.quit)
                    loop.exec_()

                    showedPath.append([step[0], step[1]])
        # showedPath = showedPath.reverse()
        # self.timerShowPath.stop()
        self.showSteps(showedPath)

    def showSteps(self, showedPath):
        for i in range(len(showedPath)-1, -1, -1):
            step = showedPath[i]
            numberbutton = PushButton(str(
                self.count), style=self.Styles["Blue"], row=step[0], column=step[1], color="blue")
            self.Buttons[step[0]][step[1]] = numberbutton
            numberbutton.setEnabled(False)
            self.layout.addWidget(numberbutton, step[0]+1, step[1])
            self.count += 1
            loop = QEventLoop()
            QTimer.singleShot(70, loop.quit)
            loop.exec_()

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
                redbutton = PushButton(
                    '', style=self.Styles["Red"], row=node[0], column=node[1], color="red")
                self.Buttons[node[0]][node[1]] = redbutton
                redbutton.setEnabled(False)
                self.layout.addWidget(redbutton, node[0]+1, node[1])
                foodIsFound = True
                break
            elif currentButton.styleSheet().split()[0] == 'background-color:white;':
                yellowbutton = PushButton(
                    '', style=self.Styles["Yellow"], row=node[0], column=node[1], color="yellow")
                self.Buttons[node[0]][node[1]] = yellowbutton
                yellowbutton.setEnabled(False)
                self.layout.addWidget(yellowbutton, node[0]+1, node[1])
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
        greenbutton = PushButton(
            '', style=self.Styles["Green"], row=startcell[0], column=startcell[1], color="green")
        self.Buttons[startcell[0]][startcell[1]] = greenbutton
        greenbutton.setEnabled(False)
        self.layout.addWidget(greenbutton, startcell[0]+1, startcell[1])

    def buildMap(self, difficulty, foodCount):
        self.combobox_algorithm.hide()
        self.combobox_difficulty.hide()
        self.combobox_food.hide()
        self.build_btn.hide()
        self.start_btn.hide()

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
        self.start_btn.show()

    def run(self, foodCount, algorithm):
        loop = QEventLoop()

        self.start_btn.hide()

        foodCount = int(foodCount)
        startcell = self.startcell
        if algorithm == 'bfs':
            for i in range(foodCount):
                res = self.bfs(startcell)
                if res[2] == True:
                    self.showpath(res[0])
                startcell = res[1]
        elif algorithm == 'dfs':
            for i in range(foodCount):
                res = self.dfs(startcell)
                if res[2] == True:
                    self.showpath(res[0])
                startcell = res[1]

        elif algorithm == 'A*':
            for i in range(foodCount):
                nesrestfood = self.nearestFood(startcell)
                # print(startcell)
                # print(nesrestfood)
                res = self.aStar(startcell, nesrestfood)
                if res[2] == True:
                    self.showpath(res[0])
                startcell = res[1]

        QTimer.singleShot(1500, loop.quit)
        loop.exec_()

        self.combobox_algorithm.show()
        self.combobox_difficulty.show()
        self.combobox_food.show()
        self.build_btn.show()
        self.start_btn.show()
        self.count = 1
        self.foods = []

    def h(self, cell1, cell2):
        x1, y1 = cell1
        x2, y2 = cell2
        return abs(x1-x2) + abs(y1-y2)

    def nearestFood(self, startcell):
        foods = self.foods
        nearestFood = foods[0]
        distance = 9999999
        for i in range(len(foods)):
            # print(foods)
            if foods[i][2] == False:
                foodcell = (foods[i][0], foods[i][1])
                manhattanDistance = self.h(startcell, foodcell)
                if manhattanDistance < distance:
                    distance = manhattanDistance
                    nearestFood = foodcell
        for i in range(len(foods)):
            # print(foods[i])
            # print(nearestFood)
            if foods[i] == [nearestFood[0], nearestFood[1], False]:
            #    print('asfjksagjfsa')
               self.foods[i][2] = True
        return nearestFood

    def aStar(self, startCell, food):
        startCell = (startCell[0], startCell[1])
        g_score = {}
        f_score = {}
        astarpath = {}
        foodIsFound = False
        for row in range(self.rows):
            for column in range(self.columns):
                g_score[(row, column)] = float('inf')
                f_score[(row, column)] = float('inf')
        g_score[startCell] = 0

        tupleFood = (food[0], food[1])

        f_score[startCell] = self.h(startCell, tupleFood)

        open = PriorityQueue()
        open.put((self.h(startCell, tupleFood), self.h(
            startCell, tupleFood), startCell))

        while not open.empty():
            currCell = open.get()[2]
            currentButton = self.Buttons[currCell[0]][currCell[1]]
            if currentButton == 0 or currentButton.styleSheet().split()[0] == 'background-color:#423e40;':
                continue
            elif currentButton.styleSheet().split()[0] == 'background-color:orange;':
                redbutton = PushButton('', style=self.Styles["Red"], row=currCell[0], column=currCell[1], color="red")
                self.Buttons[currCell[0]][currCell[1]] = redbutton
                redbutton.setEnabled(False)
                self.layout.addWidget(
                    redbutton, currCell[0]+1, currCell[1])
                foodIsFound = True
                break
            elif currentButton.styleSheet().split()[0] == 'background-color:white;':
                yellowbutton = PushButton('', style=self.Styles["Yellow"], row=currCell[0], column=currCell[1], color="yellow")
                self.Buttons[currCell[0]][currCell[1]] = yellowbutton
                yellowbutton.setEnabled(False)
                self.layout.addWidget(yellowbutton, currCell[0]+1, currCell[1])
                loop = QEventLoop()
                QTimer.singleShot(40, loop.quit)
                loop.exec_()

            for d in 'ESNW':
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'S':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] + 1, currCell[1])
                elif d == 'W':
                    childCell = (currCell[0] - 1, currCell[1])
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + self.h(childCell, tupleFood)

                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, self.h(childCell, tupleFood), childCell))
                    astarpath[childCell] = currCell

        fwdpath = {}
        foodcell = [currCell[0], currCell[1]]
        dicFood = (foodcell[0], foodcell[1])
        dicStart = (startCell[0], startCell[1])
        while(dicFood != dicStart):
            fwdpath[astarpath[dicFood]] = dicFood
            dicFood = astarpath[dicFood]

        return [fwdpath, foodcell, foodIsFound]


app = QtWidgets.QApplication(sys.argv)
w = MyWindow()
w.setWindowTitle('Searchs Algorithm')
w.show()


# startcell = [w.pacmanRow, w.pacmanColumn]
# w.run(5, 'bfs', startcell)
# w.run(5, 'dfs', startcell)


sys.exit(app.exec_())
