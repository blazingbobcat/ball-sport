#Ball sport alpha v0.2
#by Josh Klipstein
#November 6, 2018

#Ball class

import pygame
from math import *

#Load ball image
img = pygame.image.load('graphics/d.bmp')

class ball(object):
    def __init__(self, x0, y0, width, height, radius, number):
        #Initialize all ball attributes
        self.__x0 = x0#Initial ball coords
        self.__y0 = y0
        self.__width = width
        self.__height = height
        self.__radius = radius#radius of ball path
        self.number = number + 1#number of ball
        self.__angle = pi / 2 #Angle of ball path
        self.__caught = False #Bool of which hand caught ball ("False" = Right)
        self.__x = x0 + (self.__radius * cos(self.__angle))#Position of ball
        self.__y = y0 - (self.__radius * sin(self.__angle))
        self.visibility = False

    #Draw ball function
    def draw(self, win):
        #Move ball before drawing
        if self.visibility == True:
            self.move()
            win.blit(img, (self.__x, self.__y))

    #Move ball function
    def move(self):
        #Move the ball in a parabolic pattern starting from one player's hand
        #and ending up in the other
        if self.__caught == False:
            self.__angle += pi / (12 * (self.number))
            self.__x = self.__x0 + (self.__radius * cos(self.__angle)) - 8
            self.__y = self.__y0 - (self.__radius * sin(self.__angle)) - 8              
        else:
            self.__angle -= pi / (12 * (self.number))
            self.__x = self.__x0 + (self.__radius * cos(self.__angle)) - 8
            self.__y = self.__y0 - (self.__radius * sin(self.__angle)) - 8
        
    #Function to set coordinates and angle of ball
    def setCoord(self, x, y, angle):
        self.__x0 = x
        self.__y0 = y
        self.__angle = angle

    #Function to retrieve coordinates and angle of ball
    def getCoords(self):
        return (self.__x, self.__y, self.__angle)
                    
    #Function to tell which hand caught ball
    def caughtBall(self, c):
        self.__caught = c

    #Function to get radius of ball
    def getRadius(self):
        return self.__radius

#End class
        
            
        
