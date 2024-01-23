import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((750, 750))
clock = pygame.time.Clock()
running = True
dt = 0

rock = pygame.image.load("graphics/asteroid.png")
rock_scale = (100, 100)
rock = pygame.transform.scale(rock, rock_scale)
rock_pos = pygame.Vector2(random.randrange(0,650), random.randrange(0,650))

accel_left = 0
accel_right = 0
accel_up = 0
accel_down = 0


player = pygame.image.load("graphics/box.png")
player_scale = (135 / 4, 160 / 4)
player = pygame.transform.scale(player, player_scale)
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    screen.fill("black")
    screen.blit(player, player_pos)
    screen.blit(rock, rock_pos)

    # move up
    if keys[pygame.K_w]:
        player_pos.y -= (100 + accel_up) * dt
        if accel_up < 1000:
            accel_up += 20
    else:
        if accel_up != 0:
            player_pos.y -= (accel_up) * dt
            accel_up -= 20

    # move down
    if keys[pygame.K_s]:
        player_pos.y += (100 + accel_down) * dt
        if accel_down < 1000:
            accel_down += 20
    else:
        if accel_down != 0:
            player_pos.y += (accel_down) * dt
            accel_down -= 20

    # move left
    if keys[pygame.K_a]:
        player_pos.x -= (100 + accel_left) * dt
        if accel_left < 1000:
            accel_left += 20
    else:
        if accel_left != 0:
            player_pos.x -= (accel_left) * dt
            accel_left -= 20

    # move right
    if keys[pygame.K_d]:
        player_pos.x += (100 + accel_right) * dt
        if accel_right < 1000:
            accel_right += 20
    else:
        if accel_right != 0:
            player_pos.x += (accel_right) * dt
            accel_right -= 20

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()