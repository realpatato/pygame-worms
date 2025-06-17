''' EXPLOSION - HANDLES EXPLOSIONS '''
''' IMPORTS '''
#needed for all of the collision stuff and pixel stuff
import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, r, x, y):
        ''' Explosion Object - Stores the mask of the explosion and the explosion functionality '''
        self.set_rect(r, x, y)
        self.set_sprite(r)
        self.set_mask()

    def set_sprite(self, r):
        ''' Sets the sprite for the explosion given a radius '''
        #loads in an image of a circle, uses this to store a surface, instead of drawing on one then storing that one
        sprite = pygame.image.load("sprites/circle.png")
        #scales the circle to the given radius (kinda, the edges of the image are not the edges of the circle)
        sprite = pygame.transform.scale(sprite, (r * 2, r * 2))
        #stores the sprite in a variable
        self._sprite = sprite

    def set_mask(self):
        ''' Sets the mask based on the sprite '''
        #creates a mask with the sprite surface
        self._mask = pygame.mask.from_surface(self._sprite)
        #creates a mask used only for drawing the explosion
        self._draw_mask = self._mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255))

    def set_rect(self, r, x, y):
        ''' Sets the rect of the explosion based on the radius, x, and y positions '''
        #creates a rect starting at 0, 0 that is double the radius in width and length
        self._rect = pygame.Rect(0, 0, r * 2, r * 2)
        #sets the center of the rect to x and y since thats where we want the explosion to come from
        self._rect.center = (x, y)
    
    def gen_overlap(self, level, screen):
        ''' Generates the overlap surface for the destruction '''
        #gets the masks of the level
        level_parts_masks = level._foreground._masks
        #creates an empty list for storing all of the overlaps - since there can be multiple parts
        overlaps = []
        #iterates over the masks of the level
        for i in range(len(level_parts_masks)):
            #sets the level part to the current mask
            level_part = level_parts_masks[i]
            #creates an empty surface for the overlap to be drawn on
            empty_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            #gets a mask of the overlap between the level and the explosion
            overlap_mask = self._mask.overlap_mask(level_parts_masks[i], (level_part.get_rect().x - self._rect.x, level_part.get_rect().y - self._rect.y))
            #puts that mask on the empty surface
            overlap_mask_surface = overlap_mask.to_surface(surface=empty_surface, unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255), dest=(self._rect.x, self._rect.y))
            #adds the surface to the list of overlaps
            overlaps.append(overlap_mask_surface)
        #returns a list of overlaps
        return overlaps

    def find_empty_overlaps(self, pixel_array):
        ''' Finds empty overlaps to prevent lag '''
        #iterates over each row in the pixel array
        for i in range(len(pixel_array)):
            #checks if the value has anything besides 0
            if len(set(pixel_array[i])) != 1:
                #returns true since there is an overlap
                return True
        #returns false since no overlap is there
        return False

    def remove_pixels(self, level, overlaps):
        ''' Removes pixels from the level '''
        #iterating over overlaps
        for overlap in overlaps:
            #gets the pixels of the overlaps
            overlap_pixels = pygame.PixelArray(overlap)
            #checks if there even is any overlap
            overlap_exist = self.find_empty_overlaps(overlap_pixels)
            #removes stuff if there is a overlap
            if overlap_exist:
                #gets the pixels of the level
                level_pixels = pygame.PixelArray(level._foreground._img)
                #iterates over the rows
                for i in range(len(level_pixels)):
                    #and the columns
                    for k in range(len(level_pixels[i])):
                        #checks if both pixels are not 0 - 0 is the value when there is nothing there
                        if level_pixels[i][k] != 0 and overlap_pixels[i][k] != 0:
                            #if the overlap matches, it removes the pixels by making it invisible
                            level_pixels[i][k] = pygame.Color(0, 0, 0, 0)
                #deletes the level pixels, to unlock them
                del level_pixels
            #deletes the overlap pixels, to unlock them
            del overlap_pixels

    def explode(self, level, screen):
        ''' Does the explosion '''
        #draws the circle representing the explosion
        self.draw_self(screen)
        #updates the display so you can see it
        pygame.display.update()
        #generates the overlaps
        overlaps = self.gen_overlap(level, screen)
        #removes the pixels of the level
        self.remove_pixels(level, overlaps)
        #updates the mask of the level
        level._foreground.set_masks()
    
    def draw_self(self, surface):
        surface.blit(self._draw_mask, (self._rect.x, self._rect.y))