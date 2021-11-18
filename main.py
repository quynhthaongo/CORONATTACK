import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 500))
clock = pygame.time.Clock()
FPS = 120

#color command
red = (180,0,40)
red1 = (255,200,200)
red2 = (100,0,0)
brown = (250, 40, 40)
brownred = (120,20,20)
black = (0,0,0)
purple = (150, 0, 150)
pink = (255, 20, 150)
white = (255, 255, 255)

pygame.display.set_caption("Coronie Journey")
keys = pygame.key.get_pressed()

artery = pygame.image.load('arteries.png')
artery = pygame.transform.scale(artery, (500,300))
coronie = pygame.image.load('coronie61.png')
coronie = pygame.transform.scale(coronie, (70, 70))
bcell = pygame.image.load('bcell5.png')
bcell = pygame.transform.scale(bcell, (90, 100))
tcell = pygame.image.load('tcell5.png')
tcell = pygame.transform.scale(tcell, (90,100))
nkcell = pygame.image.load('nkcell5.png')
nkcell = pygame.transform.scale(nkcell, (100, 100))
neutrophil = pygame.image.load('neutrophil.png')
neutrophil = pygame.transform.scale(neutrophil, (70, 70))
mucus = pygame.image.load('mucus3.png')
mucus = pygame.transform.scale(mucus, (70, 70))
mucusr = pygame.image.load('mucusrotate.png')
mucusr = pygame.transform.scale(mucusr, (70, 70))
fire = pygame.image.load('fire.png')
fire = pygame.transform.scale(fire, (200,50))
dendritic = pygame.image.load('dendritic.png')
dendritic = pygame.transform.scale(dendritic, (70, 70))
macrophage = pygame.image.load('macrophage2.png')
macrophage = pygame.transform.scale(macrophage, (70, 70))

coronie_rect = coronie.get_rect(center=(100, 250))
bcell_rect = bcell.get_rect(center=(600,220))
tcell_rect = tcell.get_rect(center=(500,300))
nkcell_rect = nkcell.get_rect(center=(400,250))
mucus_rect = mucus.get_rect(center=(400,320))
mucusr_rect = mucusr.get_rect(center=(230,190))
#fire_rect = fire.get_rect()#center=(250,250))

coronie_movey = 250

running = True
while running:
    screen.fill((black))
    screen.blit(artery, (-50, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                coronie_movey = coronie_movey
                coronie_movey = coronie_movey - 10
            if event.key == pygame.K_DOWN:
                coronie_movey = coronie_movey
                coronie_movey = coronie_movey + 10
            if event.key == pygame.K_SPACE:
                fire_rect = fire.get_rect()
                fire_rect.centery = coronie_rect.centery
                fire_rect.centerx = 200
                screen.blit(fire, fire_rect)
                pygame.display.update()
                if fire_rect.colliderect(bcell_rect):
                    bcell_rect.centerx = -100
                if fire_rect.colliderect(tcell_rect):
                    tcell_rect.centerx = -100
                if fire_rect.colliderect(nkcell_rect):
                    nkcell_rect.centerx = -100

        #if coronie_rect.colliderect(mucus_rect):
        #    running = False
        #if coronie_rect.colliderect(mucusr_rect):
        #    running = False
    if coronie_rect.top < 160 or coronie_rect.bottom > 340:
        running = False
    if coronie_rect.colliderect(bcell_rect):
        pygame.time.delay(500)
        running = False
    if coronie_rect.colliderect(tcell_rect):
        pygame.time.delay(500)
        running = False
    if coronie_rect.colliderect(nkcell_rect):
        pygame.time.delay(500)
        running = False


#class Enemies:
#    def __init__(self):
#    pass


#def Enemies_spawn():
#    x = random.randint(400, 800)
#    y = random.randint(200, 300)
#    new_enemies = Enemies((x, y))
#def Mucus_spawn():
#    x = random.randint(400,800)
#    new_mucus = Mucus((x, 400))




    coronie_movey = coronie_movey
    coronie_rect.centery = coronie_movey
    mucusr_rect.centerx = mucusr_rect.centerx - 1
    mucus_rect.centerx = mucus_rect.centerx - 1
    nkcell_rect.centerx = nkcell_rect.centerx - 1
    bcell_rect.centerx = bcell_rect.centerx - 1
    tcell_rect.centerx = tcell_rect.centerx - 1
    #screen.fill((black))
    #screen.blit(artery, (-50,100))
    #screen.blit(mucus, mucus_rect)
    #screen.blit(mucusr, mucusr_rect)
    screen.blit(nkcell, nkcell_rect)
    screen.blit(bcell, bcell_rect)
    screen.blit(tcell,tcell_rect)
    screen.blit(coronie, coronie_rect)
    #screen.blit(fire, fire_rect)

    pygame.display.update()
    clock.tick(FPS)

