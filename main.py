import pygame
import random
import sys

# General setting of game
pygame.init()
screen = pygame.display.set_mode((400, 500))
clock = pygame.time.Clock()
FPS = 90

# Color command
black = (0,0,0)

pygame.display.set_caption("Coronie Journey")
keys = pygame.key.get_pressed()

# Loading image
# Background
artery = pygame.image.load('arteries1.png')
artery = pygame.transform.scale(artery, (500,300))
artery2 = pygame.image.load('arteries2.png')
artery2 = pygame.transform.scale(artery2, (500,300))
artery_x_pos = 0

# Player - Coronie
# Load image, scale, put in to rectangle, declare motion variables
coronie = pygame.image.load('coronie61.png')
coronie = pygame.transform.scale(coronie, (70, 70))
coronie_rect = coronie.get_rect(center=(100, 230))
coronie_movey = 250
coronie_movey_change = 0
coroniehit = pygame.image.load('coronie9.png')
coroniehit = pygame.transform.scale(coroniehit, (70, 70))

# Coronie's weapon - flame
# Load image, scale, put into rectangle, declare motion variables
fire = pygame.image.load('purpleflame.png')
fire = pygame.transform.scale(fire, (70, 50))
fire_rect = fire.get_rect(center=(-500,-500))
fire_movex = 0
shock = pygame.image.load('electricshock1.png')
shock = pygame.transform.scale(shock, (100, 100))
shock_rect = shock.get_rect()

# Physical Barrier: Mucus
# Load image, scale, create list of mucus, create event to spawn mucus & set event timer
# Declare list of random positions & distance between top mucus and bottom mucus
mucus_surface = pygame.image.load('mucus3.png')
mucus_surface = pygame.transform.scale(mucus_surface, (60, 70))
mucus_list = []
SPAWNMUCUS = pygame.USEREVENT
mucus_posx = [600, 900]
mucus_distance = [-180,-110,100,190]
pygame.time.set_timer(SPAWNMUCUS,7000)

# Cellcurity (Enemies): Bcell, Tcell, NKcell
# Load image, scale, create lists of enemies, Create event to spawn enemies & set timer
# List of random position & random enemies type
bcell_surface = pygame.image.load('bcell5.png')
bcell_surface = pygame.transform.scale(bcell_surface, (90, 100))
tcell_surface = pygame.image.load('tcell3.png')
tcell_surface = pygame.transform.scale(tcell_surface, (90, 100))
nkcell_surface = pygame.image.load('nkcell5.png')
nkcell_surface = pygame.transform.scale(nkcell_surface, (100, 100))
neutrophil_surface = pygame.image.load('neutrophil.png')
neutrophil_surface = pygame.transform.scale(neutrophil_surface, (70, 70))
bcell_list = []
tcell_list = []
nkcell_list = []
enemie_posx = [700,1000]
enemie_posy = [230,250,270]
enemie_type = [1, 2, 3]
spawn_speed = 3000
SPAWNENEMIE = pygame.USEREVENT
pygame.time.set_timer(SPAWNENEMIE,spawn_speed)

# Draw 3 artery surface next to each other, with the middle one being the mirrored of the others
# This is to create smooth animation of the artery moving continuous
# Another function later on would move these three artery left ward and spawn them when reach the end
def draw_artery():
    screen.blit(artery, (artery_x_pos, 100))
    screen.blit(artery2, (artery_x_pos + 500, 100))
    screen.blit(artery, (artery_x_pos + 1000, 100))

# functions to create new mucus, move the mucus, and to draw the new mucus on the screen
def create_mucus():
    random_mucus = random.choice(mucus_posx)
    random_mucusdistance = random.choice(mucus_distance)
    bottom_mucus = mucus_surface.get_rect(center=(random_mucus, 330))
    top_mucus = mucus_surface.get_rect(center=(random_mucus + random_mucusdistance, 190))
    return bottom_mucus, top_mucus

def move_mucuss(mucuss):
    for mucus in mucuss:
        mucus.centerx = mucus.centerx - 2.5
    return mucuss

