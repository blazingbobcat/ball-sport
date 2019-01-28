#Ball sport v1.1
#by Josh Klipstein
#January 3, 2018

import pygame
from ball_player import *
from ball_ball_class import *
from math import *
pygame.init() #initialize pygame window
pygame.mixer.init() #intialize mixer

#Initialize window dimensions
win_x = 800
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
                "3rd ball appears after 100 points are achieved.",\
                "This game is for one player or two.",\
                "CONTROLS (for both players):", "Escape: Quit game",\
                "Space: Start game",\
                "Left Arrow: Move hands left", \
                "Right Arrow: Move hands right",\
                "To start one-player game, press 1.", \
                "To start two player game, press 2.",\
                "Press 1 or 2 for new game,",\
                "Or press ESC to quit.",\
                "Player 1!",\
                "Player 2!",\
                "One Player!",\
                "Press Space when ready"]

#Game text
text = ["Game Over!",\
        "New Hi-Score!",\
        "P1:",\
        "Hi-Score:",\
        "P2:",\
        "P1 wins!",\
        "P2 wins!",\
        "P1 wins with hi-score!",\
        "P2 wins with hi-score!",\
        "Oops!  Tie game!",\
        "Tie game, but with hi-score!"]

clock = pygame.time.Clock() #Initialize time variable
score = 0 #Score variable player 1
score2 = 0 #Score variable player 2
gameOv = 0 #variable to end game
play = 0 #counter for game playing
global hiScoreOld #variable to record hi-score from log
with open("hiScoreLog.txt") as h:
    #Read old high-score into variable from log
    for line in h:
        hiScoreOld = line
hiScore = int(hiScoreOld) #Hi-Score variable
c = 0
d = 0
time = 10 #time variable

#Font variables
font = pygame.font.SysFont('comicsans', 30, True, True)
font2 = pygame.font.SysFont('comicSans', 100, False, True)
font3 = pygame.font.SysFont('comicSans', 20, False, True)

#Render instructions to play or quit game
inst = [font.render(instructions[16], 1, (128,0,0)),\
        font.render(instructions[17], 1, (128,0,0)),\
        font.render(instructions[18], 1, (0,128,0)),\
        font.render(instructions[19], 1, (0,0,128)),\
        font.render(instructions[20], 1, (128,0,0)),\
        font.render(instructions[21], 1, (128,0,0))]

#Render game text
onScreen = [font2.render(text[0], 1, (128,0,0)),\
        font2.render(text[1], 1, (128,0,0)),\
        font3.render(text[2], 1, (0,128,0)),\
        font3.render(text[3], 1, (0,0,0)),\
        font3.render(text[4], 1, (0,0,128)),\
        font.render(text[5], 1, (0,128,0)),\
        font.render(text[6], 1, (0,0,128)),\
        font.render(text[7], 1, (0,128,0)),\
        font.render(text[8], 1, (0,0,128)),\
        font.render(text[9], 1, (0,0,0)),\
        font.render(text[10], 1, (0,0,0))]

#Initialize all sounds
intro = pygame.mixer.Sound('sounds/sms-alert-2-daniel_simon.wav')
whoosh = pygame.mixer.Sound('sounds/Woosh-Mark_DiAngelo-4778593.wav')
catch = pygame.mixer.Sound('sounds/Ball_Bounce-Popup_Pixels-172648817.wav')
drop = pygame.mixer.Sound('sounds/Light Bulb Breaking-SoundBible.com-53066515.wav')
hi = pygame.mixer.Sound('sounds/Ta Da-SoundBible.com-1884170640.wav')
tieGame = pygame.mixer.Sound('sounds/Sad_Trombone-Joe_Lamb-665429450.wav')

