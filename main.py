import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 500))
clock = pygame.time.Clock()
FPS = 90

# color command
black = (0,0,0)

pygame.display.set_caption("Coronie Journey")
keys = pygame.key.get_pressed()

# Loading image
artery = pygame.image.load('arteries1.png')
artery = pygame.transform.scale(artery, (500,300))
artery2 = pygame.image.load('arteries2.png')
artery2 = pygame.transform.scale(artery2, (500,300))
artery_x_pos = 0

coronie = pygame.image.load('coronie61.png')
coronie = pygame.transform.scale(coronie, (70, 70))
coronie_rect = coronie.get_rect(center=(100, 250))
coronie_movey = 250

# Create event to spawn mucus
mucus_surface = pygame.image.load('mucus3.png')
mucus_surface = pygame.transform.scale(mucus_surface, (70, 70))
mucus_list = []
SPAWNMUCUS = pygame.USEREVENT
mucus_posx = [600, 800]
mucus_distance = [-120,120]
pygame.time.set_timer(SPAWNMUCUS,2400)

# Create event to spawn enemie
bcell_surface = pygame.image.load('bcell5.png')
bcell_surface = pygame.transform.scale(bcell_surface, (90, 100))
tcell_surface = pygame.image.load('tcell5.png')
tcell_surface = pygame.transform.scale(tcell_surface, (90, 100))
nkcell_surface = pygame.image.load('nkcell5.png')
nkcell_surface = pygame.transform.scale(nkcell_surface, (100, 100))
neutrophil_surface = pygame.image.load('neutrophil.png')
neutrophil_surface = pygame.transform.scale(neutrophil_surface, (70, 70))
enemie_list = []
SPAWNENEMIE = pygame.USEREVENT
enemie_posx = [700,1000]
enemie_posy = [190,250,310]
enemie_type = [1, 2, 3]
pygame.time.set_timer(SPAWNENEMIE,3000)

# Draw 3 artery surface next to each other
def draw_artery():
    screen.blit(artery, (artery_x_pos, 100))
    screen.blit(artery2, (artery_x_pos + 500, 100))
    screen.blit(artery, (artery_x_pos + 1000, 100))

# functions to create new mucus, move the mucus, and to draw the new mucus on the screen
def create_mucus():
    random_mucus = random.choice(mucus_posx)
    random_mucusdistance = random.choice(mucus_distance)
    bottom_mucus = mucus_surface.get_rect(center=(random_mucus, 320))
    top_mucus = mucus_surface.get_rect(center=(random_mucus + random_mucusdistance, 190))
    return bottom_mucus, top_mucus

def move_mucuss(mucuss):
    for mucus in mucuss:
        mucus.centerx = mucus.centerx - 2
    return mucuss

def draw_mucuss(mucuss):
    for mucus in mucuss:
        if mucus.centery >= 310:
            screen.blit(mucus_surface, mucus)
        elif mucus.centery <= 200:
            flip_mucus = pygame.transform.flip(mucus_surface,False,True)
            screen.blit(flip_mucus, mucus)

# function to create enemie, move enemie and draw new enemie to the screen
def create_enemie():
    random_enemiex = random.choice(enemie_posx)
    random_enemiey = random.choice(enemie_posy)
    bcell_enemie = bcell_surface.get_rect(center=(random_enemiex, random_enemiey))
    tcell_enemie = tcell_surface.get_rect(center=(random_enemiex, random_enemiey))
    nkcell_enemie = nkcell_surface.get_rect(center=(random_enemiex, random_enemiey))
    return bcell_enemie, tcell_enemie, nkcell_enemie

def move_enemie(enemies):
    for enemie in enemies:
        enemie.centerx = enemie.centerx - 2
    return enemies

def draw_enemie(enemies):
    for enemie in enemies:
        random_enemietype = random.choice(enemie_type)
        if random_enemietype == 1:
            screen.blit(bcell_surface, enemie)
        elif random_enemietype == 2:
            screen.blit(tcell_surface, enemie)
        elif random_enemietype == 3:
            screen.blit(nkcell_surface, enemie)

# function to check for collision
# i am still working on how to successfully test for collision, but it will generally look like this
def collision():
    if coronie_rect.top < 160 or coronie_rect.bottom > 340:
        running = False
    if coronie_rect.colliderect(bottom_mucus or top_mucus):
        running = False
    if coronie_rect.colliderect(bcell_enemie):
        pygame.time.delay(500)
        running = False
    if coronie_rect.colliderect(tcell_enemie):
       pygame.time.delay(500)
       running = False
    if coronie_rect.colliderect(nkcell_enemie):
       pygame.time.delay(500)
       running = False


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # function to control coronie's movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                coronie_movey = coronie_movey
                coronie_movey = coronie_movey - 10
            if event.key == pygame.K_DOWN:
                coronie_movey = coronie_movey
                coronie_movey = coronie_movey + 10
    # creating fire attack for coronie:
            if event.key == pygame.K_SPACE:
                fire = pygame.image.load('fire.png')
                fire = pygame.transform.scale(fire, (200, 50))
                fire_rect = fire.get_rect()
                fire_rect.centery = coronie_rect.centery
                fire_rect.centerx = 200
                screen.blit(fire, fire_rect)
                pygame.display.update()

    # adding new mucus to the mucus list to keep spawning
        if event.type == SPAWNMUCUS:
            mucus_list.extend(create_mucus())
        if event.type == SPAWNENEMIE:
            enemie_list.extend(create_enemie())

    screen.fill((black))

# Make the 3 artery surfaces move to the left and spawn them again at the end
    artery_x_pos = artery_x_pos
    artery_x_pos = artery_x_pos - 1
    draw_artery()
    if artery_x_pos <= -1000:
        artery_x_pos = 0

# Display coronie's position
    coronie_movey = coronie_movey
    coronie_rect.centery = coronie_movey
    screen.blit(coronie, coronie_rect)

# Adding new position of mucus and enemie to the list, and draw mucus and enemie from that list
    mucus_list = move_mucuss(mucus_list)
    draw_mucuss(mucus_list)

    enemie_list = move_enemie(enemie_list)
    draw_enemie(enemie_list)

    pygame.display.update()
    clock.tick(FPS)
    collision()