# If y center of mucus is above, it would be flipped, become the top mucus.
# Otherwise, it would stay at the bottom
def draw_mucuss(mucuss):
    for mucus in mucuss:
        if mucus.centery >= 310:
            screen.blit(mucus_surface, mucus)
        elif mucus.centery <= 200:
            flip_mucus = pygame.transform.flip(mucus_surface,False,True)
            screen.blit(flip_mucus, mucus)

# function to create enemie, move enemie and draw new enemie to the screen
def create_bcell():
    random_bcellx = random.choice(enemie_posx)
    random_bcelly = random.choice(enemie_posy)
    bcell = bcell_surface.get_rect(center=(random_bcellx, random_bcelly))
    return bcell
def create_tcell():
    random_tcellx = random.choice(enemie_posx)
    random_tcelly = random.choice(enemie_posy)
    tcell = tcell_surface.get_rect(center=(random_tcellx, random_tcelly))
    return tcell
def create_nkcell():
    random_nkcellx = random.choice(enemie_posx)
    random_nkcelly = random.choice(enemie_posy)
    nkcell = nkcell_surface.get_rect(center=(random_nkcellx, random_nkcelly))
    return nkcell

# I wanted to make enemies move faster as the game continue. Therefore, I use game ticks * 0.0001 as their speed
def move_bcell(bcells):
    for bcell in bcells:
        bcell.centerx = bcell.centerx - 0.0001 * pygame.time.get_ticks()
    return bcells
def move_tcell(tcells):
    for tcell in tcells:
        tcell.centerx = tcell.centerx - 0.00005 * pygame.time.get_ticks()
    return tcells
def move_nkcell(nkcells):
    for nkcell in nkcells:
        nkcell.centerx = nkcell.centerx - 0.00015 * pygame.time.get_ticks()
    return nkcells

def draw_bcell(bcells):
    for bcell in bcells:
        screen.blit(bcell_surface, bcell)
def draw_tcell(tcells):
    for tcell in tcells:
        screen.blit(tcell_surface, tcell)
def draw_nkcell(nkcells):
    for nkcell in nkcells:
        screen.blit(nkcell_surface, nkcell)

# Function to check for collision

# Move out of game bound:
def collision_artery():
    if coronie_rect.top < 160 or coronie_rect.bottom > 350:
        game_over()
        pygame.quit()
        sys.exit()

# Collision with mucus:
# Since Coronie is round-shape, but the only way to check for collision in pygame is using rectangle
# I create another smaller rectangle that fit inside Coronie's circle
# and check for collision with mucus using that rectangle
# And then, I check for collision of the original Coronie's rectangle mid top and mid bottom
# with the mid top/ mid bottom of the mucus. That is the best way I could think of
# to make it looks as if the collision of the "circle" was being checked, while I just use rectangle
def collisions(mucuss):
    for mucus in mucuss:
        if smallrect.colliderect(mucus):
            game_over()
            running = False
            pygame.quit()
            sys.exit()
        if coronie_rect.colliderect(mucus):
            if coronie_rect.centerx == mucus.centerx:
                game_over()
                running = False
                pygame.quit()
                sys.exit()

# Check for collision between Coronie and enemies
# as well as enemies and flame. When flame hit them, they will disappear (move out of bound)
# I want to make flame only counted as "hit" if it reach the center portions of the enemies
# Therefore, I check for collision, and if there is collision,
# check if the x center of flame is within the central range of enemie
def collision(bcells):
    for bcell in bcells:
        if coronie_rect.colliderect(bcell):
            game_over()
            running = False
            pygame.quit()
            sys.exit()
        if fire_rect.colliderect(bcell):
            if fire_rect.centerx >= (bcell.top + 15) and fire_rect.centerx <= (bcell.bottom - 15):
                shock_rect.centerx = fire.rect.centerx
                shock_rect.centery = fire.rect.centery
                screen.blit(shock,shock_rect)
                pygame.display.update()
                bcell.centerx = -100

def collision(tcells):
    for tcell in tcells:
        if coronie_rect.colliderect(tcell):
            game_over()
            running = False
            pygame.quit()
            sys.exit()
        if fire_rect.colliderect(tcell):
            if fire_rect.centerx >= (tcell.top + 15) and fire_rect.centerx <= (tcell.bottom - 15):
                tcell.centerx = -100

