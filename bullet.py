import pygame
from PIL import Image
import math


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        '''x et y la position de la balle '''
        super().__init__()
        self.radius = 5
        self.pos = [x, y]
        self.image = pygame.image.load('images/round_bullet.png')
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.bullet_state = "ready"
        self.dir = self.parametre_tir()

    def reset_position(self, pos):
        self.position = pos.copy()
        self.old_position = self.position.copy()

    def save_location(self): self.old_position = self.position.copy()

    def update(self):
        px = self.pos[0]
        py = self.pos[1]

        px += 6 * self.vector[0]
        py += 6 * self.vector[1]
        self.pos = [px, py]
        self.rect.topleft = self.pos

        # Disparition de la balle si elle sort de l'écran
        if self.rect.topleft[0] > 800 or self.rect.topleft[0] < 0 or self.rect.topleft[1] > 800 or self.rect.topleft[1] < 0:
            self.kill()

    def rotate(self, img, rect, angle):
        self.rot_image = pygame.transform.rotate(img, angle)
        return self.rot_image

    def parametre_tir(self):
        self.vector = self.vector_bullet()  # on recupère le vecteur de direction du tir

        # on reduit le vecteur au maximum
        if abs(self.vector[0]) > abs(self.vector[1]):
            i = abs(self.vector[0])
        else:
            i = abs(self.vector[1])

        self.vector = [self.vector[0] / i, self.vector[1] / i]
        return self.vector

    def vector_bullet(self):

        # On recupère la position de la balle
        posBulletX = self.pos[0]
        posBulletY = self.pos[1]

        # On recupère les coordonées du clic
        posMouseX = pygame.mouse.get_pos()[0]
        posMouseY = pygame.mouse.get_pos()[1]

        # On calcul le vecteur de direction de la balle
        vect = [posMouseX - posBulletX, posMouseY - posBulletY]
        return vect

    def touche(self):
        self.kill()