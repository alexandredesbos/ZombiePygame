import pygame
import math


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.radius = 20
        self.sprite_sheet = pygame.image.load('images/zombie.png')
        self.image = pygame.transform.scale(self.sprite_sheet, (40, 48))
        self.image_rotated = self.image
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.change_position = [0, 0]
        self.old_position = self.position.copy()
        self.speed = 1
        self.cooldown = 0
        self.stuck = False

    def get_position(self):
        return [self.position[0], self.position[1]]

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self): self.change_position[0] += self.speed

    def move_left(self): self.change_position[0] -= self.speed

    def move_up(self): self.change_position[1] -= self.speed

    def move_down(self): self.change_position[1] += self.speed

    def update(self, player_x, player_y):
        self.rect.center = self.position
        self.follow_player(player_x,player_y)

    # Replace le sprite à son ancienne position si il atteind une zone de collision
    def move_back(self):
        self.position = self.old_position
        self.rect.center = self.position

    def get_image(self, x, y):
        image = pygame.Surface([64, 64])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 64, 64))
        return image

    def follow_player(self, player_x, player_y):
        #gère le mouvement du zombie, et sa rotation par rapport au joueur

        
        self.player_kill = False
        if self.get_position()[0] > player_x:
            self.move_left()
        elif self.get_position()[0] < player_x:
            self.move_right()
        if self.get_position()[1] > player_y:
            self.move_up()
        elif self.get_position()[1] < player_y:
            self.move_down()

        self.position[0] += self.change_position[0]
        self.position[1] += self.change_position[1]
        self.change_position = [0, 0]
        
        if self.get_position()[0] == player_x or self.get_position()[1]:
            self.player_kill = True

        #calcul d'angle pour faire tourner le sprite
        playerX = player_x
        playerY = player_y
        deltaX = playerX - self.get_position()[0]
        deltaY = playerY - self.get_position()[1]
        
        aglD = math.atan2(deltaY , deltaX) * 180 / math.pi
        aglD = aglD + 90

        self.rect.topleft = self.position
        self.image = pygame.transform.rotozoom(self.image_rotated, -aglD, 1)
        self.rect = self.image.get_rect(center = (self.position))
        self.image.set_colorkey([255, 255, 255])


    def touche(self):
        self.kill()

    def tempo(self):
        #méthode pour temporiser entre chaque coup de poing de zombie
        if self.cooldown >= 50:
            self.cooldown = 0
        elif self.cooldown > 0:
            self.cooldown += 1


   
        
        

        
