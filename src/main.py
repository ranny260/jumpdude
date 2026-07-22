import pygame
from player import Player

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
running = True
clock = pygame.time.Clock()
bgimage = pygame.image.load('python\\jumpdude\\resources\\craftpix-891123-free-pixel-art-street-2d-backgrounds\\PNG\\City3\\Bright\\City3.png').convert()
player = Player()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    
    player.move(keys)
    
    screen.blit(bgimage, (0,0))
    screen.blit(player.surf, (player.posicion.x,player.posicion.y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()