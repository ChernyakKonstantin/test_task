import random

MAP_SIZE = 10

class EmptyCell:
    """ This class instances fill field empty cells.
        Its purpose is to indicate that a player missed.
    """
    def isShot(self):
        return False

class Ship:
    """ This class instances is logical unit a player's ship.
        Ship health is number of non-hit ships cells
    """
    def __init__(self, size):
        self.size = size
        self.health = self.size

    def isDead(self):
        """ Return True if the ship was destroyed.
            Otherwise return False.
        """
        if self.health == 0:
            return True
        else:
            return False
    
    def isShot(self):
        """ Return True if the ship was hit. 
            Otherwise return False. 
        """
        return True
    
    def getDamage(self):
        """ Substract from the ship health one score. """
        self.health -= 1
              
class OneDeckShip(Ship):
    """ One-cell sized ship. """
    def __init__(self):
        super().__init__(size = 1)
    
class TwoDeckShip(Ship):
    """ Two-cell sized ship. """
    def __init__(self):
        super().__init__(size = 2)
    
class ThreeDeckShip(Ship):
    """ Three-cell sized ship. """
    def __init__(self):
        super().__init__(size = 3)
    
class FourDeckShip(Ship):
    """ Four-cell sized ship. """
    def __init__(self):
        super().__init__(size = 4)

class GameField:
    """ This class store game field data.
        A ship cells refer to its instance.
        Field can be filled randomly. 
    """
    def __init__(self):
        self.size = MAP_SIZE

        self.emptyСell = EmptyCell()
        self.field = [[self.emptyСell for i in range(self.size)] for j in range(self.size)]
        
    def isShot(self, idx):
        """ Interface to ship isShot function. """
        row = idx[0]
        col = idx[1]
        return self.field[row][col].isShot()

    def getDamage(self,idx):
        """ Interface to ship getDamage function. """
        row = idx[0]
        col = idx[1]
        self.field[row][col].getDamage()

    def isLoser(self):
        """ Return True if all player's ships are destroyed. 
            Otherwise return False.
        """
        if all([ship.isDead() for ship in self.ships]):
            return True
        else:
            return False

    def _selectPos(self):
        """ Return randomly selected ship position. """
        return random.choice(self.possibleCell)
    
    def _selectOrient(self):
        """ Return randomly selected ship orientation. """
        hor = 0
        vert = 1
        return random.choice([hor,vert])
    
    def _placeHor(self, pos, ship):
        """ Return cells indexes of horizontally placed ship. """
        i = pos[0]
        j = pos[1]
        return [(i, j + step) for step in range(ship.size)]

    def _placeVert(self, pos, ship):
        """ Return cells indexes of vetrically placed ship. """
        i = pos[0]
        j = pos[1]
        return [(i + step, j) for step in range(ship.size)]
    
    def _isCorrect(self, cells):
        """ Return True if ship all cells are possible and empty.
            Otherwise return False.
        """
        flags = []
        for cell in cells:
            res = cell in self.possibleCell
            flags.append(res)
        if all(flags):
            return True
        else:
            return False
            
    def _restrictCellsVert(self, pos, ship):
        """ Remove cells occupied with vertically placed ship from available cells. """
        i = pos[0] - 1
        j = pos[1] - 1
        for step in range(ship.size + 2):
            try:
                self.possibleCell.remove((i, j + step))
            except ValueError:
                pass
            try:
                self.possibleCell.remove((i + 1, j + step))
            except ValueError:
                pass
            try:
                self.possibleCell.remove((i + 2, j + step))
            except ValueError:
                pass

    def _restrictCellsHor(self, pos, ship):
        """ Remove cells occupied with horizontallly placed ship from available cells. """
        i = pos[0] - 1
        j = pos[1] - 1
        for step in range(ship.size + 2):
            try:
                self.possibleCell.remove((i + step, j))
            except ValueError:
                pass
            try:
                self.possibleCell.remove((i + step, j + 1))
            except ValueError:
                pass
            try:
                self.possibleCell.remove((i + step, j + 2))             
            except ValueError:
                pass
            
    def setCells(self, cells, ship):
        """ Assign the ship to selected cells. """
        for cell in cells:
            i = cell[0]
            j = cell[1]
            self.field[i][j] = ship
                   
    def randomFill(self):
        """ Fill the field with randomly placed ships. """
        self.ships = [FourDeckShip(),
                ThreeDeckShip(),
                ThreeDeckShip(),
                TwoDeckShip(),
                TwoDeckShip(),
                TwoDeckShip(),
                OneDeckShip(),
                OneDeckShip(),
                OneDeckShip(),
                OneDeckShip()]
        self.possibleCell = [(i,j) for i in range(self.size) for j in range(self.size)]
        hor = 0
        vert = 1
        for ship in self.ships:
            done = False
            while not done:
                pos = self._selectPos()
                orient = self._selectOrient()
            
                if orient == hor:
                    cells = self._placeHor(pos, ship)
                elif orient == vert:
                    cells = self._placeVert(pos, ship)
                    
                if self._isCorrect(cells):
                    done = True
                else: 
                    done = False
            
            if orient == hor:
                self._restrictCellsVert(pos, ship)
            if orient == vert:
                self._restrictCellsHor(pos, ship)
            
            self.setCells(cells, ship)
            
    def manualFill(self, cells):
        """ Function accept list of cells and 
            define to which ship assign field cells.
        """
        if len(cells) == 4:
            ship = FourDeckShip()
        if len(cells) == 3:
            ship = ThreeDeckShip()
        if len(cells) == 2:
            ship =TwoDeckShip()
        if len(cells) == 1:
            ship = OneDeckShip()
        self.setCells(cells, ship)

class Player:
    """ This class provide player's activity
        and player's interaction with game field.
    """
    def __init__(self, name):
        self.name = name
        self.gameField = GameField()
        self.selectedCell = None

    def isShot(self, idx):
        """ Interface to GameField isShot function. """
        return self.gameField.isShot(idx)

    def isLoser(self):
        """ Interface to GameField isLoser function. """
        return  self.gameField.isLoser()

    def randomFill(self):
        """ Interface to GameField randomFill function. """
        self.gameField.randomFill()

    def manualFill(self, cells):
        """ Interface to GameField manualFill function. """
        self.gameField.manualFill(cells)

    def attack(self):
        """ Return a cell to hit. """
        return self.selectedCell

    def getDamage(self, idx):
        """ Interface to GameField getDamage function. """
        return self.gameField.getDamage(idx)

    def setSelection(self, cell):
        """ Interface of cell selection to hit"""
        self.selectedCell = cell

class AIPlayer(Player):
    """ This class provide AI player. """
    def __init__(self):
        super().__init__(name = "AI player")
        self.possibleCells = self.getPossibleCells()
        self.randomFill()

    def getPossibleCells(self):
        fieldSize = self.gameField.size
        return [(i,j) for i in range(fieldSize) for j in range(fieldSize)]

    def _removeCell(self, usedCell):
        """ Exclude used cell from possible options. """
        self.possibleCells.remove(usedCell)

    def _sampleCell(self):
        """ Randomly sample a possible cell to hit. """
        return random.choice(self.possibleCells)
    
    def naiveAttack(self):
        """ Bot randomly sample a cell to hit
            and exclude it from possible options 
            to avoid a reuse.
        """
        cell = self._sampleCell()
        self._removeCell(cell)
        return cell




