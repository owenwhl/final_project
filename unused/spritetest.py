import pygame

pygame.init()
screen = pygame.display.set_mode((750, 750))
clock = pygame.time.Clock()
running = True
dt = 0

class CameraGroup(pygame.sprite.Group):
    def __init__(self,projectile):
        super().__init__(projectile)
        self.camera = ""
    
    def sprite_list(self):
        print(self.sprites())

class ProjectileGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def fire_bullet(self,bullet):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            print(f"{bullet.projectile_1} has been fired")

class Projectile_1(pygame.sprite.Sprite):
    def __init__(self,camera,group):
        super().__init__(camera,group)
        self.projectile_1 = "bullet_1.png"
        self.group = group
    
class Projectile_2(pygame.sprite.Sprite):
    def __init__(self,camera,group):
        super().__init__(camera,group)
        self.projectile_2 = "bullet_2.png"
        self.group = group

class Player(pygame.sprite.Sprite):
    def __init__(self,camera):
        super().__init__(camera)
        self.image = "player"

new_sprite = pygame.sprite.Sprite
projectile_group = ProjectileGroup()
camera = CameraGroup(projectile_group)
player = Player(camera)

projectile_1 = Projectile_1(camera,projectile_group)
projectile_2 = Projectile_2(camera,projectile_group)

fire_rate = 500
fire_bullet = pygame.USEREVENT + 1
pygame.time.set_timer(fire_bullet, fire_rate)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == fire_bullet:
            projectile_group.fire_bullet(projectile_1)
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()
