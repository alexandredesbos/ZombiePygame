import pygame
import math
import random
import pygame_menu
from pygame import mixer


from bullet import Bullet
from player import Player
from enemies import Enemy
from userinterface import UserInterface



class Game:

    def __init__(self):

        # initialize the pygame
        pygame.init()

        # create the screen
        self.screenDim = (800, 800)
        self.screen = pygame.display.set_mode(self.screenDim, )

        # Title and icon
        pygame.display.set_caption("CMI-zombie")
        icon = pygame.image.load('images/zombie.png')
        pygame.display.set_icon(icon)

        # generate player
        self.player = Player(500,500)

        # generate the map
        self.map = pygame.image.load('images/map.png')

        # var

        self.numero_vague = 0
        self.vague_fini = True
        self.wait = "non appuyé"
        self.wall_radius = 25

        # user interface

        self.UI = UserInterface(self.player.munition, self.player.coin, self.player.smg_magazine, self.player.pistol_magazine, self.numero_vague)

        # Collision
        self.bullets = []
        self.walls = []

        #définition des cercles qui représente les mur
        for i in range(0,801, 800):
            for j in range(20,800, 20):
                self.walls.append([i, j])
        for i in range(0,801, 800):
            for j in range(20,800, 20):
                self.walls.append([j, i])
        self.walls.append([300,300])
        self.walls.append([320, 280])
        self.walls.append([340, 280])
        self.walls.append([360, 280])
        self.walls.append([380, 280])
        self.walls.append([400, 280])
        self.walls.append([420, 280])
        self.walls.append([440, 280])
        self.walls.append([470, 300])

        self.walls.append([605, 160])
        self.walls.append([625, 160])
        self.walls.append([640, 160])

        self.walls.append([606, 594])

        self.walls.append([130, 160])
        self.walls.append([145, 133])
        self.walls.append([160, 133])
        self.walls.append([175, 133])
        self.walls.append([200, 133])
        self.walls.append([220, 133])
        self.walls.append([240, 133])
        self.walls.append([275, 160])

        self.walls.append([380, 400])

        # calques
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()



        #######################initialisation Menu################################

        # Promo autres groupes
        self.secret = pygame_menu.Menu("Les jeux des CMI", self.screenDim[0], self.screenDim[1],
                                  theme=pygame_menu.themes.THEME_GREEN)
        path_groupe1 = "images/groupe1.png"
        path_groupe2 = "images/groupe2.png"
        self.secret.add.image(path_groupe1, scale=(self.screenDim[0] / 1280 * 0.5, self.screenDim[1] / 720 * 0.5))
        self.secret.add.image(path_groupe2, scale=(self.screenDim[0] / 1280 * 0.5, self.screenDim[1] / 720 * 0.5))
        # manque un moyen de quitter (W.I.P.)

        # Menu des options
        self.options = pygame_menu.Menu("options", self.screenDim[0], self.screenDim[1], theme=pygame_menu.themes.THEME_GREEN)
        self.options.add.range_slider('Musique', 50, (0, 100), 1, rangeslider_id="music", value_format=lambda x: str(int(x)))
        self.options.add.range_slider('Effets sonore', 50, (0, 100), 1, rangeslider_id="sfx",
                                 value_format=lambda x: str(int(x)))
        self.options.add.button('retour au jeu', self.start)
        self.options.add.button('Quitter le jeu', pygame_menu.events.EXIT)
        # manque un moyen de quitter (W.I.P.)

        # Menu shop
        self.shop = pygame_menu.Menu("Shop", self.screenDim[0], self.screenDim[1],
                                        theme=pygame_menu.themes.THEME_GREEN)
        self.shop.add.button('clic pour acheter 10 munitions supplémentaires', self.player.buy_munition)
        self.shop.add.button('retour au jeu', self.start)

        # Menu des options
        self.options = pygame_menu.Menu("Options", self.screenDim[0], self.screenDim[1],
                                        theme=pygame_menu.themes.THEME_GREEN)
        self.options.add.range_slider('Musique', 50, (0, 100), 1, rangeslider_id="music",
                                      value_format=lambda x: str(int(x)))
        self.options.add.range_slider('Effets sonore', 50, (0, 100), 1, rangeslider_id="sfx",
                                      value_format=lambda x: str(int(x)))
        self.options.add.button('commandes', self.show_control)
        self.options.add.button('retour au jeu', self.start)
        self.options.add.button('Quitter le jeu', pygame_menu.events.EXIT)

        # Menu des controles
        self.control = pygame_menu.Menu("Commandes", self.screenDim[0], self.screenDim[1],
                                        theme=pygame_menu.themes.THEME_GREEN)
        self.control.add.text_input('haut : ', default='z')
        self.control.add.text_input('bas : ', default='s')
        self.control.add.text_input('gauche : ', default='q')
        self.control.add.text_input('droite : ', default='d')
        self.control.add.text_input('rechargement : ', default='r')
        self.control.add.text_input('acheter des munitions : ', default='c')
        self.control.add.text_input('poing : ', default='1')
        self.control.add.text_input('Pistolet : ', default='2')
        self.control.add.text_input('mitraillette : ', default='3')
        self.control.add.button('retour', self.start)
        self.control.add.button('Quitter le jeu', pygame_menu.events.EXIT)
        # manque un moyen de quitter (W.I.P.)

        # Menu principal
        self.principal = pygame_menu.Menu("Bienvenue !", self.screenDim[0], self.screenDim[1],
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.principal.add.text_input('Nom du Perso : ', default='Billy')
        self.principal.add.button('Lancer la partie', self.start)
        self.principal.add.button('commandes', self.show_control)
        self.principal.add.button('Quitter le jeu', pygame_menu.events.EXIT)  # Quitter

        self.mort = pygame_menu.Menu("Vous êtes mort D:", self.screenDim[0], self.screenDim[1],
                                theme=pygame_menu.themes.THEME_DARK)
        #self.mort.add.text_input("Vagues réussi : ", self.numero_vague)
        self.mort.add.button('Quitter le jeu', pygame_menu.events.EXIT)

    def show_control(self):
        self.Menu("control", self.screen)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()
        if pressed[pygame.K_s]:
            self.player.move_down()
        if pressed[pygame.K_q]:
            self.player.move_left()
        if pressed[pygame.K_d]:
            self.player.move_right()
        if pygame.mouse.get_pressed()[0]:
            if self.player.can_shoot():
                self.player.remove_bullet_magazine()
                self.bullet_group.add(self.player.create_bullet())

        if pressed[pygame.K_1]:
            self.player.change_weapon('hand')
            self.player.weapon = self.player.hand()
        if pressed[pygame.K_2]:
            self.player.change_weapon('pistol')
            self.player.weapon = self.player.pistol()
        if pressed[pygame.K_3]:
            self.player.change_weapon('smg')
            self.player.weapon = self.player.smg()
        if pressed[pygame.K_r]:
            self.wait = "push"
        if self.wait == "push" and not pressed[pygame.K_r]:
            self.player.reload()
            self.wait = "no_push"
        if pressed[pygame.K_c]:
            self.Menu("shop", self.screen)
        if pressed[pygame.K_ESCAPE]:
            self.Menu("options", self.screen)


    def vagues(self, taille_vague):
        for i in range(0, taille_vague):
            if random.randint(0,1) == 0:
                if random.randint(0,1) == 0:
                    self.spawn(random.randint(50,700), 50)
                else:
                    self.spawn(random.randint(50, 700), 700)
            else:
                if random.randint(0,1) == 0:
                    self.spawn(50, random.randint(50,700))
                else:
                    self.spawn(700, random.randint(50,700))

    def spawn(self, x, y):
        self.enemy_group.add(Enemy(x,y))

    def new_vague(self):
        if len(self.enemy_group) == 0:
            self.vagues(self.numero_vague)
            self.numero_vague += 1

    def collision_circle(self, sprite, list):
        collision = False
        for wall in list:
            distance = math.hypot(sprite.position[0] - wall[0], sprite.position[1] - wall[1])
            if distance <= sprite.radius + self.wall_radius:
                collision = True
        return collision

    def update(self):
        self.player_group.update()
        self.bullet_group.update()
        self.enemy_group.update(self.player.position[0], self.player.position[1])
        self.UI.update(self.player.munition, self.player.coin, self.player.score, self.player.smg_magazine, self.player.pistol_magazine, self.numero_vague)

        # Gestion collision
        for sprite in self.bullet_group.sprites():
            for enemy in self.enemy_group:
                distance = math.hypot(sprite.pos[0] - enemy.position[0], sprite.pos[1] - enemy.position[1])
                if distance <= sprite.radius + enemy.radius:
                    enemy.touche()
                    sprite.touche()
                    self.player.get_coin()
                    self.player.get_point()

        if self.collision_circle(self.player, self.walls):
            self.player.move_back()
        for enemy in self.enemy_group:
            if self.collision_circle(enemy, self.walls):
                col = enemy.position
                enemy.move_back()
                if col[0] >= enemy.position[0] and col[1] > enemy.position[1]:
                    enemy.position[0] -= 2
                    enemy.position[1] -= 1
                elif col[0] > enemy.position[0] and col[1] <= enemy.position[1]:
                    enemy.position[0] -= 1
                    enemy.position[1] += 2
                elif col[0] < enemy.position[0] and col[1] <= enemy.position[1]:
                    enemy.position[0] += 1
                    enemy.position[1] += 2
                elif col[0] <= enemy.position[0] and col[1] > enemy.position[1]:
                    enemy.position[0] += 2
                    enemy.position[1] -= 1

        if self.player.munition == 0:
            self.UI.no_mun = True
        else:
            self.UI.no_mun = False


    def Menu(self, choix, surface):
        if choix == "principal":
            self.principal.mainloop(surface)
        elif choix == "mort":
            self.mort.mainloop(surface)
        elif choix == "options":
            self.options.mainloop(surface)
        elif choix == "secret":
            self.secret.mainloop(surface)
        elif choix == "control":
            self.control.mainloop(surface)
        elif choix == "shop":
            self.shop.mainloop(surface)
        else:
            print("Le choix désiré n'existe pas.")

    def damages(self):
        for zombie in self.enemy_group:
            zombie.tempo()
            distance = math.hypot(self.player.position[0] - zombie.position[0], self.player.position[1] - zombie.position[1])
            if distance <= self.player.radius + zombie.radius and zombie.cooldown == 0:
                self.player.health = self.player.health - 1
                mixer.Sound('son/croc.wav').play()
                zombie.cooldown = 1
                

    def dead(self):
        if self.player.health <= 0:
            living = False
        else :
            living = True
        return living

    def start(self):
        clock = pygame.time.Clock()
        # Game loop
        alive = True
        while alive:

            for wall in self.walls:
                pygame.draw.circle(self.screen, (0, 0, 0), (wall[0], wall[1]), 25, 0)
            for sprite in self.enemy_group:
                sprite.save_location()
                pygame.draw.circle(self.screen, (255, 228, 96), (sprite.position[0], sprite.position[1]), 20, 0)
            for bullet in self.bullet_group:
                pygame.draw.circle(self.screen, (0, 0, 0), (bullet.pos[0], bullet.pos[1]), 5, 0)
            self.update()
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.map, (0, 0))
            self.player.save_location()
            self.handle_input()
            self.player_group.draw(self.screen)
            pygame.draw.circle(self.screen, (self.player.health_display()),
                               (self.player.position[0], self.player.position[1]), 15, 0)
            self.bullet_group.draw(self.screen)
            self.enemy_group.draw(self.screen)
            self.UI.render(self.screen)
            self.new_vague()
            self.damages()



            # update the full display surface to the screen
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    alive = False

            alive = self.dead()
            # FPS
            clock.tick(60)

        self.Menu("mort", self.screen)

    def run(self):

        self.Menu('principal', self.screen)
        pygame.quit()
