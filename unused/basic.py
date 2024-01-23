import pygame
import math

pygame.init()
screen = pygame.display.set_mode((750, 750))
clock = pygame.time.Clock()
game_timer = pygame.time.Clock()
running = True
dt = 0

tick = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('white')
    
    dt = clock.tick(60) / 1000

pygame.quit()
