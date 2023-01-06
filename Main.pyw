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
    from Scripts.Class.ClassPlayer import Player
    from Scripts.Class.ClassFish import Poisson
except RuntimeError as re:
    import sys

    print("[ERREUR]: Impossible d'importer le modules ! %s" % str(re))
    sys.exit()

joysticks = []
try:
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
except Exception as e:
    print(e)


# Initialisation de Pygame
def main():
    using_controller = False
    last_controller = 0
    retval = False
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()  # Sons de pygame.

    # Définition de la fenêtre

    try:
        screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN | pygame.SCALED)
    except IOError:
        screen = pygame.display.set_mode((1280, 720))
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

    shark_right_1 = pygame.image.load("textures/shark/animation/right/shark_pos_1.png").convert_alpha()
    shark_right_2 = pygame.image.load("textures/shark/animation/right/shark_pos_2.png").convert_alpha()
    shark_right_3 = pygame.image.load("textures/shark/animation/right/shark_pos_3.png").convert_alpha()
    shark_right_4 = pygame.image.load("textures/shark/animation/right/shark_pos_4.png").convert_alpha()
    shark_right_5 = pygame.image.load("textures/shark/animation/right/shark_pos_5.png").convert_alpha()
    shark_right_6 = pygame.image.load("textures/shark/animation/right/shark_pos_6.png").convert_alpha()
    shark_right_7 = pygame.image.load("textures/shark/animation/right/shark_pos_7.png").convert_alpha()

    shark_left_1 = pygame.image.load("textures/shark/animation/left/shark_pos_1.png").convert_alpha()
    shark_left_2 = pygame.image.load("textures/shark/animation/left/shark_pos_2.png").convert_alpha()
    shark_left_3 = pygame.image.load("textures/shark/animation/left/shark_pos_3.png").convert_alpha()
    shark_left_4 = pygame.image.load("textures/shark/animation/left/shark_pos_4.png").convert_alpha()
    shark_left_5 = pygame.image.load("textures/shark/animation/left/shark_pos_5.png").convert_alpha()
    shark_left_6 = pygame.image.load("textures/shark/animation/left/shark_pos_6.png").convert_alpha()
    shark_left_7 = pygame.image.load("textures/shark/animation/left/shark_pos_7.png").convert_alpha()

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
    replace_string = ""
    replace_x = 400
    if len(joysticks) > 0:
        replace_string = "or a controller button "
        replace_x = 250
    start_text = start_font.render('         Press SPACE %sto play !' % replace_string, True, (0, 0, 0))
    screen.blit(start_text, (replace_x, 600))
    screen.blit(start_font.render("v1.5", True, (0, 0, 0)), (0, 680))
    screen.blit(start_font.render("github.com/SiniKraft", True, (0, 0, 0)), (980, 680))
    pygame.display.update()
    continuer_loop = True
    while continuer_loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                using_controller = False
                if event.key == pygame.K_SPACE:
                    continuer_loop = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.JOYBUTTONDOWN:
                continuer_loop = False

    # Définition du joueur

    eating = 0
    can_eat = 1
    time_remaining = 0
    shark_direction = "right"
    poisson_manges = 0
    chrono = 0
    generated_fishes = 0
    eaten_fishes = var_font.render("Eaten fishes : ", True, (0, 0, 0))
    estmort = False
    temp = 99
    temp_remains = 0

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

    player = Player(shark_right)
    poisson1 = Poisson(fish_right, no_texture)
    timeout = False
    running = True  # Arrête la fenêtre si cette variable est sur False.

    while running:
        dt = clock.tick(FPS) / 1000  # Change les FPS en secondes.
        screen.fill(BLACK)  # Rempli l'arrière-plan de cette couleur.
        var_text = var_font.render(str(round(poisson_manges)), True, (255, 0, 0))
        been_collision = 0

        player.time_vies = player.time_vies - 0.1
        if player.time_vies < -1:
            player.time_vies = -0.1

        if collision(poisson1.rect, player.rect):
            if eating == 1 and poisson1.is_fish:
                poisson_manges = poisson_manges + 1
                poisson1.is_fish = False
                been_collision = 1
                eat_sound.play()

        if generated_fishes > 0:
            if collision(poisson2.rect, player.rect):
                if eating == 1 and poisson2.is_fish:
                    poisson_manges = poisson_manges + 1
                    poisson2.is_fish = False
                    been_collision = 1
                    eat_sound.play()

        if generated_fishes > 1:
            if collision(evil_poisson1.rect, player.rect):
                if evil_poisson1.is_fish:
                    evil_poisson1.is_fish = False
                    been_collision = 2
                    player.enlever_vies()
                    pic_sound.play()

        if generated_fishes > 2:
            if collision(poisson3.rect, player.rect):
                if eating == 1 and poisson3.is_fish:
                    poisson_manges = poisson_manges + 1
                    poisson3.is_fish = False
                    been_collision = 1
                    eat_sound.play()

        if generated_fishes > 3:
            if collision(poisson4.rect, player.rect):
                if eating == 1 and poisson4.is_fish:
                    poisson_manges = poisson_manges + 1
                    poisson4.is_fish = False
                    been_collision = 1
                    eat_sound.play()

        if generated_fishes > 4:
            if collision(evil_poisson2.rect, player.rect):
                if evil_poisson2.is_fish:
                    evil_poisson2.is_fish = False
                    been_collision = 2
                    player.enlever_vies()
                    pic_sound.play()

        if generated_fishes > 5:
            if collision(poisson5.rect, player.rect):
                if eating == 1 and poisson5.is_fish:
                    poisson_manges = poisson_manges + 1
                    poisson5.is_fish = False
                    been_collision = 1
                    eat_sound.play()

        if generated_fishes > 6:
            if collision(evil_poisson3.rect, player.rect):
                if eating == 1 and evil_poisson3.is_fish:
                    poisson_manges = poisson_manges - 4
                    evil_poisson3.is_fish = False
                    been_collision = 2
                    player.enlever_vies()
                    pic_sound.play()

        if generated_fishes > 7:
            if collision(poisson6.rect, player.rect):
                if eating == 1 and poisson6.is_fish:
                    poisson_manges = poisson_manges + 1
                    poisson6.is_fish = False
                    been_collision = 1
                    eat_sound.play()

        if generated_fishes > 8:
            if collision(evil_poisson4.rect, player.rect):
                if evil_poisson4.is_fish:
                    poisson_manges = poisson_manges - 4
                    evil_poisson4.is_fish = False
                    been_collision = 2
                    player.enlever_vies()
                    pic_sound.play()

        if generated_fishes > 9:
            if collision(poisson7.rect, player.rect):
                if eating == 1 and poisson7.is_fish:
                    poisson_manges = poisson_manges + 1
                    poisson7.is_fish = False
                    been_collision = 1
                    eat_sound.play()

        if using_controller and been_collision > 0:
            try:
                if been_collision == 1:
                    joysticks[last_controller].rumble(1.0, 1.0, 200)
                else:
                    joysticks[last_controller].rumble(1.0, 1.0, 100)
            except:
                pass

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
                using_controller = False
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    player.velocity[1] = int(-300 * dt)  # 300 pixels par seconde
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.velocity[1] = int(300 * dt)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    player.velocity[0] = int(-300 * dt)
                    shark_direction = "left"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.velocity[0] = int(300 * dt)
                    shark_direction = "right"
                elif event.key == pygame.K_ESCAPE:  # Quitter si le bouton echap est pressé.
                    running = False
                elif event.key == pygame.K_SPACE:
                    if eating == 0 and can_eat == 1:
                        eating = 1
                        can_eat = 0
                        player.anime_time = 7
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    player.velocity[1] = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.velocity[1] = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    if shark_direction == "left":
                        player.velocity[0] = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if shark_direction == "right":
                        player.velocity[0] = 0
            elif event.type == pygame.JOYBUTTONDOWN:
                using_controller = True
                last_controller = event.joy
                if eating == 0 and can_eat == 1:
                    eating = 1
                    can_eat = 0
                    player.anime_time = 7
            elif event.type == pygame.JOYAXISMOTION:
                using_controller = True
                last_controller = event.joy
                player.velocity = [
                    joysticks[last_controller].get_axis(0) * 5,
                    joysticks[last_controller].get_axis(1) * 5
                ]
                if player.velocity[0] < 0:
                    shark_direction = "left"
                else:
                    shark_direction = "right"
            elif event.type == pygame.MOUSEMOTION:
                using_controller = False

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
            poisson2 = Poisson(fish_right, no_texture)
            generated_fishes = 1
        else:
            if chrono > 15 and generated_fishes == 1:
                evil_poisson1 = Poisson(fish_right, no_texture)
                evil_poisson1.is_evil = True
                generated_fishes = 2
            else:
                if not generated_fishes > 9:
                    if generated_fishes == 2 and chrono > 20:
                        poisson3 = Poisson(fish_right, no_texture)
                        generated_fishes = 3
                    else:
                        if generated_fishes == 3 and chrono > 30:
                            poisson4 = Poisson(fish_right, no_texture)
                            generated_fishes = 4
                        else:
                            if generated_fishes == 4 and chrono > 35:
                                evil_poisson2 = Poisson(fish_right, no_texture)
                                evil_poisson2.is_evil = True
                                generated_fishes = 5
                            else:
                                if generated_fishes == 5 and chrono > 40:
                                    poisson5 = Poisson(fish_right, no_texture)
                                    generated_fishes = 6
                                else:
                                    if generated_fishes == 6 and chrono > 45:
                                        evil_poisson3 = Poisson(fish_right, no_texture)
                                        evil_poisson3.is_evil = True
                                        generated_fishes = 7
                                    else:
                                        if generated_fishes == 7 and chrono > 50:
                                            poisson6 = Poisson(fish_right, no_texture)
                                            generated_fishes = 8
                                        else:
                                            if generated_fishes == 8 and chrono > 55:
                                                evil_poisson4 = Poisson(fish_right, no_texture)
                                                evil_poisson4.is_evil = True
                                                generated_fishes = 9
                                            else:
                                                if generated_fishes == 9 and chrono > 60:
                                                    poisson7 = Poisson(fish_right, no_texture)
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
            can_eat = 1  # eat clock
        if shark_direction == "right":
            if eating == 1:
                if player.anime_time == 7:
                    player.image = shark_right_7
                    player.change_texture(shark_right_7)
                else:
                    if player.anime_time == 6:
                        player.image = shark_right_6
                        player.change_texture(shark_right_6)
                    else:
                        if player.anime_time == 5:
                            player.image = shark_right_5
                            player.change_texture(shark_right_5)
                        else:
                            if player.anime_time == 4:
                                player.image = shark_right_4
                                player.change_texture(shark_right_4)
                            else:
                                if player.anime_time == 3:
                                    player.image = shark_right_3
                                    player.change_texture(shark_right_3)
                                else:
                                    if player.anime_time == 2:
                                        player.image = shark_right_2
                                        player.change_texture(shark_right_2)
                                    else:
                                        if player.anime_time == 1:
                                            player.image = shark_right_1
                                            player.change_texture(shark_right_1)
                                        else:
                                            if player.anime_time == 0:
                                                player.image = shark_right_open
                                                player.change_texture(shark_right_open)
            else:
                player.image = shark_right
        if shark_direction == "left":
            if eating == 1:
                if player.anime_time == 7:
                    player.image = shark_left_7
                    player.change_texture(shark_left_7)
                else:
                    if player.anime_time == 6:
                        player.image = shark_left_6
                        player.change_texture(shark_left_6)
                    else:
                        if player.anime_time == 5:
                            player.image = shark_left_5
                            player.change_texture(shark_left_5)
                        else:
                            if player.anime_time == 4:
                                player.image = shark_left_4
                                player.change_texture(shark_left_4)
                            else:
                                if player.anime_time == 3:
                                    player.image = shark_left_3
                                    player.change_texture(shark_left_3)
                                else:
                                    if player.anime_time == 2:
                                        player.image = shark_left_2
                                        player.change_texture(shark_left_2)
                                    else:
                                        if player.anime_time == 1:
                                            player.image = shark_left_1
                                            player.change_texture(shark_left_1)
                                        else:
                                            if player.anime_time == 0:
                                                player.image = shark_left_open
                                                player.change_texture(shark_left_open)
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

        if player.anime_time < 8 and not player.anime_time == 0 and not player.isAnimationFliped == 1:
            player.anime_time = player.anime_time - 1
        if player.anime_time == 0:
            if player.waitBeforeClose > 15:
                player.anime_time = player.anime_time + 1
                player.waitBeforeClose = 0
                player.isAnimationFliped = 1
            else:
                player.waitBeforeClose = player.waitBeforeClose + 0.25
        if player.anime_time < 8 and not player.anime_time == 0 and not player.isAnimationFliped == 0:
            player.anime_time = player.anime_time + 1
            if player.anime_time == 8:
                player.isAnimationFliped = 0

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

        # Actualise l'écran.
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
        time_text = time_font.render(str(temp), True, (255, 0, 0))
        screen.blit(player.image, player.rect)
        if player.vies > 1:
            screen.blit(health, (864, 0))
            if player.vies > 2:
                screen.blit(health, (928, 0))
                if player.vies > 3:
                    screen.blit(health, (992, 0))
        screen.blit(eaten_fishes, (1110, 0))
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

    # À partir d'ici, le jeu s'est arrêté.
    # Vérifions s'il s'est arrêté avec échap ou, car le joueur a perdu.
    restart = False
    if estmort:
        newecran = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("You died because you hit a wounding fish !")
        if timeout:
            pygame.display.set_caption("You died because you didn't have enough time !")
        pygame.display.update()
        continuer = True
        pygame.display.set_icon(icon)
        end_text = end_font.render('Your score :', True, (0, 0, 0))
        end_var_text = end_font.render(str(round(poisson_manges)), True, (255, 0, 0))
        better_score_text = start_font.render('Best score (before yours) :', True, (0, 0, 0))
        better_score_var_text = start_font.render(str(round(better_score)), True, (255, 0, 0))

        while continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                if event.type == pygame.KEYDOWN:
                    using_controller = False
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
                if event.type == pygame.JOYBUTTONDOWN:
                    continuer = False
                    restart = True
            pygame.display.update()
            screen.blit(background, (0, 0))
            screen.blit(end_text, (120, 100))
            screen.blit(end_var_text, (420, 100))
            screen.blit(better_score_text, (80, 210))
            screen.blit(better_score_var_text, (500, 210))
            screen.blit(var_font.render('Press ENTER to replay.', True, (0, 0, 0)), (180, 300))

        if better_score < poisson_manges:
            better_score = poisson_manges
            os.makedirs("save/", exist_ok=True)
            outfile = open("save/save.dat", 'wb')
            pickle.dump(better_score, outfile)
            outfile.close()

    if restart:
        retval = True
        print("[INFO]: Redémarrage du jeu.")
    else:
        print("[INFO]: Arrêt du jeu.")

    return retval


while main():
    pass

sys.exit()
