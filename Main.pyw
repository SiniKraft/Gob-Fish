print("[INFO]: Lancement du jeu.")

# Importation des modules

try:
    print("------------------------------Détails-de-Pygame------------------------")
    import pygame

    print("-----------------------------------------------------------------------")
    import sys
    import time
    import random
    import pickle
    import os
except:
    print("[ERREUR]: Impossible d'importer le modules !")
    sys.exit()

# Initialisation de Pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()  # Sons de pygame.

# Définition de la fenêtre

try:
    screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
except:
    screen = pygame.display.set_mode(1280, 720)
pygame.display.set_caption("GobFish")
clock = pygame.time.Clock()
FPS = 60

# Définition des couleurs

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (159, 255, 159)
BLUE = (159, 159, 255)

# import des textures sons et textes.

shark_right = pygame.image.load("textures/shark/shark_right.png").convert_alpha()
shark_right_open = pygame.image.load("textures/shark/shark_right_open.png").convert_alpha()
shark_left_open = pygame.image.load("textures/shark/shark_left_open.png").convert_alpha()
shark_left = pygame.image.load("textures/shark/shark_left.png").convert_alpha()
background = pygame.image.load("textures/background/background.jpg").convert_alpha()
icon = pygame.image.load("textures/icon/icon.png").convert_alpha()
title = pygame.image.load("textures/background/title.png").convert_alpha()
evil_fish_right = pygame.image.load("textures/evil_fish/evil_fish_right.png").convert_alpha()
evil_fish_left = pygame.image.load("textures/evil_fish/evil_fish_left.png").convert_alpha()
fish_right = pygame.image.load("textures/fish/fish_right.png").convert_alpha()
fish_left = pygame.image.load("textures/fish/fish_left.png").convert_alpha()
no_texture = pygame.image.load("textures/no_texture.png").convert_alpha()
health = pygame.image.load("textures/health/health.png").convert_alpha()
start_font = pygame.font.SysFont('Comic Sans MS', 30)
end_font = pygame.font.SysFont('Comic Sans MS', 50)
var_font = pygame.font.SysFont('Comic Sans MS', 20)
time_font = pygame.font.SysFont('Comic Sans MS', 50)
eat_sound = pygame.mixer.Sound("sounds/eat.wav")
pic_sound = pygame.mixer.Sound("sounds/pic.wav")
swim1 = pygame.mixer.Sound("sounds/swim1.ogg")
swim2 = pygame.mixer.Sound("sounds/swim2.ogg")
swim3 = pygame.mixer.Sound("sounds/swim3.ogg")
swim4 = pygame.mixer.Sound("sounds/swim4.ogg")

try:
    file = open("save/save.dat", 'rb')
    better_score = pickle.load(file)
    file.close()
except:
    better_score = 0

# Icone

pygame.display.set_icon(icon)

# Lancement de l'écran titre

screen.blit(title, (0, 0))
start_text = start_font.render('The game will start in 3 seconds.', False, (0, 0, 0))
screen.blit(start_text, (400, 600))
pygame.display.update()
time.sleep(1)
screen.blit(title, (0, 0))
start_text = start_font.render('The game will start in 2 seconds.', False, (0, 0, 0))
screen.blit(start_text, (400, 600))
pygame.display.update()
time.sleep(1)
screen.blit(title, (0, 0))
start_text = start_font.render('The game will start in 1 second.', False, (0, 0, 0))
screen.blit(start_text, (400, 600))
pygame.display.update()
time.sleep(1)

# Définition du joueur

