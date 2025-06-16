''' MAIN FILE - HANDLES MAIN GAME LOOP '''
''' IMPORTS '''
#needed for visual aspects of the game
import pygame

#initializes the pygame module
pygame.init()

''' SCREEN SETUP '''
#variables for screen size
screen_width = 1000
screen_height = 500

#creates the screen with width and height
screen = pygame.display.set_mode((screen_width, screen_height))

#sets the caption for the window
pygame.display.set_caption("Worms")

''' LOOP '''
#variable to control loop
keep_playing = True

#clock to manage framerate
clock = pygame.time.Clock()

background = pygame.image.load("levels/worm-level.png")
background = pygame.transform.scale(background, (1000, 500))
background_mask = pygame.mask.from_surface(background)
masks = background_mask.connected_components()
outlines_list = []
for mask in masks:
    outlines_list.append(mask.outline())

while keep_playing:
    #check for pgame events
    for event in pygame.event.get():
        #check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            #get the mouse position
            mouse_pos = pygame.mouse.get_pos()
            for i in range(0, len(masks)):
                #ensures it starts at the very end, and goes to the front
                index = 0 - (i + 1)
                #gets the object from the list with index
                enemy_object = masks[index]
                #checking for where the mouse is in the sprite rect
                pos_in_enemy_mask = (mouse_pos[0] - enemy_object.get_rect().x, mouse_pos[1] - enemy_object.get_rect().y)
                #checks if the mouse is with the sprite basically
                if enemy_object.get_rect().collidepoint(*mouse_pos) and enemy_object.get_at(pos_in_enemy_mask):
                    print("CLICK")
        #check for quit
        if event.type == pygame.QUIT:
            #set control variable to false
            keep_playing = False
    
    #fills the screen with black
    screen.fill((0, 0, 0))
    
    screen.blit(background, (0, 0))
    for mask in outlines_list:
        pygame.draw.polygon(screen, (255, 0, 0), mask, 2)

    #updates the screen
    pygame.display.update()

    #sets the frame rate
    clock.tick(60)

''' ENDING THE PROGRAM '''
#quits the window
pygame.quit()
#ends the program
quit()