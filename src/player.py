import pygame

class Player:

    def __init__(self):
        self.posicion = (200,920)
        self.velocidad = 1
        self.surf = pygame.image.load('python\\jumpdude\\resources\\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\\3 Dude_Monster\\Dude_Monster.png').convert()
        self.surf = pygame.transform.scale(self.surf, (120,120))