eating = 0
can_eat = 1
time_remaining = 0
shark_direction = "right"
poisson_manges = 0
chrono = 0
generated_fishes = 0
eated_fishes = var_font.render("Eaten fishes : ", False, (0, 0, 0))
estmort = False
temp = 99
temp_remains = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = shark_right
        self.rect = self.image.get_rect()  # Adapte le taille du personnage a la taille de l'image.
        self.velocity = [0, 0]
        self.rect.x = 640
        self.rect.y = 360
        self.vies = 4
        self.time_vies = 0

    def update(self):
        self.rect.move_ip(*self.velocity)

    def enlever_vies(self):
        if self.time_vies < 0.1:
            self.vies = self.vies - 1
            self.time_vies = 30


class Poisson(pygame.sprite.Sprite):
    def __init__(self):
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


# Vérifie si le joueur et un poisson se touchent.

def collision(poisson, player1):
    if player1.right < poisson.left:
        return False
    if player1.bottom < poisson.top:
        return False
    if player1.left > poisson.right:
        return False
    if player1.top > poisson.bottom:
        return False
    return True


# Joue 1 des 4 sons de swim

def play_swim_sound():
    nombre_alea = random.randint(0, 4)
    if nombre_alea > 3:
        swim4.play()
    else:
        if nombre_alea > 2:
            swim3.play()
        else:
            if nombre_alea > 1:
                swim2.play()
            else:
                swim1.play()


