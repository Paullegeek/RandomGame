import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obama vs Trump: Melon Wars")

# Couleurs
WHITE = (255, 255, 255)

# Charger les images
background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

obama_img = pygame.image.load("obama.png")
obama_img = pygame.transform.scale(obama_img, (64, 64))

melon_img = pygame.image.load("melon.png")
melon_img = pygame.transform.scale(melon_img, (32, 32))

trump_img = pygame.image.load("trump.png")
trump_img = pygame.transform.scale(trump_img, (64, 64))

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obama_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

class Melon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = melon_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = trump_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

    def update(self):
        self.rect.y += 3
        if self.rect.top > HEIGHT:
            self.kill()

# Groupes de sprites
player = Player()
melons = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

# Ajouter des ennemis
def spawn_enemy():
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)

# Boucle principale
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            melon = Melon(player.rect.centerx, player.rect.top)
            melons.add(melon)
            all_sprites.add(melon)

    # Mise à jour
    all_sprites.update()

    # Gestion des collisions
    for melon in melons:
        hits = pygame.sprite.spritecollide(melon, enemies, True)
        if hits:
            melon.kill()

    # Ajouter des ennemis périodiquement
    if random.randint(1, 50) == 1:
        spawn_enemy()

    # Dessiner l'image de fond
    screen.blit(background_img, (0, 0))

    # Dessiner tous les sprites par-dessus
    all_sprites.draw(screen)
    
    # Rafraîchir l'écran
    pygame.display.flip()

    # Contrôle de la vitesse
    clock.tick(60)

pygame.quit()
