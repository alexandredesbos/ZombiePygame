import pygame
from InventorySlot import InventorySlot

class Inventory:
    def __init__(self, mun, coin,smg_mag, pistol_mag):
        self.slots = []
        self.image = pygame.image.load("images/inventorybar.png")
        self.rect = self.image.get_rect()
        self.rect.topleft= (570, 710)

        self.slots.append(InventorySlot("images/coin.png",(580, 723), coin))
        self.slots.append(InventorySlot("images/gun.png",(620, 723), pistol_mag))
        self.slots.append(InventorySlot("images/machine-gun.png", (670, 723), smg_mag))
        self.slots.append(InventorySlot("images/munition.png",(715, 723), mun))


    def render(self, screen):
        screen.blit(self.image, self.rect)
        for slot in self.slots:
            slot.render(screen)
