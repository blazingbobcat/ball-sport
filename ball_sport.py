#Ball sport alpha v0.2
#by Josh Klipstein
#November 6, 2018

import pygame
from ball_player import *
from ball_ball_class import *
from math import *
pygame.init()#initialize pygame window

#Initialize window dimensions
win_x = 1000
win_y = 500
win = pygame.display.set_mode((win_x, win_y))#Create pygame window
pygame.display.set_caption("BALL SPORT -- BY JOSH KLIPSTEIN")#Name pygame window
#Instructions for game
instructions = ["Welcome to Ball Sport!", \
                "This game will have you juggling 3 balls",\
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
play = 0 #counter for game playing
c = 0
d = 0

#Function to redraw everything in game window
def redraw_game_window():
    pygame.Surface.fill(win,(255,255,255)) #Keep background white

    c = 1
    if play == 0:
        #Print instructions before game starts
        for i in instructions:
            j = font3.render(i, 1, (0,0,0))
            win.blit(j, (win_x // 2 - 2.7*len(i), 23 * c))
            c += 1
    
    #Render the score text on screen
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (10,10))

    #Draw arms
    l_arm.draw(win)
    r_arm.draw(win)
    
    #Draw hands
    hands[0].draw(win)
    hands[1].draw(win)

    #Draw the balls
    for ball in balls:
        ball.draw(win)

    man.draw(win) #Draw our player

    #Print "Game Over" if gameOver variable is 1
    if gameOv == 1:
        gameOver = font2.render('Game Over', 1, (128,0,0)) #Game over sign
        inst = font.render('Press space for new game.',\
                           1, (128,0,0)) #Instructions to quit
                                         #to quit game
        inst_2 = font.render('Or press ESC to quit.',\
                             1, (128,0,0))

        #Display messages
        win.blit(gameOver, (win_x // 2 - 180, win_y - 400))
        win.blit(inst, (win_x // 2 - 140, win_y - 300))
        win.blit(inst_2, (win_x // 2 - 140, win_y - 250))
    elif gameOv == 2:
        #Display this message if player hits ESC
        gameOver = font2.render('Game Over', 1, (128,0,0))
        win.blit(gameOver, (win_x // 2 - 180, win_y - 400))
        
    pygame.display.update()#keep updating display

#End function
            
#Font variables for score
font = pygame.font.SysFont('comicsans', 30, True, True)
font2 = pygame.font.SysFont('comicSans', 100, False, True)
font3 = pygame.font.SysFont('comicSans', 20, False, True)

#Create instance of player
man = player(win_x // 2 - 32, win_y - 100, 64, 64)

#Initialize balls and ball list
ball1 = ball(man.x + 32, man.y + 32, 16, 16, 104, 0)
ball2 = ball(man.x + 32, man.y + 32, 16, 16, 202, 1)
ball3 = ball(man.x + 32, man.y + 32, 16, 16, 301, 2)
balls = []
balls.append(ball1) 
balls.append(ball2)
balls.append(ball3)

#Initialize all arm variables
l_arms = [arm([(man.x + 32, man.y + 32),
               (man.x + 32 - z * 50, man.y + 64),
             (man.x + 32 - z * 50, man.y + 64),
               (man.x + 32 - z * 100, man.y + 32)])
            for z in range(1, 4)]
r_arms = [arm([(man.x + 32, man.y + 32),
               (man.x + 32 + z * 50, man.y + 64),
             (man.x + 32 + z * 50, man.y + 64),
               (man.x + 32 + z * 100, man.y + 32)])
            for z in range(1, 4)]
l_arm = l_arms[c]
r_arm = r_arms[d]

#Initialize hands
hands = [hand(l_arm.getCoords()[3][0] - 16,
              l_arm.getCoords()[3][1] - 32, 32, 32, False),
         hand(r_arm.getCoords()[3][0] - 16,
              r_arm.getCoords()[3][1] - 32, 32, 32, True)]

#main loop
run = True #Start game running
while run:
    #Begin game loop with clock 
    clock.tick(10)

    #Check if balls have fallen
    for ball in balls:
        if ball.visibility == True:
            if ball.getCoords()[1] + 8 >= hands[0].y:
                if ball.getCoords()[0] + 8 >= hands[0].x\
                and ball.getCoords()[0] + 8 <= hands[0].x+32:
                    score += 10 #Increase score if ball is caught
                    ball.caughtBall(True) #Change side of ball caught
                elif ball.getCoords()[0] + 8 >= hands[1].x\
                and ball.getCoords()[0] + 8 <= hands[1].x+32:
                    score += 10 
                    ball.caughtBall(False)
                else:
                    #Game is over if one of the balls is fallen
                    gameOv = 1
                    play = 2 #Explicitly stop game
                    for z in balls:
                        z.visibility = False #Remove balls

    #Check score to add other ball
    if score == 100:
        ball3.visibility = True

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
            c = 0
            d = 0
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            hands[0].x = l_arm.getCoords()[3][0]-16
            hands[0].y = l_arm.getCoords()[3][1]-32
            hands[1].x = r_arm.getCoords()[3][0]-16
            hands[1].y = r_arm.getCoords()[3][1]-32
            
            #Reset balls in list and x- and y-coordinates; and angle
            ball1.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball2.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball3.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball1.caughtBall(False)
            ball2.caughtBall(False)
            ball3.caughtBall(False)
            ball1.visibility = True
            ball2.visibility = True
            ball3.visibility = False
            
    if keys[pygame.K_LEFT]:
        #Left key gets pressed
        #Extend left arm and contract right arm
        if c < 2 and d > 0:
            c+=1
            d-=1
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            hands[0].x = l_arm.getCoords()[3][0]-16
            hands[0].y = l_arm.getCoords()[3][1]-32
            hands[1].x = r_arm.getCoords()[3][0]-16
            hands[1].y = r_arm.getCoords()[3][1]-32
        elif c < 2 and d == 0:
            c+=1
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            hands[0].x = l_arm.getCoords()[3][0]-16
            hands[0].y = l_arm.getCoords()[3][1]-32
            hands[1].x = r_arm.getCoords()[3][0]-16
            hands[1].y = r_arm.getCoords()[3][1]-32
            
    elif keys[pygame.K_RIGHT]:
        #Right key gets pressed
        #Extend right arm and contract left
        if d < 2 and c > 0:
            d+=1
            c-=1
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            hands[0].x = l_arm.getCoords()[3][0]-16
            hands[0].y = l_arm.getCoords()[3][1]-32
            hands[1].x = r_arm.getCoords()[3][0]-16
            hands[1].y = r_arm.getCoords()[3][1]-32
        elif d < 2 and c == 0:
            d+=1
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            hands[0].x = l_arm.getCoords()[3][0]-16
            hands[0].y = l_arm.getCoords()[3][1]-32
            hands[1].x = r_arm.getCoords()[3][0]-16
            hands[1].y = r_arm.getCoords()[3][1]-32
            
    elif keys[pygame.K_ESCAPE]:
        #Escape key quits game.  Flash game over screen if ESC is pressed
        gameOv = 2
        play = 2 #Also stop game explicitly
        run = False
    else:
        pass

    redraw_game_window() #Recall the redraw function if game playing
pygame.quit()#end pygame session
