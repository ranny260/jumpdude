import pygame

class Player:

    def __init__(self):
        self.posicion = pygame.Vector2(200,920)
        self.velocidad = 2
        self.surf = pygame.image.load('python\\jumpdude\\resources\\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\\3 Dude_Monster\\Dude_Monster.png').convert()
        self.surf = pygame.transform.scale(self.surf, (120,120))
    
    def move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.posicion.x += self.velocidad
        if keys[pygame.K_LEFT]:
            self.posicion.x -= self.velocidad
        if keys[pygame.K_UP]:
            self.posicion.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.posicion.y += self.velocidad