import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 400))
running = True
clock = pygame.time.Clock()
r = 1
g = 255
b = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    screen.fill((r, g, b))
    pygame.display.flip()
    clock.tick(1)

pygame.quit()