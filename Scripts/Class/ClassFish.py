##########################################################
# Please don't edit this file or the game won't launch ! #
##########################################################

import pygame
import random

class Poisson(pygame.sprite.Sprite):
    def __init__(self, fish_right):
        super().__init__()
        self.image = fish_right
        self.rect = self.image.get_rect()  # Adapte le taille du personnage a la taille de l'image.
        self.velocity = [0, 0]
        self.is_fish = True
        self.remaining_time = 0
        self.direction = "right"
        self.direction_y = "up"
        self.time_to_move = 0
        self.is_evil = False
        self.rect.y = random.randint(20, 700)

    def update(self):
        self.rect.move_ip(*self.velocity)

    def kill(self):
        self.image = no_texture

    def change_texture(self, texture):
        self.image = texture

    def bouger_aleatoirement(self):
        self.rect.x = random.randint(0, 1280)
        self.rect.y = random.randint(0, 720)
        if random.randint(0, 3) > 1.4:
            self.direction = "left"
        else:
            self.direction = "right"

    def changer_x(self, xvar):
        self.rect.x = xvar

    def obtenir_x(self):
        return self.rect.x