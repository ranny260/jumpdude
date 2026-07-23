import pygame

class Player:

    def __init__(self):
        self.posicion = pygame.Vector2(200,920)
        self.velocidad = 2
        self.surf = pygame.image.load('resources\\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\\3 Dude_Monster\\Dude_Monster.png').convert()
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

    def run(self, index):
        anim_run = pygame.image.load('resources\\craftpix-net-622999-free-pixel-art-tiny-hero-sprites\\3 Dude_Monster\\Dude_Monster_Run_6.png')
        frames = []
        frames.append(anim_run.subsurface(pygame.Rect(0, 0, 32, 32)))
        frames.append(anim_run.subsurface(pygame.Rect(32, 0, 32, 32)))
        frames.append(anim_run.subsurface(pygame.Rect(64, 0, 32, 32)))
        frames.append(anim_run.subsurface(pygame.Rect(96, 0, 32, 32)))
        frames.append(anim_run.subsurface(pygame.Rect(128, 0, 32, 32)))
        frames.append(anim_run.subsurface(pygame.Rect(160, 0, 32, 32)))

        self.surf = frames[index].convert()
        self.surf = pygame.transform.scale(self.surf, (120,120))