#Function to redraw everything in game window
def redraw_game_window():
    global hiScoreOld
    pygame.Surface.fill(win,(255,255,255)) #Keep background white

    #Scores Text
    scores = [font3.render(str(score), 1, (0,0,0)),\
              font3.render(str(hiScore), 1, (0,0,0)),\
              font3.render(str(score2), 1, (0,0,0)),\
                font3.render('{:.2e}'.format(score), 1, (0,0,0)),\
              font3.render('{:.2e}'.format(hiScore), 1, (0,0,0)),\
              font3.render('{:.2e}'.format(score2), 1, (0,0,0))]

    c = 1
    if play == 0:
        #Print instructions before game starts
        for i in range(16):
            j = font3.render(instructions[i], 1, (0,0,0))
            win.blit(j, (win_x // 2 - (j.get_width()/2), 23 * c + 10))
            c += 1
    elif play == 1:
        #Instructions for one-player game
        for z in balls:
            z.visibility = False #Make balls invisible again
        win.blit(inst[4], (win_x // 2 - (inst[4].get_width()/2), win_y // 2 - 20))
        win.blit(inst[5], (win_x // 2 - (inst[5].get_width()/2), win_y // 2 + 10))
    elif play == 3:
        for z in balls:
            z.visibility = False
        #Instructions for Player 1
        win.blit(inst[2], (win_x // 2 - (inst[2].get_width()/2), win_y // 2 - 20))
        win.blit(inst[5], (win_x // 2 - (inst[5].get_width()/2), win_y // 2 + 10))
    elif play == 5:
        for z in balls:
            z.visibility = False
        #Instructions for Player 2
        win.blit(inst[3], (win_x // 2 - (inst[3].get_width()/2), win_y // 2 - 20))
        win.blit(inst[5], (win_x // 2 - (inst[5].get_width()/2), win_y // 2 + 10))
    elif play == 7:
        for z in balls:
            z.visibility = False #Game is stopped here

    #Render the score text on screen.  If any score is over 1000, render
    #all scores using scientific notation
    if score > 1000 or score2 > 1000:
        win.blit(onScreen[2], (10, 10))
        win.blit(scores[3], (onScreen[2].get_width()+10, 10))
        win.blit(onScreen[3], (win_x // 2 - (onScreen[3].get_width() / 2), 10))
        win.blit(scores[4], (win_x // 2 + (onScreen[3].get_width() / 2) + 2, 10))
        win.blit(onScreen[4], (win_x - 100, 10))
        win.blit(scores[5], (win_x - 77, 10))
    else:
        win.blit(onScreen[2], (10, 10))
        win.blit(scores[0], (onScreen[2].get_width()+10, 10))
        win.blit(onScreen[3], (win_x // 2 - (onScreen[3].get_width() / 2), 10))
        win.blit(scores[1], (win_x // 2 + (onScreen[3].get_width() / 2) + 2, 10))
        win.blit(onScreen[4], (win_x - 50, 10))
        win.blit(scores[2], (win_x - 28, 10))

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
        win.blit(onScreen[0], (win_x // 2 - (onScreen[0].get_width()/2), win_y - 400))
        if int(hiScoreOld) < hiScore:
            #If hi-score is more than old hi-score, display message
            win.blit(onScreen[1], (win_x // 2 - (onScreen[1].get_width()/2), win_y - 300))
            win.blit(inst[0], (win_x // 2 - (inst[0].get_width()/2), win_y - 170))
            win.blit(inst[1], (win_x // 2 - (inst[1].get_width()/2), win_y - 130))
        else:
            #If hi-score is less than old hi-score, just display instructions
            win.blit(inst[0], (win_x // 2 - (inst[0].get_width()/2), win_y - 250))
            win.blit(inst[1], (win_x // 2 - (inst[1].get_width()/2), win_y - 200))
    elif gameOv == 2:
        #Display this message if player hits ESC
        win.blit(onScreen[0], (win_x // 2 - (onScreen[0].get_width()/2), win_y - 400))
    elif gameOv == 3:
        #Display this message if player 1 wins 2-player game
        win.blit(onScreen[5], (win_x // 2 - (onScreen[5].get_width()/2), win_y - 300))
        win.blit(inst[0], (win_x // 2 - (inst[0].get_width()/2), win_y - 250))
        win.blit(inst[1], (win_x // 2 - (inst[1].get_width()/2), win_y - 200))
    elif gameOv == 4:
        #Display this message if player 2 wins 2-player game
        win.blit(onScreen[6], (win_x // 2 - (onScreen[6].get_width()/2), win_y - 300))
        win.blit(inst[0], (win_x // 2 - (inst[0].get_width()/2), win_y - 250))
        win.blit(inst[1], (win_x // 2 - (inst[1].get_width()/2), win_y - 200))
    elif gameOv == 5:
        #Display this message if player 1 wins 2-player game with high score
        win.blit(onScreen[7], (win_x // 2 - (onScreen[7].get_width()/2), win_y - 300))
        win.blit(inst[0], (win_x // 2 - (inst[0].get_width()/2), win_y - 250))
        win.blit(inst[1], (win_x // 2 - (inst[1].get_width()/2), win_y - 200))
    elif gameOv == 6:
        #Display this message if player 2 wins 2-player game with high score
        win.blit(onScreen[8], (win_x // 2 - (onScreen[8].get_width()/2), win_y - 300))
        win.blit(inst[0], (win_x // 2 - (inst[0].get_width()/2), win_y - 250))
        win.blit(inst[1], (win_x // 2 - (inst[1].get_width()/2), win_y - 200))
    elif gameOv == 7:
        #Display this message if score is tied in the end
        win.blit(onScreen[9], (win_x // 2 - (onScreen[9].get_width()/2), win_y - 300))
        win.blit(inst[0], (win_x // 2 - (inst[0].get_width()/2), win_y - 250))
        win.blit(inst[1], (win_x // 2 - (inst[1].get_width()/2), win_y - 200))
    elif gameOv == 8:
        #Display this message if score is tied, but there is new hi-score
        win.blit(onScreen[10], (win_x // 2 - (onScreen[10].get_width()/2), win_y - 300))
        win.blit(inst[0], (win_x // 2 - (inst[0].get_width()/2), win_y - 250))
        win.blit(inst[1], (win_x // 2 - (inst[1].get_width()/2), win_y - 200))
                
    pygame.display.update()#keep updating display

#End function

#Function to reset the hands on arms every time arms move
def reset_hands(hands):
    hands[0].x = l_arm.getCoords()[3][0]-16
    hands[0].y = l_arm.getCoords()[3][1]-32
    hands[1].x = r_arm.getCoords()[3][0]-16
    hands[1].y = r_arm.getCoords()[3][1]-32

#End function

#Function to reset balls' visibilities at the beginning of each game
def reset_balls(balls):
    balls[0].visibility = True
    balls[1].visibility = True
    balls[2].visibility = False
    
#Create instance of player
man = player(win_x // 2 - 32, win_y - 100, 64, 64)

#Initialize balls and ball list
ball1 = ball(man.x + 26, man.y + 36, 12, 12, 102, 0)
ball2 = ball(man.x + 26, man.y + 36, 12, 12, 201.5, 1)
ball3 = ball(man.x + 26, man.y + 36, 12, 12, 301, 2)
balls = [ball1, ball2, ball3]

#Initialize all arm variables
l_arms = [arm([(man.x + 32, man.y + 42),
               (man.x + 32 - z * 50, man.y + 64),
             (man.x + 32 - z * 50, man.y + 64),
               (man.x + 32 - z * 100, man.y + 42)])
            for z in range(1, 4)]
r_arms = [arm([(man.x + 32, man.y + 42),
               (man.x + 32 + z * 50, man.y + 64),
             (man.x + 32 + z * 50, man.y + 64),
               (man.x + 32 + z * 100, man.y + 42)])
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
    #Begin game loop with clock using time variable 
    clock.tick(time)

    #Check if balls have fallen
    for ball in balls:
        if ball.visibility == True:
            if ball.getCoords()[1] + 12 >= hands[0].y:
                if ball.getCoords()[0] + 12 >= hands[0].x\
                and ball.getCoords()[0] + 12 <= hands[0].x+32:
                    if play == 2 or play == 4:
                        score += 10 #Increase score if ball is caught
                        #If score is a multiple of 200, increase speed of game
                        if score % 200 == 0:
                            time += 1
                    elif play == 6:
                        score2 += 10
                        if score2 % 200 == 0:
                            time += 1
                    catch.play() #Play caught sound
                    ball.caughtBall(True) #Change side of ball caught
                    whoosh.play() #Play whoosh sound
                elif ball.getCoords()[0] + 12 >= hands[1].x\
                and ball.getCoords()[0] + 12 <= hands[1].x+32:
                    if play == 2 or play == 4:
                        score += 10
                        if score % 200 == 0:
                            time += 1
                    elif play == 6:
                        score2 += 10
                        if score2 % 200 == 0:
                            time += 1
                    catch.play() 
                    ball.caughtBall(False)
                    whoosh.play()
                else:
                    #Game is over if one of the balls is fallen
                    if play == 2:
                        #One-player game over
                        gameOv = 1
                        play = 7 #Explicitly stop game
                        if hiScore < score:
                            hi.play() #play hi-score sound
                            hiScore = score#Update Hi-Score
                            #Update high-score in log
                            with open("hiScoreLog.txt", mode='a') as h:
                                h.write(str(hiScore) + '\n')
                        else:
                            drop.play() #Play drop sound
                    elif play == 4:
                        #Player 1's game ends, so move on to player 2
                        play = 5
                        drop.play()
                    elif play == 6:
                        #Player 2's game ends.  Output appropriate message
                        #depending on which player wins
                        play = 7

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
                        elif score < score2:
                            if hiScore < score2:
                                gameOv = 6 #Player 2 got high score
                                hi.play()
                                hiScore = score2
                                with open("hiScoreLog.txt", mode='a') as h:
                                    h.write(str(hiScore) + '\n')
                            else:
                                drop.play() #Play drop sound
                                gameOv = 4 #Player 2 wins, no hi score
                        else:
                            if hiScore < score:
                                gameOv = 8 #Scores are equal, but new hi-score
                                hi.play() #Play hi-score sound effect
                                hiScore = score
                                with open("hiScoreLog.txt", mode='a') as h:
                                    h.write(str(hiScore) + '\n')
                            else:
                                #No hi-score.  Play the tie game sound effect
                                tieGame.play()
                                gameOv = 7
                            
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
        if play == 0 or play == 7:
            #User starts 2-player game
            gameOv = 0 #Reset game-over condition
            play = 1 #Reset play condition
            score = 0
            score2 = 0

    elif keys[pygame.K_2]:
        if play == 0 or play == 7:
            #User starts 2-player game
            gameOv = 0 #Reset game-over condition
            play = 3 #Reset play condition
            score = 0
            score2 = 0 

    if keys[pygame.K_SPACE]:
        #Space gets pressed
        #Start game in 2-player mode for either Player 1 or 2
        time = 10 #reset time variable
        if play == 1:
            play = 2 #Start Player 1 game when user hits space

            with open("hiScoreLog.txt") as h:
                for line in h:
                    hiScoreOld = line
                
            c = 0
            d = 0
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            reset_hands(hands)
            
            for b in balls:
                b.setCoord(man.x + 26, man.y + 36, pi / 2)
                b.caughtBall(False)
            reset_balls(balls) #Call function to reset balls' visibilities

            whoosh.play()
        elif play == 3:
            play = 4 #Player 1 starts in 2-player game when user hits space
            c = 0
            d = 0
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            reset_hands(hands)
            
            for b in balls:
                b.setCoord(man.x + 26, man.y + 36, pi / 2)
                b.caughtBall(False)
            reset_balls(balls)

            whoosh.play()

        elif play == 5:
            play = 6 #Player 2 starts
            c = 0
            d = 0
            l_arm = l_arms[c]
            r_arm = r_arms[d]
            reset_hands(hands)
            
            for b in balls:
                b.setCoord(man.x + 26, man.y + 36, pi / 2)
                b.caughtBall(False)
            reset_balls(balls)

            whoosh.play()
            
    if keys[pygame.K_LEFT]:
        #Left key gets pressed
        #Extend left arm and contract right arm
        if play == 2 or play == 4 or play == 6:
            if c < 2:
                # If left arm not extended, move left arm
                c += 1
                l_arm = l_arms[c] # Set new left-arm graphic
                if d > 0:
                    # If right arm fully extended, contract right arm
                    d = 0
                    r_arm = r_arms[d] # Set new right-arm graphic
                reset_hands(hands) # Reset hand graphics every time arms move
            
    elif keys[pygame.K_RIGHT]:
        #Right key gets pressed
        #Extend right arm and contract left
        if play == 2 or play == 4 or play == 6:
            if d < 2:
                # If right arm not extended, move right arm
                d += 1
                r_arm = r_arms[d] # Set new right-arm graphic
                if c > 0:
                    # If left arm fully extended, contract left arm
                    c = 0
                    l_arm = l_arms[c] # Set new left-arm graphic
                reset_hands(hands)
            
    elif keys[pygame.K_ESCAPE]:
        #Escape key quits game.  Flash game over screen if ESC is pressed
        gameOv = 2
        play = 7 #Also stop game explicitly
        run = False
    else:
        pass

    redraw_game_window() #Recall the redraw function if game playing

pygame.mixer.quit() #stop mixer
pygame.quit()#end pygame session
