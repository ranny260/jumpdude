import pygame
from random import randint

def print_score():
    global score
    global current_time
    if game_running:
        current_time = pygame.time.get_ticks()
        score = (current_time - start_time) // 1000
    numbers_surf = my_numbers.render(f"health: {health} || score: {score}", True, 'grey')
    numbers_rect = numbers_surf.get_rect(topleft = (200, 60))
    screen.blit(numbers_surf, numbers_rect)

def obstacle_movement(obs_list):
    return_list = []
    if obs_list:
        for obs in obs_list:
            obs.x -= 5
            if obs.x > -100:
                return_list.append(obs)
                if obs.bottom > 325:
                    screen.blit(cross_surf, obs)
                elif obs.bottom < 201:
                    screen.blit(skull_surf, obs)
                else:
                    screen.blit(obstacle_surf, obs)
                
                pygame.draw.rect(screen, 'red', obs, 1)
        return return_list
    else:
        return []

def has_collided(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return True
    return False

# pygame window and game setup
screen_width = 600
screen_height = 400 
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
game_running = False
start_time = 0
score = 0

# fonts
my_font = pygame.font.Font('resources\\fonts\\storm_gust\\Storm Gust.ttf', 50)
my_numbers = pygame.font.Font('resources\\fonts\\Sectar.otf', 20)
splash_font = pygame.font.Font('resources\\fonts\\Sectar.otf', 30)

# images
bg_image = 'resources\\graveyard\\Background\\Background-Layer 00.png'
ground_image = 'resources\\graveyard\\Platfromer\\Full_Ground.png'
obstacle_image = 'resources\\graveyard\\Environment\\Headstone 02.png'
cross_image = 'resources\\graveyard\\Environment\\Headstone 03.png'
skull_image = 'resources\\graveyard\\Environment\\Skull.png'
player_image = 'resources\\tiny-hero\\1 Pink_Monster\\Pink_Monster.png'
start_bg_image = 'resources\\StartScreen.png'

# deco ingame
bg_surface = pygame.image.load(bg_image).convert()
ground_surface = pygame.image.load(ground_image).convert()
text_surf = my_font.render("Phase One: The Graveyard", True, 'grey')
text_rect = text_surf.get_rect(midtop = (screen_width / 2, 10))

#init screen
splash_bg_surf = pygame.image.load(start_bg_image).convert()
splash_text_surf = splash_font.render("Press Intro to Start", True, (148,141,157))
splash_text_rect = splash_text_surf.get_rect(center = (300, 300))
splash_text_alpha = 255
splash_text_alpha_vel = -4

# obstacles
obstacle_surf = pygame.image.load(obstacle_image).convert_alpha()
obstacle_surf = pygame.transform.scale(obstacle_surf,(76, 90))
cross_surf = pygame.image.load(cross_image).convert_alpha()
cross_surf = pygame.transform.rotozoom(cross_surf,0,0.5)
skull_surf = pygame.image.load(skull_image).convert_alpha()
skull_surf = pygame.transform.rotozoom(skull_surf,0,0.78)
obstacle_list = []

obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event, 1200)

# player
player_surf = pygame.image.load(player_image).convert_alpha()
player_surf = pygame.transform.scale(player_surf, (50,80))
player_rect = player_surf.get_rect(midbottom = (100,325))
player_gravity = 0
health = 10
jumps = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_running :
            #game running
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 325:
                    player_gravity = - 20 
            if event.type == obstacle_event:
                gamble = randint(0, 3)
                if gamble < 1:
                    obstacle_list.append(obstacle_surf.get_rect(midbottom = (randint(800, 1000), 325)))
                elif gamble >= 1 and gamble < 2:
                    obstacle_list.append(skull_surf.get_rect(midbottom = (randint(800, 1000), 200)))
                else:
                    obstacle_list.append(cross_surf.get_rect(midbottom = (randint(800, 1000), 329)))

        else:
            #game not running
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    start_time = pygame.time.get_ticks()
                    #obstacle_rect.left = screen_width + 50
                    game_running = True
                    health = 10
                    jumps = 0

    if game_running:
        screen.blit(bg_surface,(0,0))
        screen.blit(ground_surface,(0,325))
        screen.blit(text_surf, text_rect)

        #obstacle movement
        obstacle_list = obstacle_movement(obstacle_list)
        # obstacle_rect.x -= 5
                
        # if obstacle_rect.right < 0:
        #     jumps += 1
        #     obstacle_rect.left = screen_width + 50
        
        # screen.blit(obstacle_surf, obstacle_rect)
        print_score()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 325:
            player_rect.bottom = 325

        screen.blit(player_surf, player_rect)
        pygame.draw.rect(screen, 'red', player_rect, 1)
        
        # if player_rect.colliderect(obstacle_rect):
        #     health -= 1 
        if has_collided(player_rect, obstacle_list):
            health -= 1 
              
        if health <= 0:
            game_running = False
    else:
        obstacle_list = []
        player_gravity = 0
        player_rect.bottom = 325
        screen.fill((25, 10, 20))
        screen.blit(splash_bg_surf, (0,0))
        screen.blit(splash_text_surf, splash_text_rect)
        splash_text_alpha += splash_text_alpha_vel
        splash_text_surf.set_alpha(splash_text_alpha)
        if splash_text_alpha < 50 or splash_text_alpha > 255: splash_text_alpha_vel *= -1
        if score > 0 :
            splash_score_surf = my_numbers.render(f"Your last score was: {score}", True, (148,141,157))
            splash_score_rect = splash_score_surf.get_rect(center = (300, 250))
            screen.blit(splash_score_surf, splash_score_rect)

    pygame.display.update()

    clock.tick(60)  # limits FPS to 60

pygame.quit()