''' EXPLOSION - HANDLES EXPLOSIONS '''
''' IMPORTS '''
#needed for the sprite class - giving a circle collider
import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, r, x, y):
        self.set_rect(r, x, y)
        self.set_sprite(r)
        self.set_mask()

    def set_sprite(self, r):
        sprite = pygame.image.load("sprites/circle.png")
        sprite = pygame.transform.scale(sprite, (r * 2, r * 2))
        self._sprite = sprite

    def set_mask(self):
        self._mask = pygame.mask.from_surface(self._sprite)
        self._draw_mask = self._mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255))

    def set_rect(self, r, x, y):
        self._rect = pygame.Rect(0, 0, r * 2, r * 2)
        self._rect.center = (x, y)
    
    def gen_overlap(self, level, screen):
        level_parts_masks = level._foreground._masks
        for i in range(len(level_parts_masks)):
            level_part = level_parts_masks[i]
            empty_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            overlap_mask = self._mask.overlap_mask(level_parts_masks[i], (level_part.get_rect().x - self._rect.x, level_part.get_rect().y - self._rect.y))
            return overlap_mask.to_surface(surface=empty_surface, unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255), dest=(self._rect.x, self._rect.y))

    def remove_pixels(self, level, overlap):
        overlap_pixels = pygame.PixelArray(overlap)
        level_pixels = pygame.PixelArray(level._foreground._img)
        for i in range(len(level_pixels)):
            for k in range(len(level_pixels[i])):
                if level_pixels[i][k] != 0 and overlap_pixels[i][k] != 0:
                    level_pixels[i][k] = pygame.Color(0, 0, 0, 0)
        del overlap_pixels
        del level_pixels
    
    def explode(self, level, screen):
        self.draw_self(screen)
        overlap = self.gen_overlap(level, screen)
        self.remove_pixels(level, overlap)
    
    def draw_self(self, surface):
        surface.blit(self._draw_mask, (self._rect.x, self._rect.y))