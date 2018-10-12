#Ball sport alpha v0.1
#Josh Klipstein
#October 12, 2018

#Classes for player parts

import pygame

#Load images for player
img = [pygame.image.load('graphics/a.bmp'), pygame.image.load('graphics/b.bmp'),
          pygame.image.load('graphics/c.bmp')]

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
        win.blit(img[2], (self.x, self.y)) #Draw player head

#Class end

#Arms class
class arm(object):
    def __init__(self, x, y, width, height):
        #Initialize player size and position
        self.x = x
        self.y = y
        self.__width = width
        self.__height = height
        
    #Function to draw arm
    def draw(self, win):
        #Our function to draw player
        win.blit(img[1], (self.x, self.y)) #Draw player arm


#Class end

#Hands class
class hand(object):
    def __init__(self, x, y, width, height):
        #Initialize player size and position
        self.x = x
        self.y = y
        self.__width = width
        self.__height = height

    #Function to draw hand
    def draw(self, win):
        #Our function to draw player
        win.blit(img[0], (self.x, self.y)) #Draw player hand

#Class end
