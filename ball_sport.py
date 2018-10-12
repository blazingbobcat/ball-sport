#Ball sport alpha v0.1
#Josh Klipstein
#October 12, 2018

import pygame
from ball_player import *
from ball_ball_class import *
from math import *
pygame.init()#initialize pygame window

win = pygame.display.set_mode((480, 500))#Create pygame window
pygame.display.set_caption("BALL SPORT -- BY JOSH KLIPSTEIN")#Name pygame window
#Instructions for game
instructions = ["Welcome to Ball Sport!", "This game will have you juggling 3 balls",\
                "(2 balls to start) until you drop one them.", \
                "You get 10 points for each catch of the balls.", \
                "You control the left and right hands of your character",\
                "with the arrow keys; and must keep the balls",\
                "moving without falling.",\
                "It's harder than it sounds!",\
                "TIP:  Like in real juggling, you must", \
                "keep your hands moving to keep the balls moving.", \
                "CONTROLS:", "Escape: Quit game",\
                "Space: Start/Restart game",\
                "Left Arrow: Move hands left", \
                "Right Arrow: Move hands right",\
                "Press Space to start playing!"]

clock = pygame.time.Clock() #Initialize time variable
score = 0 #Score variable
gameOv = 0 #variable to end game
x = 0 #ball number variable
play = 0 #counter for game playing

#Function to redraw everything in game window
def redraw_game_window():
    pygame.Surface.fill(win,(255,255,255)) #Keep background white

    c = 1
    if play == 0:
        #Print instructions before game starts
        for i in instructions:
            j = font3.render(i, 1, (0,0,0))
            win.blit(j, (220- 2.7*len(i), 23 * c))
            c += 1
    
    #Render the score text on screen
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (10,10))

    #Draw the balls
    for ball in balls:
            ball.draw(win)

    #Draw player's arms
    for arm in arms:
        arm.draw(win) 

    #Draw player's hands
    for hand in hands:
        hand.draw(win) 

    man.draw(win) #Draw our player

    #Print "Game Over" if gameOver variable is 1
    if gameOv == 1:
        gameOver = font2.render('Game Over', 1, (128,0,0)) #Game over sign
        inst = font.render('Press space for new game.',\
                           1, (128,0,0)) #Instructions to quit
                                         #to quit game
        inst_2 = font.render('Or press X or ESC to quit.',\
                             1, (128,0,0))

        #Display messages
        win.blit(gameOver, (50, 150))
        win.blit(inst, (90, 250))
        win.blit(inst_2, (90, 300))
    elif gameOv == 2:
        #Display this message if player hits ESC
        gameOver = font2.render('Game Over', 1, (128,0,0))
        win.blit(gameOver, (50, 200))
        
    pygame.display.update()#keep updating display

#End function

#Function to check score, and add another ball if score reaches 100
def check_score(score):
    if score == 100:
        ball3.setCoord(230, 272, pi / 2)
        balls.append(ball3)

#End function
        
#Font variables for score
font = pygame.font.SysFont('comicsans', 30, True, True)
font2 = pygame.font.SysFont('comicSans', 100, False, True)
font3 = pygame.font.SysFont('comicSans', 20, False, True)

#Create instance of player
man = player(210, 400, 64, 64)
#Left extended arm:  man.x-127, man.y+32
#Right extended arm:  man.x + 109, man.y+32
#Difference in length:  63 pixels
arms = [arm(man.x-16, man.y+32, 64, 22), arm(man.x, man.y+32, 64, 22),
        arm(man.x-16, man.y+32, 64, 22), arm(man.x, man.y+32, 64, 22)]
hands = [hand(arms[2].x-32, man.y+20, 32, 32), hand(arms[3].x+64, man.y+20,\
                                                    32, 32)]

#Initialize balls and ball list
ball1 = ball(230, 400, 16, 16, 0)
ball2 = ball(230, 336, 16, 16, 1)
ball3 = ball(230, 272, 16, 16, 2)
balls = []

#main loop
run = True #Start game running
while run:
    #Begin game loop with clock 
    clock.tick(27)

    #Check if balls have fallen
    for ball in balls:
        if ball.getCoords()[2] <= (ball.number) * (-pi / 2) \
        or ball.getCoords()[2] >= pi + (ball.number) * (pi / 2):
            if (ball.getCoords()[0] < hands[0].x \
                or ball.getCoords()[0] > hands[0].x + 32) \
               and (ball.getCoords()[0] > hands[1].x +32 \
                    or ball.getCoords()[0] < hands[1].x):
                #Game is over if one of the balls is fallen
                gameOv = 1
                play = 2 #Explicitly stop game
                for z in range(len(balls)):
                    balls.pop()
            else:
                score += 10 #Increase score if ball is caught
                check_score(score) #Check the score to add another ball

    #Check if player quits game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()#Create variable handle for key presses

    #Take input from player's keyboard
    #Possible key presses are left, right, space and escape
    #Left = move arms left
    #Right = move arms right
    #Escape = end game (get "game over" screen)
    #Starts new game (counter controlled)

    if keys[pygame.K_SPACE]:
        #Space gets pressed
        #Start game if not started already, or restart game after game over.
        if play != 1:
            gameOv = 0 #Reset game-over condition
            play = 1 #Reset play condition
            score = 0 #Reset score
            #Reset arms
            arms[0].x = man.x-16
            arms[1].x = man.x
            arms[2].x = man.x-16
            arms[3].x = man.x
            hands[0].x = arms[2].x-32
            hands[1].x = arms[3].x+64
            #Reset balls in list and x- and y-coordinates
            ball1.setCoord(230, 400, pi / 2)
            ball2.setCoord(230, 336, pi / 2)
            balls.append(ball1) 
            balls.append(ball2)
            
    if keys[pygame.K_LEFT]:
        #Left key gets pressed
        #Check first if left arm already extended
        if arms[2].x != man.x - 64:
            #Arm is not extended, so extend, and contract other arm.
            #Arms are numbered 1 = left, 2 = right
            arms[2].x -= 2
            hands[0].x = arms[2].x - 32
            if arms[3].x > man.x:
                #Right arm is extended, so contract
                arms[3].x -= 2
                hands[1].x = arms[3].x + 64
            
    elif keys[pygame.K_RIGHT]:
        #Right key gets pressed
        #Check first if right arm is extended, then extend arm and contract
        #other arm if so
        if arms[3].x != man.x + 44:
            arms[3].x += 2
            hands[1].x = arms[3].x + 64
            if arms[2].x < man.x - 16:
                #Left arm is extended, so contract
                arms[2].x += 2
                hands[0].x = arms[2].x - 32
            
    elif keys[pygame.K_ESCAPE]:
        #Escape key quits game.  Flash game over screen if ESC is pressed
        gameOv = 2
        play = 2 #Also stop game explicitly
        run = False
    else:
        pass

    redraw_game_window() #Recall the redraw function if game playing

pygame.quit()#end pygame session
