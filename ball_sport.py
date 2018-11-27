#Ball sport beta v0.3
#by Josh Klipstein
#November 27, 2018

import pygame
from ball_player import *
from ball_ball_class import *
from math import *
pygame.init() #initialize pygame window
pygame.mixer.init() #intialize mixer

#Initialize window dimensions
win_x = 1000
win_y = 500
win = pygame.display.set_mode((win_x, win_y)) #Create pygame window
pygame.display.set_caption("BALL SPORT -- BY JOSH KLIPSTEIN") #Name pygame window

#Instructions for game
instructions = ["Welcome to Ball Sport!", \
                "This game will have you juggling 3 balls",\
                "(2 balls to start) until you drop one them.", \
                "You get 10 points for each catch of the balls.", \
                "You control the left and right hands of your character",\
                "with the arrow keys; and must keep the balls",\
                "moving without falling.",\
                "This game is for one player or two.",\
                "CONTROLS (for both players):", "Escape: Quit game",\
                "Space: Start game",\
                "Left Arrow: Move hands left", \
                "Right Arrow: Move hands right",\
                "To start one-player game, press 1.", \
                "To start two player game, press 2."]

clock = pygame.time.Clock() #Initialize time variable
score = 0 #Score variable player 1
score2 = 0 #Score variable player 2
gameOv = 0 #variable to end game
play = 0 #counter for game playing
global hiScoreOld
with open("hiScoreLog.txt") as h:
    #Read old high-score into variable from log
    for line in h:
        hiScoreOld = line
hiScore = int(hiScoreOld) #Hi-Score variable
c = 0
d = 0

#Font variables for score
font = pygame.font.SysFont('comicsans', 30, True, True)
font2 = pygame.font.SysFont('comicSans', 100, False, True)
font3 = pygame.font.SysFont('comicSans', 20, False, True)

#Messages
gameOver = font2.render('Game Over', 1, (128,0,0)) #Game over sign
hiSc = font.render('New Hi-Score!', 1, (128,0,0)) #Show that
                                                #player attained a new high score
#Instructions to play or quit game
inst = [font.render('Press 1 or 2 for new game,',
                   1, (128,0,0)), 
        font.render('Or press ESC to quit.',
                     1, (128,0,0)),
        font.render('Player 1!', 1, (0,128,0)),\
        font.render('Player 2!', 1, (0,0,128)),\
        font.render('Press Space when ready', 1, (128,0,0))]

#Game Text
text = [font.render('P1: ', 1, (0,0,0)),\
        font.render('Hi-Score: ', 1, (0,0,0)),\
        font.render('P2: ', 1, (0,0,0)),\
        font.render('P1 wins!', 1, (128,0,0)),\
        font.render('P2 wins!', 1, (128,0,0)),\
        font.render('P1 wins with high score!', 1, (128,0,0)),\
        font.render('P2 wins with high score!', 1, (128,0,0))]

#Initialize all sounds
intro = pygame.mixer.Sound('sounds/Short_triumphal_fanfare-John_Stracke-815794903.wav')
whoosh = pygame.mixer.Sound('sounds/Woosh-Mark_DiAngelo-4778593.wav')
catch = pygame.mixer.Sound('sounds/Ball_Bounce-Popup_Pixels-172648817.wav')
drop = pygame.mixer.Sound('sounds/Light Bulb Breaking-SoundBible.com-53066515.wav')
hi = pygame.mixer.Sound('sounds/Ta Da-SoundBible.com-1884170640.wav')

