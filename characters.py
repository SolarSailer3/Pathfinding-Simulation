'''
characters.py - super and sub class of characters

Featuring:
    Pacman - "Papa needs his cherries"
    Ghost Gang - "Knock Knock", "Who's there?", "boo"

'''

# import random

class Character():
    '''
    super class Character
    __init__ arguments:
        row : within MAXROWS
        col : within MAXCOLS
        name: names are passed in
        colour: colours are passed in
    '''

    def __init__(self, name, colour, col, row):
        self.col = col
        self.row = row
        self.name = name
        self.colour = colour
        self.eaten = False
        
    def getRow(self):
        return self.row
    
    def getCol(self):
        return self.col
    
    def getName(self):
        return self.name

    def getColour(self):
        return self.colour
    
    def move(self, coords):
        self.col, self.row = coords

class PacPerson(Character):
    '''
    sub class of character - trying to avoid being eaten by the enemy
    
    '''
    myclass = 'Pacman'

    def __init__(self, name, colour, row, col):
        super().__init__(name, colour, row, col)
        self.invincible = False
        self.invincibility_duration = 0   

class Ghost(Character):
    '''
    sub class of character - the enemy that is trying to eat the main character
    '''
    myclass = 'Ghost'    