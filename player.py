import pygame
from pygame import mixer
import math
from bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.radius = 25
        self.sprite_sheet = pygame.image.load('images/spritejoueur.png')
        self.image = self.get_image(56, 0)
        self.image_rotated = self.image
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.old_position = self.position.copy()
        self.images = {'hand' : self.get_image(0,0),
                       'pistol' : self.get_image(56,0),
                       'smg' : self.get_image(112,0)}
        self.munition = 50
        self.pistol_magazine = 0
        self.smg_magazine = 0
        self.weapon_name = "pistol"
        self.cool_down_count = 0
        self.cool_down_regen = 0
        self.player_kill = False
        self.coin = 0
        self.health = 5
        self.score = 0
        self.filtre = 0
        self.reload_sound = mixer.Sound('son/reload.wav')
        self.weapon = self.pistol()

    def get_position(self):
        '''récupère la position du joueur'''
        return [self.position[0], self.position[1]]

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self): self.position[0] += 3

    def move_left(self): self.position[0] -= 3

    def move_up(self): self.position[1] -= 3

    def move_down(self): self.position[1] += 3

    def update(self):
        '''met à jour le sprite'''
        posMouseX = pygame.mouse.get_pos()[0]
        posMouseY = pygame.mouse.get_pos()[1]
        deltaY = posMouseY - self.position[1]
        deltaX = posMouseX - self.position[0]
        angleInDegrees = math.atan2(deltaY , deltaX) * 180 / math.pi
        angleInDegrees = angleInDegrees + 90

        self.rect.topleft = self.position
        self.image = pygame.transform.rotozoom(self.image_rotated, -angleInDegrees, 1)
        self.rect = self.image.get_rect(center = self.position)
        self.image.set_colorkey([0, 0, 0])

        if self.regen_auto():
            self.health += 1

        if self.health == 5:
            self.filtre = 0
        elif self.health == 4:
            self.filtre = 10
        elif self.health == 3:
            self.filtre = 20
        elif self.health == 2:
            self.filtre = 30
        elif self.health == 1:
            self.filtre = 40

    def move_back(self):
        '''Replace le joueur à son ancienne position si il atteint une zone de collision'''
        self.position = self.old_position
        self.rect.center = self.position

    def get_image(self, x, y):
        '''dessine le srite'''
        image = pygame.Surface([55, 130])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 55, 130))

        return image


    def cooldown_shoot(self, delai):
        if self.cool_down_count >= delai:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def can_shoot(self):
        self.cooldown_shoot(self.delai)
        if self.weapon_name == "smg":
            return self.smg_magazine > 0 and self.cool_down_count == 0
        elif self.weapon_name == "pistol":
            return self.pistol_magazine > 0 and self.cool_down_count == 0

    def create_bullet(self):
        '''apelle une bullet'''
        self.bullet_sound.play()
        return Bullet(self.position[0], self.position[1])

    def remove_bullet_magazine(self):
        if self.weapon_name == "pistol":
            self.pistol_magazine -= 1
            self.cool_down_count = 1
        elif self.weapon_name == "smg":
            self.smg_magazine -= 1
            self.cool_down_count = 1


    def change_weapon(self, skin):
        '''change le skin selon l'arme'''
        self.image = self.images[skin]
        self.image.set_colorkey([0, 0, 0])
        self.image_rotated = self.image

    def pistol(self):
        '''capacité du chargeur'''
        self.capacity_max = 7
        self.weapon_name = "pistol"
        self.delai = 20
        self.bullet_sound = mixer.Sound('son/tir.wav')


    def smg(self):
        '''capacité du chargeur'''
        self.capacity_max = 20
        self.weapon_name = "smg"
        self.delai = 10
        self.bullet_sound = mixer.Sound('son/tir.wav')

    def hand(self):
        '''capacité du chargeur'''
        self.weapon_choose("hand")
        self.capacity_max = 0
        self.magazine = 0

    def weapon_choose(self, weapon):
        if weapon == "pistol":
            res = self.pistol_magazine
        elif weapon == "smg":
            res = self.smg_magazine
        else:
            res = 0
        return res

    def reload(self):
        if self.weapon_name == "smg":
            while self.smg_magazine < self.capacity_max and self.munition > 0:
                self.smg_magazine += 1
                self.munition -= 1
        elif self.weapon_name == "pistol":
            while self.pistol_magazine < self.capacity_max and self.munition > 0:
                self.pistol_magazine += 1
                self.munition -= 1
        self.reload_sound.play()


    def get_coin(self):
        self.coin += 1

    def get_point(self):
        self.score += 1

    def buy_munition(self):
        if self.coin >= 5:
            self.munition += 10
            self.coin -= 5
            self.buy_sound = mixer.Sound('son/buy.wav')
            self.buy_sound.play()

    def cooldown_regen(self):
        if self.cool_down_regen >= 150:
            self.cool_down_regen = 0
        else:
            self.cool_down_regen += 1

    def regen_auto(self):
        if self.health < 5:
            self.cooldown_regen()
            return self.cool_down_regen == 0

    def health_display(self):
        if self.health == 5:
            res = (249,228,183)
        elif self.health == 4:
            res = (255,153,153)
        elif self.health == 3:
            res = (255,102,102)
        elif self.health == 2:
            res = (255, 53, 53)
        elif self.health == 1:
            res = (255, 0, 0)
        return res