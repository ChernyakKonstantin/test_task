import sys
import os

from PyQt5.QtWidgets import QApplication

from logic import Player
from logic import AIPlayer
from ui import GameWindow

class Game:
    """ This class contains Battleship game """

    def __init__(self):
        self._initUI()
        self.tmpCells = []
        self.shipAmount = 0
        self.player = Player("User")
        self.bot = AIPlayer()
        self.run()

    def _initUI(self):
        """ Initialization of user interface. """
        self._app = QApplication(sys.argv)
        self.mainWindow = GameWindow()
        self.mainWindow.show()
        self.mainWindow.rndBtn.clicked.connect(self.randBtnHandler)
        self.mainWindow.placeShipBtn.clicked.connect(self.placeShipBtnHandler)
        self.mainWindow.resetBtn.clicked.connect(self.reset)
        self.mainWindow.placementFrame.cellSignal.connect(self.placementHandler)
        self.mainWindow.buttonFieldFrame.cellSignal.connect(self.buttonFieldHandler)

    def randBtnHandler(self):
        """ If button "Randomize" is presed, fill
            player's field with ships randomly """
        self.player.gameField.randomFill()
        self.mainWindow.startGame()

    def placeShipBtnHandler(self):
        """ Place ship to player's field. 
            Since pressed, "Randomize" button is disabled.
            After 10th push battle view is load."""
        self.mainWindow.rndBtn.setEnabled(False)
        self.shipAmount += 1
        if self.shipAmount == 10:
            self.mainWindow.startGame()
        self.player.manualFill(self.tmpCells)
        self.mainWindow.label.setText("Ships: %d" %self.shipAmount)
        self.tmpCells = []

    def placementHandler(self):
        """ Mark selected cells with red color and append them
            to temprorary list
        """
        btnClicked = self.mainWindow.placementFrame.btnClicked
        cell = btnClicked.getIdx()
        self.tmpCells.append(cell)
        btnClicked.setColor("red")
        btnClicked.disable()

    def buttonFieldHandler(self):
        """ If enemy's field cell is pressed, check if enemy's ship
            is shot. If True, substract one health point from the ship.
            Then perform AIPlayer step. If a player lost, show winner's 
            name and restart."""

        btnClicked = self.mainWindow.buttonFieldFrame.btnClicked
        cell = btnClicked.getIdx()

        if self.bot.isShot(cell):
            self.bot.getDamage(cell)
            btnClicked.setColor("red")
            if self.bot.isLoser():
                self.gameOver(self.player.name)
        else:
            btnClicked.setColor("blue")
        btnClicked.disable()

        cell = self.bot.naiveAttack()
        if self.player.isShot(cell):
            self.mainWindow.label.setText("AI hit you!")
            self.player.getDamage(cell)
            if self.player.isLoser():
                self.gameOver(self.bot.name)
        else:
            self.mainWindow.label.setText("AI missed!")

    def gameOver(self, name):
        """ Display winner's name """
        self.mainWindow.label.setText("%s is winner!" %name)
        self.mainWindow.buttonFieldFrame.setEnabled(False)

    def reset(self):
        """ Perform app restart. """
        os.execl(sys.executable, sys.executable, *sys.argv)

    def run(self):
        """ Run application. """
        sys.exit(self._app.exec_())

if __name__ == '__main__':
    game = Game()

