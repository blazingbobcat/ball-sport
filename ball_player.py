#Ball sport v1.1
#by Josh Klipstein
#January 3, 2018

#Classes for player parts

import pygame

#Load images for player
img = [pygame.image.load('graphics/a.bmp'),
        pygame.image.load('graphics/c.bmp'),
        pygame.image.load('graphics/e.bmp')]

#Head class
class player(object):
    def __init__(self, x, y, width, height):
        #Initialize player size and position
        self.x = x
        self.y = y
        self.__width = width
        self.__height = height

    def draw(self, win):
        #Our function to draw player
        win.blit(img[1], (self.x, self.y), special_flags=3) #Draw player head

#Class end

#Arms class
class arm(object):
    def __init__(self, coords):
        #Initialize player size and position
        self.__coords = coords
        
    #Function to draw arm
    def draw(self, win):
        pygame.draw.lines(win, (0,0,0), False, self.__coords, 10) #Draw arm

    #Function to get arm coordinates list
    def getCoords(self):
        return self.__coords
        
#Class end

#Hands class
class hand(object):
    def __init__(self, x, y, width, height, side):
        #Initialize player size and position
        self.x = x
        self.y = y
        self.__width = width
        self.__height = height
        self.__side = side
    
    #Function to draw hand
    def draw(self, win):
        if self.__side:
            win.blit(img[2], (self.x, self.y), special_flags = 3)
        else:
            win.blit(img[0], (self.x, self.y), special_flags = 3)

