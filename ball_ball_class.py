#Ball sport alpha v0.1
#Josh Klipstein
#October 12, 2018

#Ball class

import pygame
from math import *

#Load ball image
img = pygame.image.load('graphics/d.bmp')

class ball(object):
    def __init__(self, x0, y0, width, height, number):
        #Initialize all ball attributes
        self.__x0 = x0
        self.__y0 = y0
        self.__width = width
        self.__height = height 
        self.number = number#number of ball
        self.__angle = pi / 2
        self.__tempAngle = (number + 1) * (pi / 6) + pi
        self.__radius = (number + 1) * 54
        self.__x = x0 + (self.__radius * cos(self.__angle))
        self.__y = y0 - (self.__radius * sin(self.__angle))

    #Draw ball function
    def draw(self, win):
        #Move ball before drawing
        self.move()
        win.blit(img, (self.__x, self.__y))

    #Move ball function
    def move(self):
        #Move the ball in a parabolic pattern starting from one player's hand
        #and ending up in the other
        if self.__tempAngle == (self.number) * (-pi / 6):
            self.__angle += pi / (24 * (self.number + 1))
            self.__x = self.__x0 + (self.__radius * cos(self.__angle))
            self.__y = self.__y0 - (self.__radius * sin(self.__angle))
            if self.__angle >= (self.number) * (pi / 6) + pi:
                self.__tempAngle = (self.number) * (pi / 6) + pi
        else:
            self.__angle -= pi / (24 * (self.number + 1))
            self.__x = self.__x0 + (self.__radius * cos(self.__angle))
            self.__y = self.__y0 - (self.__radius * sin(self.__angle))
            if self.__angle <= (self.number)* (-pi / 6):
                self.__tempAngle = (self.number) * (-pi / 6)

    #Function to set coordinates and angle of ball
    def setCoord(self, x, y, angle):
        self.__x0 = x
        self.__y0 = y
        self.__angle = angle

    #Function to retrieve coordinates and angle of ball
    def getCoords(self):
        return (self.__x, self.__y, self.__angle)
                    
        
#End class
        
            
        
