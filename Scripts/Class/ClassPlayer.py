##########################################################
# Please don't edit this file or the game won't launch ! #
##########################################################

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, shark_right):
        super().__init__()
        self.image = shark_right
        self.rect = self.image.get_rect()  # Adapte la taille du personnage à la taille de l'image.
        self.velocity = [0, 0]
        self.rect.x = 640
        self.rect.y = 360
        self.vies = 4
        self.time_vies = 0
        self.anime_time = 8
        self.isAnimationFliped = 0
        self.waitBeforeClose = 0

    def update(self):
        self.rect.move_ip(*self.velocity)
        if self.rect.x > 1280 - self.rect.width:
            self.rect.x = 1280 - self.rect.width
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > 720 - self.rect.height:
            self.rect.y = 720 - self.rect.height
        if self.rect.y < 0:
            self.rect.y = 0

    def enlever_vies(self):
        if self.time_vies < 0.1:
            self.vies = self.vies - 1
            self.time_vies = 30

    def change_texture(self, texture):
        self.image = texture