import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QPoint

WINDOW_SIZE = (420, 620)

GAME_FIELD_SIZE = (400, 400)
GAME_FIELD_POS = (10, 210)

class ButtonFieldFrame(QFrame):
    """ This class provides a grid
        of buttons, representing ButtonFieldFrame 
        field. 
    """
    cellSignal = pyqtSignal()
    def __init__(self, parent):
        super().__init__(parent)
        self.btnClicked = None
        self._initField()

    def _initField(self):
        self.setFixedSize(400,400)
        grid = QGridLayout()
        positions = [(i,j) for i in range(10) for j in range(10)]
        for position in positions:
            button = CellButton(self, position)
            button.clicked.connect(self.buttonClicked)
            grid.addWidget(button, *position)
        self.setLayout(grid)

    def buttonClicked(self):
        self.btnClicked = self.sender()
        self.cellSignal.emit()

class CellButton(QPushButton):
    """ This class provides a cell button.
        Non-used cell is gray color.
        Used empty cell is blue. Used ship cell is red.
        Cell stores its row and columns position. 
    """
    def __init__(self, parent, idx):
        super().__init__(parent)
        self.idx = idx
        self.initButton()

    def initButton(self):
        self.setStyleSheet("QPushButton { background-color: #575757; \
                                          border-style: solid; \
                                          border-width: 1px; \
                                          border-color: black; } \
                            QPushButton:pressed {  background-color: #404040; \
                                                   border-style: solid; \
                                                   border-width: 1px; \
                                                   border-color: black; }")
        self.setFixedSize(40,40)

    def disable(self):
        """ Interface to disable button. """
        self.setEnabled(False)

    def getIdx(self):
        """ Interface to get the button 
            row and column position. 
        """
        return self.idx

    def setColor(self, color):
        """ Interface to set the button color. """
        self.setStyleSheet("QPushButton { background-color: %s; \
                                          border-style: solid; \
                                          border-width: 1px; \
                                          border-color: black; }" %color)        

class GameWindow(QMainWindow):
    """ This class contains game main window.
        Initial window is ships placement. 
        Since all ships are placed, startFlag = True,
        ButtonFieldFrame field is shown.
        gameStart sender is GameWindow itself.

    """
    
    def __init__(self):
        super().__init__()
        self._initWindow()
    
    def _initWindow(self):
        self.setWindowTitle("Battleship")
        self.setFixedSize(420, 520)

        self.centralWidget = QWidget(self)
        self.placementFrame = ButtonFieldFrame(self) 
        self.placementFrame.move(10,110)
        self.buttonFieldFrame = ButtonFieldFrame(self)
        self.buttonFieldFrame.move(10,110)

        self.label = QLabel("Ships: 0", self)
        self.label.move(50, 50)
        
        self.rndBtn = QPushButton("Randomize", self)
        self.rndBtn.move(200,50)
        self.placeShipBtn = QPushButton("Place ship", self)
        self.placeShipBtn.move(300,50)

        self.resetBtn =  QPushButton("Reset", self)
        self.resetBtn.move(300,50)

        self._enableWidget(self.placementFrame)
        self._disableWidget(self.buttonFieldFrame)
        self._disableWidget(self.resetBtn)

    def startGame(self):
        """ Switch placement view to battle view"""
        self.label.setText("")
        self._enableWidget(self.buttonFieldFrame)
        self._enableWidget((self.resetBtn))
        self._disableWidget(self.placementFrame)
        self._disableWidget(self.rndBtn)
        self._disableWidget(self.placeShipBtn)
    
    def _enableWidget(self, widget):
        widget.setEnabled(True)
        widget.setVisible(True)

    def _disableWidget(self, widget):
        widget.setEnabled(False)
        widget.setVisible(False)

 