#Function to redraw everything in game window
def redraw_game_window():
    global hiScoreOld  #Old hi-score variable
    pygame.Surface.fill(win,(255,255,255)) #Keep background white
    #Scores Text
    scores = [font.render(str(score), 1, (0,0,0)),\
              font.render(str(hiScore), 1, (0,0,0)),\
              font.render(str(score2), 1, (0,0,0))]

    c = 1
    if play == 0:
        #Print instructions before game starts
        for i in instructions:
            j = font3.render(i, 1, (0,0,0))
            win.blit(j, (win_x // 2 - 2.7*len(i), 23 * c + 10))
            c += 1
    elif play == 2:
        win.blit(inst[2], (win_x // 2 - 60, win_y // 2 - 20))
        win.blit(inst[4], (win_x // 2 - 140, win_y // 2 + 10))
    elif play == 4:
        win.blit(inst[3], (win_x // 2 - 60, win_y // 2 - 20))
        win.blit(inst[4], (win_x // 2 - 140, win_y // 2 + 10))

    #Render the score text on screen
    win.blit(text[0], (10,10))
    win.blit(scores[0], (50, 10))
    win.blit(text[1], (win_x // 2 - 60, 10))
    win.blit(scores[1], (win_x // 2 + 50, 10))
    win.blit(text[2], (win_x - 100, 10))
    win.blit(scores[2], (win_x - 60, 10))

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
        #Display messages
        win.blit(gameOver, (win_x // 2 - 180, win_y - 400))
        if int(hiScoreOld) < hiScore:
            #If hi-score is more than old hi-score, display message
            win.blit(hiSc, (win_x // 2 - 100, win_y - 300))
        win.blit(inst[0], (win_x // 2 - 140, win_y - 250))
        win.blit(inst[1], (win_x // 2 - 100, win_y - 200))
    elif gameOv == 2:
        #Display this message if player hits ESC
        win.blit(gameOver, (win_x // 2 - 180, win_y - 400))
    elif gameOv == 3:
        #Display this message if player 1 wins 2-player game
        win.blit(text[3], (win_x // 2 - 40, win_y - 300))
        win.blit(inst[0], (win_x // 2 - 140, win_y - 250))
        win.blit(inst[1], (win_x // 2 - 100, win_y - 200))
    elif gameOv == 4:
        #Display this message if player 2 wins 2-player game
        win.blit(text[4], (win_x // 2 - 40, win_y - 300))
        win.blit(inst[0], (win_x // 2 - 140, win_y - 250))
        win.blit(inst[1], (win_x // 2 - 100, win_y - 200))
    elif gameOv == 5:
        #Display this message if player 1 wins 2-player game with high score
        win.blit(text[5], (win_x // 2 - 140, win_y - 300))
        win.blit(inst[0], (win_x // 2 - 140, win_y - 250))
        win.blit(inst[1], (win_x // 2 - 100, win_y - 200))
    elif gameOv == 6:
        #Display this message if player 2 wins 2-player game with high score
        win.blit(text[6], (win_x // 2 - 140, win_y - 300))
        win.blit(inst[0], (win_x // 2 - 140, win_y - 250))
        win.blit(inst[1], (win_x // 2 - 100, win_y - 200))
                
    pygame.display.update()#keep updating display

#End function

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

#Play intro sound
intro.play()

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
                    if play == 1 or play == 3:
                        score += 10 #Increase score if ball is caught
                    else:
                        score2 += 10
                    catch.play() #Play caught sound
                    ball.caughtBall(True) #Change side of ball caught
                    whoosh.play() #Play whoosh sound
                elif ball.getCoords()[0] + 8 >= hands[1].x\
                and ball.getCoords()[0] + 8 <= hands[1].x+32:
                    if play == 1 or play == 3:
                        score += 10
                    else:
                        score2 += 10
                    catch.play() 
                    ball.caughtBall(False)
                    whoosh.play()
                else:
                    #Game is over if one of the balls is fallen
                    if play == 1:
                        #One-player game over
                        gameOv = 1
                        play = 6 #Explicitly stop game
                        for z in balls:
                            z.visibility = False #Remove balls
                        if hiScore < score:
                            hi.play() #play hi-score sound
                            hiScore = score#Update Hi-Score
                            #Update high-score in log
                            with open("hiScoreLog.txt", mode='a') as h:
                                h.write(str(hiScore) + '\n')
                        else:
                            drop.play() #Play drop sound
                    elif play == 3:
                        #Player 1's game ends, so move on to player 2
                        play = 4
                        for z in balls:
                            z.visibility = False #Remove balls
                        drop.play()
                    else:
                        #Player 2's game ends.  Output appropriate message
                        #depending on which player wins
                        play = 6
                        for z in balls:
                            z.visibility = False #Remove balls

                        if score > score2:
                            if score > hiScore:
                                gameOv = 5 #Player 1 got high score
                                #Record new high score in log
                                hi.play() 
                                hiScore = score
                                with open("hiScoreLog.txt", mode='a') as h:
                                    h.write(str(hiScore) + '\n')
                            else:
                                gameOv = 3 #Player 1 wins, no hi score
                                drop.play()
                        else:
                            if hiScore < score2:
                                gameOv = 6 #Player 2 got high score
                                hi.play()
                                hiScore = score2
                                with open("hiScoreLog.txt", mode='a') as h:
                                    h.write(str(hiScore) + '\n')
                            else:
                                drop.play() #Play drop sound
                                gameOv = 4 #Player 2 wins, no hi score
                            
    #Check score to add other ball
    if score == 100 or score2 == 100:
        ball3.visibility = True

    #Check if player quits game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()#Create variable handle for key presses

    #Take input from player's keyboard
    #Possible key presses are left, right, 1, 2, space and escape
    #Left = move arms left
    #Right = move arms right
    #Escape = end game (get "game over" screen)
    #1, 2 = Starts new game (counter controlled)
    #Space = Begins game session

    if keys[pygame.K_1]:
        if play == 0 or play == 6:
            #User starts 1-player game
            gameOv = 0 #Reset game-over condition
            play = 1 #Reset play condition
            score = 0 #Reset score for Player 1
            score2 = 0 #Reset score for Player 2

            #Reset arms
            c = 0
            d = 0
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            hands[0].x = l_arm.getCoords()[3][0]-16
            hands[0].y = l_arm.getCoords()[3][1]-32
            hands[1].x = r_arm.getCoords()[3][0]-16
            hands[1].y = r_arm.getCoords()[3][1]-32
            
            #Reset balls' coordinates, angles and visibilities
            ball1.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball2.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball3.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball1.caughtBall(False)
            ball2.caughtBall(False)
            ball3.caughtBall(False)
            ball1.visibility = True
            ball2.visibility = True
            ball3.visibility = False

            with open("hiScoreLog.txt") as h:
                #Read old high-score into variable from log
                for line in h:
                    hiScoreOld = line


            #Play whoosh sound
            whoosh.play()

    elif keys[pygame.K_2]:
        if play == 0 or play == 6:
            #User starts 2-player game
            gameOv = 0 #Reset game-over condition
            play = 2 #Reset play condition
            score = 0
            score2 = 0 

    if keys[pygame.K_SPACE]:
        #Space gets pressed
        #Start game in 2-player mode for either Player 1 or 2
        if play == 2:
            play = 3 #Start Player 1 game when user hits space

            with open("hiScoreLog.txt") as h:
                for line in h:
                    hiScoreOld = line
                
            c = 0
            d = 0
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            hands[0].x = l_arm.getCoords()[3][0]-16
            hands[0].y = l_arm.getCoords()[3][1]-32
            hands[1].x = r_arm.getCoords()[3][0]-16
            hands[1].y = r_arm.getCoords()[3][1]-32
            
            ball1.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball2.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball3.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball1.caughtBall(False)
            ball2.caughtBall(False)
            ball3.caughtBall(False)
            ball1.visibility = True
            ball2.visibility = True
            ball3.visibility = False

            whoosh.play()
        elif play == 4:
            play = 5 #Start Player 2 game when user hits space
            c = 0
            d = 0
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            hands[0].x = l_arm.getCoords()[3][0]-16
            hands[0].y = l_arm.getCoords()[3][1]-32
            hands[1].x = r_arm.getCoords()[3][0]-16
            hands[1].y = r_arm.getCoords()[3][1]-32
            
            ball1.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball2.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball3.setCoord(man.x + 32, man.y + 32, pi / 2)
            ball1.caughtBall(False)
            ball2.caughtBall(False)
            ball3.caughtBall(False)
            ball1.visibility = True
            ball2.visibility = True
            ball3.visibility = False

            whoosh.play()
            
    if keys[pygame.K_LEFT]:
        #Left key gets pressed
        #Extend left arm and contract right arm
        if play == 1 or play == 3 or play == 5:
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
        if play == 1 or play == 3 or play == 5:
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
        play = 6 #Also stop game explicitly
        run = False
    else:
        pass

    redraw_game_window() #Recall the redraw function if game playing

pygame.mixer.quit() #stop mixer
pygame.quit()#end pygame session
