import pygame
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # run imgs
        self.run = []
        self.run_index = 0
        for i in range(0,6):
            self.run.append(pygame.image.load(f'resources/tiny-hero/1 Pink_Monster/Pink_Monster_Run_{i+1}.png').convert_alpha())
            self.run[i] = pygame.transform.scale(self.run[i], (82, 82))

        # jump imgs
        self.jump = []
        self.jump_index = 3
        for i in range(0,8):
            self.jump.append(pygame.image.load(f'resources/tiny-hero/1 Pink_Monster/Pink_Monster_Jump_{i+1}.png').convert_alpha())
            self.jump[i] = pygame.transform.scale(self.jump[i], (82, 82))
        
        self.image = self.run[self.run_index]
        self.rect = self.image.get_rect(midbottom = (100,325))
        self.gravity = 0
        self.health = 10
        self.hitbox = pygame.Rect.scale_by(self.rect, 0.5, 0.8)
        # sfx
        self.jump_sfx = pygame.mixer.Sound('resources/sound/jump.mp3')

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 325:
            self.gravity = -20
            jump_channel.play(self.jump_sfx)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 325:
            #estamos en el suelo
            self.rect.bottom = 325
            self.run_animation()
        else:
            self.jump_animation()

    def run_animation(self):
        if frame_counter % 3 == 0:
            self.run_index += 1
        if self.run_index > 5:
            self.run_index = 0
        self.image = self.run[self.run_index]

    def jump_animation(self):
        if self.gravity <= -14:
            self.jump_index = 0
        elif self.gravity > -14 and self.gravity <= -8:
            self.jump_index = 1
        elif self.gravity > -8 and self.gravity <= -2:
            self.jump_index = 2
        elif self.gravity > -2 and self.gravity <= 2:
            self.jump_index = 3
        elif self.gravity > 2 and self.gravity <=8:
            self.jump_index = 4
        elif self.gravity > 8 and self.gravity <= 14:
            self.jump_index = 5
        elif self.gravity > 14 and self.gravity <= 16:
            self.jump_index = 6
        elif self.gravity > 16:
            self.gravity = 7

        self.image = self.jump[self.jump_index]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.hitbox.bottom = self.rect.bottom

    def reset_jump(self):
        self.gravity = 0
        self.rect.y = 325

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "skull":
            self.image = pygame.image.load('resources/graveyard/Environment/Skull.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,0.78)
            y_pos = 200
        elif type == "cross":
            self.image = pygame.image.load('resources/graveyard/Environment/Headstone 03.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,0.5)
            y_pos = 329
        else:
            self.image = pygame.image.load('resources/graveyard/Environment/Headstone 02.png').convert_alpha()
            self.image = pygame.transform.scale(self.image,(76, 90))
            y_pos = 325

        self.rect = self.image.get_rect(midbottom = (randint(800, 1000), y_pos))

    def movement(self):
        self.rect.x -= 5 + int(score / 25)       

    def update(self):
        self.movement()
        self.destroy()

    def destroy(self):
        if self.rect.x < -100:
            self.kill()

# custom collide callback function
def collide_hit_rect(one, two):
    return one.hitbox.colliderect(two.rect)

def has_collided():
    if pygame.sprite.spritecollide(player.sprite, obstacles, False, collide_hit_rect):
        if not hit_channel.get_busy():
            hit_channel.play(hit_sfx)
        return True
    else:
        return False

def print_score():
    global score
    global current_time
    global text_alpha
    if game_running:
        current_time = pygame.time.get_ticks()
        score = (current_time - start_time) // 1000
    numbers_surf = my_numbers.render(f"health: {health} || score: {score}", True, 'grey')
    numbers_rect = numbers_surf.get_rect(topleft = (200, 20))
    screen.blit(numbers_surf, numbers_rect)
    if score > 2 and text_alpha > 0:
        text_alpha -= 2
        text_surf.set_alpha(text_alpha)


def ground_movement():
    if ground_rect.x < -599: ground_rect.x = 0

    ground_rect.x -= 5.000000001 + int(score / 25)
    second_rect = ground_surface.get_rect(topleft=(ground_rect.x+600, 325))
    screen.blit(ground_surface,ground_rect)
    screen.blit(ground_surface,second_rect)

def screen_movement():
    if bg_rect.x < -1333: bg_rect.x = 0
    if frame_counter % 5 == 0:
        bg_rect.x -= 1
    second_bgrect = bg_surface.get_rect(topleft = (bg_rect.x + 1334, 0))
    screen.blit(bg_surface,bg_rect)
    screen.blit(bg_surface, second_bgrect)

def check_difficulty():
    if score == 1:
        musik_channel.set_volume(0.6)
        pygame.time.set_timer(obstacle_event, 1200)
    elif score == 25:
        musik_channel.set_volume(0.7)
        pygame.time.set_timer(obstacle_event, 1000)
    elif score == 50:
        musik_channel.set_volume(0.8)
        pygame.time.set_timer(obstacle_event, 800)
    elif score == 75:
        musik_channel.set_volume(0.9)
        pygame.time.set_timer(obstacle_event, 700)
    elif score == 100:
        musik_channel.set_volume(1)
        pygame.time.set_timer(obstacle_event, 600)

# pygame window and game setup
screen_width = 600
screen_height = 400 
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
# el bucle de la aplicacion
running = True 
# Determina si estamos en lobby o jugando
game_running = False 
# Guardaremos el momento de inicio de partida para contar los segundos
# que lleva vivo, eso nos dará la puntuación
start_time = 0 
# Puntuación
score = 0
# Aqui guardaremos el tiempo actual y a este le restaremos start_time
# para calcular puntuacion
current_time = 0
# Contador de frames, lo usamos para decidir que frame pintamos en nuestras animaciones
frame_counter = 0

# player sprite based
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacles = pygame.sprite.Group()

# sounds
pygame.mixer.set_num_channels(4)
musik_channel = pygame.mixer.Channel(1)
jump_channel = pygame.mixer.Channel(2)
hit_channel = pygame.mixer.Channel(3)
hit_sfx = pygame.mixer.Sound('resources/sound/hit.mp3')
hit_sfx.set_volume(0.2)
epik_musik = pygame.mixer.Sound('resources/sound/epik_musik.mp3')

# fonts
my_font = pygame.font.Font('resources/fonts/Storm Gust.ttf', 50)
my_numbers = pygame.font.Font('resources/fonts/Sectar.otf', 20)
splash_font = pygame.font.Font('resources/fonts/Sectar.otf', 30)

# images
bg_image = 'resources/graveyard/Background/Background-Layer 00.png'
ground_image = 'resources/graveyard/Platfromer/Full_Ground.png'
start_bg_image = 'resources/StartScreen.png'

# deco ingame
bg_surface = pygame.image.load(bg_image).convert()
bg_rect = bg_surface.get_rect(topleft = (0, 0))
ground_surface = pygame.image.load(ground_image).convert()
ground_rect = ground_surface.get_rect(topleft = (0, 325))
text_alpha = 100
text_surf = my_font.render("The Graveyard", True, 'grey')
text_rect = text_surf.get_rect(midtop = (screen_width / 2, screen_height / 3))


#init screen
splash_bg_surf = pygame.image.load(start_bg_image).convert()
splash_text_surf = splash_font.render("Press Intro to Start", True, (148,141,157))
splash_text_rect = splash_text_surf.get_rect(center = (300, 300))
splash_text_alpha = 255
splash_text_alpha_vel = -4

# Creamos un evento personalizado y lo configuramos para que se ejecute
# cada 1200 milis. Será el generador de obstaculos
obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event, 1200)

# player


while running:
    # lista de eventos que hayan sucedido en el frame actual
    for event in pygame.event.get():
        # Evento de click en la X de la aplicacion
        if event.type == pygame.QUIT:
            running = False
        #game running
        if game_running :
            # evento personalizado generador de obstaculos
            if event.type == obstacle_event:
                gamble = randint(0, 5)
                if gamble < 1:
                    obstacles.add(Obstacle("pepepeeppeepepeppep"))
                elif gamble >= 1 and gamble < 3:
                    obstacles.add(Obstacle("skull"))
                else:
                    obstacles.add(Obstacle("cross"))
        #game not running
        else:
            # Se pulsa INTRO estando en el lobby
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    start_time = pygame.time.get_ticks()
                    game_running = True
                    health = 10

    if game_running:
        check_difficulty()
        # actualizamos el background y el marcador
        screen_movement()
        ground_movement()
        screen.blit(text_surf, text_rect)
        print_score()

        # updating sprites o updating groups
        player.update()
        player.draw(screen)
        obstacles.update()
        obstacles.draw(screen)

        # Comprobamos colisiones
        if has_collided():
            health -= 1 

        # Comprobamos si el player ha muerto
        if health <= 0:
            game_running = False
            musik_channel.stop()
    else:
        if not musik_channel.get_busy():
            musik_channel.play(epik_musik)
            musik_channel.set_volume(0.5)
        
        # imprimimos el background
        screen.blit(splash_bg_surf, (0,0))

        # imprimimos el texto "Press intro to start y lo animamos
        # en alpha haciendo que suba y baje el alpha
        screen.blit(splash_text_surf, splash_text_rect)
        splash_text_alpha += splash_text_alpha_vel
        splash_text_surf.set_alpha(splash_text_alpha)
        if splash_text_alpha < 50 or splash_text_alpha > 255: 
            splash_text_alpha_vel *= -1
        
        # Solo se cumple si ya hemos jugado una partida antes
        # Asi podemos usar la pantalla tanto para iniciar el juego
        # como despues de haber muerto
        if score > 0 :
            # Mostramos la puntuacion de la ultima partida
            splash_score_surf = my_numbers.render(f"Your last score was: {score}", True, (148,141,157))
            splash_score_rect = splash_score_surf.get_rect(center = (300, 250))
            screen.blit(splash_score_surf, splash_score_rect)

            # Borramos todos los obstaculos que hubiera
            obstacles.empty()
            player.sprite.reset_jump()
            pygame.time.set_timer(obstacle_event, 1200)
    
    # Siempre actualizamos el display a cada frame
    pygame.display.update()
    # Nuestra cuenta de frames
    frame_counter += 1
    # Limitacion a 60 FPS
    clock.tick(60) 

pygame.quit()