def collision(nkcells):
    for nkcell in nkcells:
        if coronie_rect.colliderect(nkcell):
            game_over()
            running = False
            pygame.quit()
            sys.exit()
        if fire_rect.colliderect(nkcell):
            if fire_rect.centerx >= (nkcell.top + 15) and fire_rect.centerx <= (nkcell.bottom - 15):
                nkcell.centerx = -100

# A function of the animation of "Game Over" event. Coronie's face will turn in to crying face
# A "GAME OVER" board will appear on the screen and exit the game
def game_over():
    screen.blit(coroniehit, coronie_rect)
    pygame.display.update()
    pygame.time.delay(500)
    gameover = pygame.image.load('gameover.png ')
    gameover = pygame.transform.scale(gameover, (200,200))
    gameover_rect = gameover.get_rect(center=(200,250))
    screen.blit(gameover, gameover_rect)
    pygame.display.update()
    pygame.time.delay(500)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

# function to control Coronie's movement: Up & Down, shooting flame
# if key is holded, Coronie will move faster.
# If not, Coronie will continue to "float" with the former direction,
# since Coronie is floating in the arteries, surrounded by blood
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                coronie_movey_change = -1.5
            if event.key == pygame.K_DOWN:
                coronie_movey_change = 1.5
            if event.key == pygame.K_SPACE:
                fire_rect.centery = coronie_rect.centery
                fire_rect.centerx = 170
                fire_movex = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                coronie_movey_change = -0.5
            if event.key == pygame.K_DOWN:
                coronie_movey_change = 0.5

# Adding new mucus to the mucus list to keep spawning
        if event.type == SPAWNMUCUS:
            mucus_list.extend(create_mucus())

# Randomly choose with type of enemie to spawn, and add them to spawning list
        if event.type == SPAWNENEMIE:
            choose_enemie = random.choice(enemie_type)
            if choose_enemie == 1:
                bcell_list.append(create_bcell())
            elif choose_enemie == 2:
                tcell_list.append(create_tcell())
            elif choose_enemie == 3:
                nkcell_list.append(create_nkcell())

    screen.fill((black))

# This is the small rectangle to check for collision (mentioned above)
    smallrect = pygame.draw.rect(screen, black, (coronie_rect.centerx - 25, coronie_rect.centery - 25, 50, 50))

# Make the 3 artery surfaces move to the left and spawn them again when they reach the end
    artery_x_pos = artery_x_pos
    artery_x_pos = artery_x_pos - 1.5
    draw_artery()
    if artery_x_pos <= -1000:
        artery_x_pos = 0

# Display coronie's position
    coronie_movey = coronie_movey
    coronie_movey = coronie_movey + coronie_movey_change
    coronie_rect.centery = coronie_movey
    screen.blit(coronie, coronie_rect)

# Display the flame, make sure that it is shot from Coronie's center.
# The flame will leave and move to the end of bound, where is would be spawn outside and recall again
    if fire_rect.centerx >= 400:
        fire_movex = 0
        fire_rect.centery = 2000
        fire_rect.centerx = 2000
    fire_rect.centerx = fire_rect.centerx + fire_movex
    screen.blit(fire, fire_rect)

# Adding new position of mucus and enemie to the list, and draw mucus and enemie from that list
# In order to create sequential event, I separate timing into which the first few scene would only spawn mucus
# And later on would spawn enemies only
    if pygame.time.get_ticks() <= 9999:
        mucus_list = move_mucuss(mucus_list)
        draw_mucuss(mucus_list)
    elif pygame.time.get_ticks() >= 1000:
        bcell_list = move_bcell(bcell_list)
        draw_bcell(bcell_list)
        tcell_list = move_tcell(tcell_list)
        draw_tcell(tcell_list)
        nkcell_list = move_nkcell(nkcell_list)
        draw_nkcell(nkcell_list)

# Call out the function to check for collision
    collision_artery()
    collisions(mucus_list)
    collision(bcell_list)
    collision(tcell_list)
    collision(nkcell_list)

    pygame.display.update()
    clock.tick(FPS)