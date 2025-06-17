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
    
    def draw_self(self, surface):
        surface.blit(self._draw_mask, (self._rect.x, self._rect.y))