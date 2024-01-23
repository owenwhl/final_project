import pygame

pygame.init()
screen = pygame.display.set_mode((750, 750))
clock = pygame.time.Clock()
running = True
dt = 0

def blit_rotate_center(surface, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center= image.get_rect(center= top_left).center)
    return rotated_image, new_rect.topleft

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,rot_vel,group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/ship_up0.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect(center = (x,y))
        self.position = pygame.Vector2((375,375))
        self.angle = 0
        self.rotation_velocity = rot_vel

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.position.y -= 1
        if keys[pygame.K_s]:
            self.position.y += 1
        if keys[pygame.K_a]:
            self.position.x -= 1
        if keys[pygame.K_d]:
            self.position.x += 1
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_velocity
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_velocity

    def update(self):
        self.move()
        self.rect.center += self.position
        blit_rotate_center(screen, self.image, self.position, self.angle)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surf.get_size()[0] // 2
        self.half_h = self.display_surf.get_size()[1] // 2

        # ground
        self.ground_surf = pygame.image.load('graphics/space.jpg').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(center=(375,375))

    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self,player):
        self.center_target_camera(player)

        ground_rect_offset = self.ground_rect.topleft - self.offset
        self.display_surf.blit(self.ground_surf,ground_rect_offset)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surf.blit(sprite.image,offset_pos)

camera_group = CameraGroup()
player = Player(375,375,5,camera_group)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('white')
    camera_group.custom_draw(player)
    player.update()


    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
