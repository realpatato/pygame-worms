''' LEVEL MANAGER - HANDLES LEVELS '''
''' IMPORTS '''
#needed for visual parts of level creation
import pygame

class Background:
    def __init__(self, img, surface):
        ''' Background Object - Stores the background image and draws itself '''
        self._img = img
        self._surface = surface
        self._background = self.generate_self()

    def generate_self(self):
        ''' Generates the background image '''
        #gets the mask of the image
        img_mask = pygame.mask.from_surface(self._img)
        #gets each piece of the mask (in the event that the image has gaps of trnasparency)
        all_masks = img_mask.connected_components()
        #creates an empty surface the size of the screen with a transparent background
        surface = pygame.Surface((self._surface.get_width(), self._surface.get_height()), pygame.SRCALPHA)
        #draws the image on the surface
        surface.blit(self._img, (0, 0))
        #iterates over each of the mask segments
        for mask in all_masks:
            #draws the section over the image on the surface
            surface.blit(mask.to_surface(setcolor=(50, 50, 50, 245), unsetcolor=(0,0,0,0)), (0, 0))
        #returns the surface
        return surface
    
    def draw_self(self):
        ''' Draws the background on the screen '''
        self._surface.blit(self._background, (0, 0))

class Foreground:
    def __init__(self, img, surface):
        ''' Foreground Object - Stores the image and the collision '''
        self._img = img
        self._surface = surface
        mask = pygame.mask.from_surface(self._img) 
        self._masks = mask.connected_components()
        self._rects = mask.get_bounding_rects()
    
    def draw_self(self):
        ''' Draws the foreground to the screen '''
        self._surface.blit(self._img, (0, 0))

class Level:
    def __init__(self, img, surface):
        ''' Level Object - Stores the foreground and background '''
        self._background = Background(img, surface)
        self._foreground = Foreground(img, surface)

    def draw_self(self):
        ''' Draws the level '''
        self._background.draw_self()
        self._foreground.draw_self()