player = Player()
poisson1 = Poisson()
timeout = False
running = True  # Arrête la fenêtre si cette variable est sur False.
while running:
    dt = clock.tick(FPS) / 1000  # Change les FPS en secondes.
    screen.fill(BLACK)  # Rempli l'arrière plan de cette couleur.
    var_text = var_font.render(str(round(poisson_manges)), False, (255, 0, 0))

    player.time_vies = player.time_vies - 0.1
    if player.time_vies < -1:
        player.time_vies = -0.1

    if collision(poisson1.rect, player.rect):
        if eating == 1 and poisson1.is_fish:
            poisson_manges = poisson_manges + 1
            poisson1.is_fish = False
            eat_sound.play()

    if generated_fishes > 0:
        if collision(poisson2.rect, player.rect):
            if eating == 1 and poisson2.is_fish:
                poisson_manges = poisson_manges + 1
                poisson2.is_fish = False
                eat_sound.play()

    if generated_fishes > 1:
        if collision(evil_poisson1.rect, player.rect):
            if evil_poisson1.is_fish:
                evil_poisson1.is_fish = False
                player.enlever_vies()
                pic_sound.play()

    if generated_fishes > 2:
        if collision(poisson3.rect, player.rect):
            if eating == 1 and poisson3.is_fish:
                poisson_manges = poisson_manges + 1
                poisson3.is_fish = False
                eat_sound.play()

    if generated_fishes > 3:
        if collision(poisson4.rect, player.rect):
            if eating == 1 and poisson4.is_fish:
                poisson_manges = poisson_manges + 1
                poisson4.is_fish = False
                eat_sound.play()

    if generated_fishes > 4:
        if collision(evil_poisson2.rect, player.rect):
            if evil_poisson2.is_fish:
                evil_poisson2.is_fish = False
                player.enlever_vies()
                pic_sound.play()

    if generated_fishes > 5:
        if collision(poisson5.rect, player.rect):
            if eating == 1 and poisson5.is_fish:
                poisson_manges = poisson_manges + 1
                poisson5.is_fish = False
                eat_sound.play()

    if generated_fishes > 6:
        if collision(evil_poisson3.rect, player.rect):
            if eating == 1 and evil_poisson3.is_fish:
                poisson_manges = poisson_manges - 4
                evil_poisson3.is_fish = False
                player.enlever_vies()
                pic_sound.play()

    if generated_fishes > 7:
        if collision(poisson6.rect, player.rect):
            if eating == 1 and poisson6.is_fish:
                poisson_manges = poisson_manges + 1
                poisson6.is_fish = False
                eat_sound.play()

    if generated_fishes > 8:
        if collision(evil_poisson4.rect, player.rect):
            if evil_poisson4.is_fish:
                poisson_manges = poisson_manges - 4
                evil_poisson4.is_fish = False
                player.enlever_vies()
                pic_sound.play()

    if generated_fishes > 9:
        if collision(poisson7.rect, player.rect):
            if eating == 1 and poisson7.is_fish:
                poisson_manges = poisson_manges + 1
                poisson7.is_fish = False
                eat_sound.play()


    def reanimer(poisson):
        if not poisson.is_fish:
            poisson.remaining_time = poisson.remaining_time + 0.02
            if poisson.remaining_time > 6:
                poisson.is_fish = True
                poisson.remaining_time = 0


    reanimer(poisson1)
    if generated_fishes > 0:
        reanimer(poisson2)
    if generated_fishes > 1:
        reanimer(evil_poisson1)
    if generated_fishes > 2:
        reanimer(poisson3)
    if generated_fishes > 3:
        reanimer(poisson4)
    if generated_fishes > 4:
        reanimer(evil_poisson2)
    if generated_fishes > 5:
        reanimer(poisson5)
    if generated_fishes > 6:
        reanimer(evil_poisson3)
    if generated_fishes > 7:
        reanimer(poisson6)
    if generated_fishes > 8:
        reanimer(evil_poisson4)
    if generated_fishes > 9:
        reanimer(poisson7)

    for event in pygame.event.get():  # Boucle faisant bouger le personnage en vérifiant les touches.
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.velocity[1] = -300 * dt  # 300 pixels par seconde
            elif event.key == pygame.K_s:
                player.velocity[1] = 300 * dt
            elif event.key == pygame.K_a:
                player.velocity[0] = -300 * dt
                shark_direction = "left"
            elif event.key == pygame.K_d:
                player.velocity[0] = 300 * dt
                shark_direction = "right"
            elif event.key == pygame.K_ESCAPE:  # Quitter si le bouton echap est pressé.
                running = False
            elif event.key == pygame.K_SPACE:
                if eating == 0 and can_eat == 1:
                    eating = 1
                    can_eat = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.velocity[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                player.velocity[0] = 0


    if player.vies == 0:
        running = False
        estmort = True




    # IA du poisson.

    def IA_poisson_normal(poisson):

        if poisson.direction == "right":
            if poisson.rect.x > 1158:
                poisson.direction = "left"
            if random.randint(0, 1000) > 1:
                poisson.velocity[0] = int(300 * dt)
            else:
                poisson.direction = "left"

        else:
            if poisson.rect.x < 0:
                poisson.direction = "right"
            if random.randint(0, 1000) > 1:
                poisson.velocity[0] = int(-300 * dt)
            else:
                poisson.direction = "right"
# IA en haut et en bas
        if poisson.direction_y == "up":
            if poisson.rect.y < 0:
                poisson.direction_y = "down"
            if random.randint(0, 1000) > 1:
                poisson.velocity[1] = int(-200 * dt)
            else:
                poisson.direction = "down"
        else:
            if poisson.rect.y > 630:
                poisson.direction_y = "up"
            if random.randint(0, 1000) > 1:
                poisson.velocity[1] = int(200 * dt)
            else:
                poisson.direction = "up"


    IA_poisson_normal(poisson1)
    if generated_fishes > 0:
        IA_poisson_normal(poisson2)
    if generated_fishes > 1:
        IA_poisson_normal(evil_poisson1)
    if generated_fishes > 2:
        IA_poisson_normal(poisson3)
    if generated_fishes > 3:
        IA_poisson_normal(poisson4)
    if generated_fishes > 4:
        IA_poisson_normal(evil_poisson2)
    if generated_fishes > 5:
        IA_poisson_normal(poisson5)
    if generated_fishes > 6:
        IA_poisson_normal(evil_poisson3)
    if generated_fishes > 7:
        IA_poisson_normal(poisson6)
    if generated_fishes > 8:
        IA_poisson_normal(evil_poisson4)
    if generated_fishes > 9:
        IA_poisson_normal(poisson7)

    poisson1.update()
    if generated_fishes > 0:
        poisson2.update()
    if generated_fishes > 1:
        evil_poisson1.update()
    if generated_fishes > 2:
        poisson3.update()
    if generated_fishes > 3:
        poisson4.update()
    if generated_fishes > 4:
        evil_poisson2.update()
    if generated_fishes > 5:
        poisson5.update()
    if generated_fishes > 6:
        evil_poisson3.update()
    if generated_fishes > 7:
        poisson6.update()
    if generated_fishes > 8:
        evil_poisson4.update()
    if generated_fishes > 9:
        poisson7.update()
    player.update()

    chrono = chrono + 0.01
    if chrono > 10 and generated_fishes == 0:
        poisson2 = Poisson()
        generated_fishes = 1
    else:
        if chrono > 15 and generated_fishes == 1:
            evil_poisson1 = Poisson()
            evil_poisson1.is_evil = True
            generated_fishes = 2
        else:
            if not generated_fishes > 9:
                if generated_fishes == 2 and chrono > 20:
                    poisson3 = Poisson()
                    generated_fishes = 3
                else:
                    if generated_fishes == 3 and chrono > 30:
                        poisson4 = Poisson()
                        generated_fishes = 4
                    else:
                        if generated_fishes == 4 and chrono > 35:
                            evil_poisson2 = Poisson()
                            evil_poisson2.is_evil = True
                            generated_fishes = 5
                        else:
                            if generated_fishes == 5 and chrono > 40:
                                poisson5 = Poisson()
                                generated_fishes = 6
                            else:
                                if generated_fishes == 6 and chrono > 45:
                                    evil_poisson3 = Poisson()
                                    evil_poisson3.is_evil = True
                                    generated_fishes = 7
                                else:
                                    if generated_fishes == 7 and chrono > 50:
                                        poisson6 = Poisson()
                                        generated_fishes = 8
                                    else:
                                        if generated_fishes == 8 and chrono > 55:
                                            evil_poisson4 = Poisson()
                                            evil_poisson4.is_evil = True
                                            generated_fishes = 9
                                        else:
                                            if generated_fishes == 9 and chrono > 60:
                                                poisson7 = Poisson()
                                                generated_fishes = 10

    # Verifier si le poisson doit s'arrêter de manger ou si il doit changer de direction.

    if eating == 1:
        time_remaining = time_remaining + 0.01
        if time_remaining > 1:
            time_remaining = 0
            eating = 0
    if eating == 0 and can_eat == 0:
        time_remaining = time_remaining + 0.01
    if time_remaining > 1.3:
        time_remaining = 0
        eating = 0
        can_eat = 1
    if shark_direction == "right":
        if eating == 1:
            player.image = shark_right_open
        else:
            player.image = shark_right
    if shark_direction == "left":
        if eating == 1:
            player.image = shark_left_open
        else:
            player.image = shark_left


    # Vérifions si le poisson1 est un poisson, si oui, l'afficher au cas ou il ne l'etait pas, si non , le cacher.
    def actualiser_texture(poisson):
        if poisson.is_fish:
            if poisson.direction == "right":
                if poisson.is_evil == True:
                    poisson.change_texture(evil_fish_right)
                else:
                    poisson.change_texture(fish_right)
            else:
                if poisson.is_evil == True:
                    poisson.change_texture(evil_fish_left)
                else:
                    poisson.change_texture(fish_left)
        else:
            poisson.kill()


    actualiser_texture(poisson1)
    if generated_fishes > 0:
        actualiser_texture(poisson2)
    if generated_fishes > 1:
        actualiser_texture(evil_poisson1)
    if generated_fishes > 2:
        actualiser_texture(poisson3)
    if generated_fishes > 3:
        actualiser_texture(poisson4)
    if generated_fishes > 4:
        actualiser_texture(evil_poisson2)
    if generated_fishes > 5:
        actualiser_texture(poisson5)
    if generated_fishes > 6:
        actualiser_texture(evil_poisson3)
    if generated_fishes > 7:
        actualiser_texture(poisson6)
    if generated_fishes > 8:
        actualiser_texture(evil_poisson4)
    if generated_fishes > 9:
        actualiser_texture(poisson7)

    # Actualise l'ecran.
    print(player.rect.y)
    screen.blit(background, (0, 0))
    screen.blit(poisson1.image, poisson1.rect)
    if generated_fishes > 0:
        screen.blit(poisson2.image, poisson2.rect)
    if generated_fishes > 1:
        screen.blit(evil_poisson1.image, evil_poisson1.rect)
    if generated_fishes > 2:
        screen.blit(poisson3.image, poisson3.rect)
    if generated_fishes > 3:
        screen.blit(poisson4.image, poisson4.rect)
    if generated_fishes > 4:
        screen.blit(evil_poisson2.image, evil_poisson2.rect)
    if generated_fishes > 5:
        screen.blit(poisson5.image, poisson5.rect)
    if generated_fishes > 6:
        screen.blit(evil_poisson3.image, evil_poisson3.rect)
    if generated_fishes > 7:
        screen.blit(poisson6.image, poisson6.rect)
    if generated_fishes > 8:
        screen.blit(evil_poisson4.image, evil_poisson4.rect)
    if generated_fishes > 9:
        screen.blit(poisson7.image, poisson7.rect)
    time_text = time_font.render(str(temp), False, (255, 0, 0))
    screen.blit(player.image, player.rect)
    if player.vies > 1:
        screen.blit(health, (864, 0))
        if player.vies > 2:
            screen.blit(health, (928, 0))
            if player.vies > 3:
                screen.blit(health, (992, 0))
    screen.blit(eated_fishes, (1110, 0))
    screen.blit(var_text, (1250, 0))
    screen.blit(time_text, (10, 0))
    pygame.display.update()
    temp_remains = temp_remains + 0.1
    if temp_remains > 6:
        temp_remains = 0
        temp = temp - 1
        if temp == 0:
            running = False
            estmort = True
            timeout = True

# A partir d'ici, le jeu s'est arrêté.
# Vérifions si il s'est arrêté avec échap ou car le joueur a perdu.
restart = False
if estmort:
    newecran = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("You died because you hit a wounding fish !")
    if timeout:
        pygame.display.set_caption("You died because you didn't have enough time !")
    pygame.display.update()
    continuer = True
    pygame.display.set_icon(icon)
    end_text = end_font.render('Your score :', False, (0, 0, 0))
    end_var_text = end_font.render(str(round(poisson_manges)), False, (255, 0, 0))
    better_score_text = start_font.render('Best score (before yours) :', False, (0, 0, 0))
    better_score_var_text = start_font.render(str(round(better_score)), False, (255, 0, 0))

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    continuer = False
                    restart = True
                else:
                    if event.key == pygame.K_KP_ENTER:
                        continuer = False
                        restart = True
                    else:
                        if event.key == pygame.K_ESCAPE:
                            continuer = False
        pygame.display.update()
        screen.blit(background, (0, 0))
        screen.blit(end_text, (120, 100))
        screen.blit(end_var_text, (420, 100))
        screen.blit(better_score_text, (80, 210))
        screen.blit(better_score_var_text, (500, 210))
        screen.blit(var_font.render('Press ENTER to replay.', False, (0, 0, 0)), (180, 300))

    if better_score < poisson_manges:
        better_score = poisson_manges
        outfile = open("save/save.dat", 'wb')
        pickle.dump(better_score, outfile)
        outfile.close()

print("[INFO]: Arrêt du jeu.")

if restart:
    os.startfile('Restartscript.vbs')
    print("[INFO]: Redémarrage du jeu.")
