import pygame
from Inventory import Inventory
from Score import Score


class UserInterface:
    def __init__(self, mun, coin, smg_mag, pistol_mag, vague):
        self.color_red = (255, 0, 0)
        self.color_green = (0, 255, 0)
        self.color_blue = (0, 0, 255)
        self.color_black = (0, 0, 0)
        self.color_white = (255, 255, 255)

        self.smallfont = pygame.font.SysFont("Verdana", 12)
        self.regularfont = pygame.font.SysFont("Verdana", 20)
        self.largefont = pygame.font.SysFont("Verdana", 40)

        self.inventory = Inventory(mun, coin, smg_mag, pistol_mag)

        self.text = self.regularfont.render("point : ", True, self.color_black)
        self.score = self.regularfont.render("0", True, self.color_black)
        self.vague = self.regularfont.render(str("vague :"), True, self.color_black)
        self.aide = self.smallfont.render(str("vous pouvez appuyer sur C pour acheter des munitions"), True, self.color_black)
        self.num_vague = self.regularfont.render(str(vague-1), True, self.color_black)
        self.no_mun = False
    
    def render(self, screen):
        self.inventory.render(screen)
        screen.blit(self.text, (660, 15))
        screen.blit(self.score, (740, 15))
        screen.blit(self.vague, (660, 45))
        screen.blit(self.num_vague, (740, 45))
        if self.no_mun == True:
            screen.blit(self.aide, (200, 700))

    def update(self, mun, coin, point,smg_mag, pistol_mag, vague):
        self.inventory = Inventory(mun, coin, smg_mag, pistol_mag)
        new_point = point
        self.text = self.regularfont.render(str("point :"), True, self.color_black)
        self.score = self.regularfont.render(str(point), True, self.color_black)
        self.vague = self.regularfont.render(str("vague :"), True, self.color_black)
        self.num_vague = self.regularfont.render(str(vague-1), True, self.color_black)
    

