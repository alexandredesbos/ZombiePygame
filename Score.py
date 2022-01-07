import pygame

class Score():
    def __init__(self, val=0):
        
        self._position = [x, y]
        self._value = val

    def show(self, value, position):
        score_afficher = myfont.render(str(score), 1, (255,0,0))
        screen.blit(score_afficher, (position[0], position[1]))

    def edit(self, points = 1):
        '''Modifie le score existant d'un nombre de point'''
        try:
            self.value += points
        except:
            print("Paramètre(s) non-reconnus ou hors plage")
    
    def reset(self):
        '''Réinitialise le score à 0'''
        self.value = 0;
