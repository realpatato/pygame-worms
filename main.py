''' MAIN FILE - HANDLES MAIN GAME LOOP '''
''' IMPORTS '''
#needed for visual aspects of the game
import pygame
import pygame.mask #must be version 2.0, make sure to update before doing anything else
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
            #gets the list of masks in the level
            foreground_masks = level._foreground._masks
            #iterates over each mask
            for i in range(0, len(foreground_masks)):
                #ensures it starts at the very end, and goes to the front
                index = 0 - (i + 1)
                #gets the specific part of the level
                level_part = foreground_masks[index]
                #checking for where the mouse is in the level part rect
                pos_in_enemy_mask = (mouse_pos[0] - level_part.get_rect().x, mouse_pos[1] - level_part.get_rect().y)
                #checks if the mouse is within the level part basically
                if level_part.get_rect().collidepoint(*mouse_pos) and level_part.get_at(pos_in_enemy_mask):
                    print(mouse_pos)
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
        level_parts_masks = level._foreground._masks
        level_parts_rects = level._foreground._rects
        for i in range(len(level_parts_masks)):
            level_part = level_parts_masks[i]
            empty_surface = pygame.Surface((level_parts_rects[i].width, level_parts_rects[i].height), pygame.SRCALPHA)
            overlap_mask = explosion._mask.overlap_mask(level_parts_masks[i], (level_parts_rects[i].x - explosion._rect.x, level_parts_rects[i].y - explosion._rect.y))
            overlap_mask_surface = overlap_mask.to_surface(surface=empty_surface, unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255), dest=(explosion._rect.x, explosion._rect.y))
            screen.blit(overlap_mask_surface, (level_parts_rects[i].x, level_parts_rects[i].y))
            pygame.draw.rect(screen, (255, 0, 0), level_parts_rects[i], 2)
            pygame.draw.rect(screen, (255, 0, 0), empty_surface.get_rect(), 2)
            #screen.blit(level_part.to_surface(unsetcolor=(0, 0, 0, 0)), (0, 0))
        '''
        for level_part in level._foreground._masks:
            empty_surface = pygame.Surface((level_part.get_rect().x, level_part.get_rect().y))
            overlap_mask = explosion._mask.overlap_mask(level_part, (level_part.get_rect().x - explosion._rect.x, level_part.get_rect().y - explosion._rect.y))
            overlap_mask_surface = overlap_mask.to_surface(surface=empty_surface, unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255))
            if clicked_and_touched == False:
                overlap_mask_pixels = pygame.PixelArray(overlap_mask_surface)
                print(overlap_mask_pixels)
                del overlap_mask_pixels
                clicked_and_touched = True
            print(empty_surface)
            print(empty_surface.get_rect())
            print(overlap_mask_surface)
            screen.blit(overlap_mask_surface, (explosion._rect.x, explosion._rect.y))
            pygame.draw.rect(screen, (255, 0, 0), overlap_mask.get_rect())
            '''
            
    #updates the screen
    pygame.display.update()

    #sets the frame rate
    clock.tick(60)

''' ENDING THE PROGRAM '''
#quits the window
pygame.quit()
#ends the program
quit()