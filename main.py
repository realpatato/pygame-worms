''' MAIN FILE - HANDLES MAIN GAME LOOP '''
''' IMPORTS '''
#needed for visual aspects of the game
import pygame #must be version 2.0, make sure to update before doing anything else
#needed for creating levels
import level_manager as lm
#needed for explosions
import explosion as ex

#initializes the pygame module
pygame.init()

''' SCREEN SETUP '''
#variables for screen size
screen_width = 1000
screen_height = 750

#creates the screen with width and height
screen = pygame.display.set_mode((screen_width, screen_height))

#sets the caption for the window
pygame.display.set_caption("Worms")

''' LOOP '''
#variable to control loop
keep_playing = True

#clock to manage framerate
clock = pygame.time.Clock()

#loading and scaling the background
background = pygame.image.load("levels/worm-level.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

#creates a level object with the background image and screen
level = lm.Level(background, screen)

explosions = []

clicked_and_touched = False

while keep_playing:
    #check for pgame events
    for event in pygame.event.get():
        #check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            #get the mouse position
            mouse_pos = pygame.mouse.get_pos()
            #get the mouse object for checking which button
            mouse_button = pygame.mouse.get_pressed()
            #checks if the left mouse button was clicked (temp)
            if mouse_button[0]:
                #creates an explosion at the mouse position (also temp)
                explosions.append(ex.Explosion(40, mouse_pos[0], mouse_pos[1]))
        #check for quit
        if event.type == pygame.QUIT:
            #set control variable to false
            keep_playing = False
    
    #fills the screen with black
    screen.fill((94,120,157))

    #draws the level
    level.draw_self()

    for explosion in explosions:
        explosion.explode(level, screen)
        try:
            explosions.remove(explosion)
        except:
            pass

    #updates the screen
    pygame.display.update()

    #sets the frame rate
    clock.tick(60)

''' ENDING THE PROGRAM '''
#quits the window
pygame.quit()
#ends the program
quit()