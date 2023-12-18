import pygame
import time
import math

def blit_rotate_center(surface, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center= image.get_rect(center= top_left).center)
    surface.blit(rotated_image, new_rect.topleft)

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,max_vel,rotation_vel):
        super().__init__()
        ship_1 = pygame.image.load('graphics/ship_up1.png').convert_alpha()
        ship_1 = pygame.transform.scale_by(ship_1, 5)
        ship_2 = pygame.image.load('graphics/ship_up2.png').convert_alpha()
        ship_2 = pygame.transform.scale_by(ship_2, 5)
        ship_still = pygame.image.load('graphics/ship_up0.png').convert_alpha()
        ship_still = pygame.transform.scale_by(ship_still, 5)
        self.ship_state = [ship_1, ship_2, ship_still]
        self.ship_index = 0

        self.image = self.ship_state[self.ship_index]
        self.rect = self.image.get_rect(midbottom = (0,0))

        self.angle = 0
        self.rotation_vel = rotation_vel
        self.max_vel = max_vel

        self.position = pygame.Vector2((x,y))
        self.velocity = 0
        # self.move_direction = pygame.Vector2()
        self.acceleration = 0.1

    def animate_ship(self,moved=False):
        if moved:
            self.ship_index += 0.1
            if self.ship_index > 2: self.ship_index = 0
            self.image = self.ship_state[int(self.ship_index)]
        else:
            self.image = self.ship_state[2]

    def move_player(self):
        radians = math.radians(self.angle)

        vertical = math.cos(radians) * self.velocity
        horizontal = math.sin(radians) * self.velocity

        self.position.x -= horizontal
        self.position.y -= vertical

    def increase_speed(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_vel)
        self.move_player()

    def reduce_speed(self):
        self.velocity = max(self.velocity - self.acceleration/2, 0)
        self.move_player()

    def rotate(self,left=False,right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def update(self):
        blit_rotate_center(screen, self.image, self.position, self.angle)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720))
running = True
dt = 0
ground_surf = pygame.image.load("graphics/space.jpg").convert_alpha()
ground_surf = pygame.transform.scale_by(ground_surf, 3)
ground_rect = ground_surf.get_rect(center = (640,360))
ship = Player(640,360,10,3)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('white')
    screen.blit(ground_surf,ground_rect)
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_d]:
        ship.rotate(right=True)
    if keys[pygame.K_a]:
        ship.rotate(left=True)
    if keys[pygame.K_w]:
        moved = True
        ship.increase_speed()
        ship.animate_ship(moved)
    if not moved:
        ship.reduce_speed()
        ship.animate_ship(moved)

    ship.update()

    pygame.display.update()
    dt = clock.tick(60) / 1000

pygame.quit()

