import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100,100))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center = (400,400))

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def create_bullet(self):
        return Bullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = pygame.Surface((50,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = (pos_x,pos_y))

    def update(self):
        self.rect.x += 5

        if self.rect.x >= 600:
            self.kill()

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
running = True
pygame.mouse.set_visible(False)

player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

bullet_group = pygame.sprite.Group()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_group.add(player.create_bullet())


    screen.fill((30,30,30))

    bullet_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    bullet_group.update()



    pygame.display.flip()
    clock.tick(30)

pygame.quit()