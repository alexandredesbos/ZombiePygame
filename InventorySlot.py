import pygame

class InventorySlot:
    def __init__(self, name, pos, count):
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.count = count

        self.font = pygame.font.Font("Fonts/Frostbite.ttf", 25)

    def render(self, screen):
        text = self.font.render(str(self.count), True, (0,0,0))
        screen.blit(self.image, self.rect)
        screen.blit(text, self.rect.midright)




