import pygame
import time
import math
import random

def restart_game(sprite_groups):
    for group in sprite_groups:
        group.empty()
    player_level.xp_cap = 100
    ship.reset()
    upgrades.reset()
    game_timer = pygame.time.Clock()
    alive = True
    return alive

def blit_rotate_center(surface, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center= image.get_rect(center= top_left).center)
    return rotated_image, new_rect.topleft

def create_asteroid():
    direction_horizontal = ['none','left','right']
    direction_vertical = ['none','up','down']
    direction = pygame.math.Vector2((0,0))
    multiplier = 2
    types = ['asteroid_1','asteroid_2','asteroid_3','asteroid_4','asteroid_5']

    rand_img = random.choice(types)
    if rand_img == 'asteroid_2':
        scale = 0.25 * (random.random() + 1)
    if rand_img == 'asteroid_1':
        scale = 0.18 * (random.random() + 1)
    if rand_img == 'asteroid_3':
        scale = 0.08 * (random.random() + 1)
    if rand_img == 'asteroid_4':
        scale = 0.22 * (random.random() + 1)
    if rand_img == 'asteroid_5':
        scale = 0.1 * (random.random() + 1)

    horizontal_change = random.choice(direction_horizontal)

    if horizontal_change == 'left':
        direction.x += multiplier
        x_pos = ship.position.x - 1000
    if horizontal_change == 'right':
        direction.x -= multiplier
        x_pos = ship.position.x + 1000
    if horizontal_change == 'none':
        direction.x = 0
        tmp_list = [ship.position.x + 1000,ship.position.x - 1000]
        x_pos = random.choice(tmp_list)
        direction_vertical.remove('none')

    vertical_change = random.choice(direction_vertical)

    if vertical_change == 'up':
        direction.y -= multiplier
        y_pos = ship.position.y + 750
    if vertical_change == 'down':
        direction.y += multiplier
        y_pos = ship.position.y - 750
    if vertical_change == 'none':
        direction.y = 0
        tmp_list = [ship.position.y + 750,ship.position.y - 750]
        y_pos = random.choice(tmp_list)

    return Asteroid(direction,x_pos,y_pos,rand_img,scale)

def create_monster(minutes,seconds):
    total_seconds = seconds + (minutes * 60)
    multiplier = 0
    if total_seconds >= 60:
        multiplier = total_seconds * 0.05
    types = ['goop','eye','brain']
    chosen_type = random.choice(types)
    skins = ['1','2','3']
    chosen_skin = random.choice(skins)
    if chosen_type == 'goop':
        speed = 1
        health = 5 + multiplier
        armor = 1
        scale = 2
    if chosen_type == 'eye':
        speed = 1
        health = 5 + multiplier
        armor = 1
        scale = 2
    if chosen_type == 'brain':
        speed = 1
        health = 5 + multiplier
        armor = 1
        scale = 2

    y_pos = 0
    x_pos = 0
    position = ['east','west','north','south']

    chosen_position = random.choice(position)

    if chosen_position == 'east':
        x_pos += ship.position.x + (random.randrange(1000,1150))
        y_pos += ship.position.y + (random.randrange(-550,550))

    if chosen_position == 'west':
        x_pos += ship.position.x - (random.randrange(1000,1150))
        y_pos += ship.position.y + (random.randrange(-550,550))
    
    if chosen_position == 'north':
        y_pos += ship.position.y - (random.randrange(550,700))
        x_pos += ship.position.x + (random.randrange(-1000,1000))

    if chosen_position == 'south':
        y_pos += ship.position.y + (random.randrange(550,700))
        x_pos += ship.position.x + (random.randrange(-1000,1000))

    return Monster(chosen_type,chosen_skin,scale,speed,health,armor,x_pos,y_pos)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,direction,x_pos,y_pos,rand_img,scale):
        super().__init__()
        # print(f"asteroid created with direction {direction} at {x_pos,y_pos}")
        self.image = pygame.image.load(f'graphics/{rand_img}.png')
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.direction = pygame.math.Vector2((0,0))
        self.direction += direction

    def move(self):
        self.rect.center += self.direction

    def check_collision(self):
        if self.rect.colliderect(ship.rect):
            ship.remaining_health -= 50
            ship.damage_cooldown = 10
            self.kill()

        for sprite in sorted(asteroid_group.sprites(),key = lambda sprite: sprite.rect.centery):
            if abs(self.rect.x) + abs(ship.position.x) > 5000 or abs(self.rect.y) + abs(ship.position.y) > 5000:
                self.kill()

class Ground(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.ground_surf = pygame.image.load('graphics/space_1.png').convert_alpha()
        self.ground_surf = pygame.transform.scale_by(self.ground_surf, 3)
        self.ground_rect = self.ground_surf.get_rect(center = (x,y))

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
    
    def center_target_camera(self,target):
        self.offset.x = target.position.x - self.half_w
        self.offset.y = target.position.y - self.half_h

    def custom_draw(self,player,alive,game_active):
        # player
        self.center_target_camera(player)

        # ground
        for sprite in sorted(ground_group.sprites(),key = lambda sprite: sprite.ground_rect.centery):
            ground_offset = sprite.ground_rect.topleft - self.offset * 2
            self.display_surface.blit(sprite.ground_surf,ground_offset)

        # active elements

        # projectiles
        for sprite in sorted(projectile_group.sprites(),key = lambda sprite: sprite.rect.centery):
            if alive and game_active:
                sprite.move_bullet()
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)
                sprite.check_collision()

        # asteroids
        for sprite in sorted(asteroid_group.sprites(),key = lambda sprite: sprite.rect.centery):
            sprite.move()
            offset_pos = sprite.rect.topleft - self.offset
            sprite.check_collision()
            self.display_surface.blit(sprite.image,offset_pos)

        # monsters
        for sprite in sorted(monster_group.sprites(),key = lambda sprite: sprite.rect.center):
            sprite.move()
            sprite.animate_sprite()
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

        # camera_group (player)
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            if alive:
                sprite.image, sprite.rect.topleft = blit_rotate_center(screen, player.image, player.position, player.angle)
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)
    
        # pickup group
        for sprite in sorted(pickup_group.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

        # explosions
        for sprite in sorted(explosion_group.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image,offset_pos)
            if sprite.animation_index >= 4:
                sprite.kill()
            else:
                sprite.image = sprite.frames[int(sprite.animation_index)]
                sprite.animation_index += 0.2

        # damage
        for sprite in sorted(damage_group.sprites(),key = lambda sprite: sprite.rect.center):
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image,offset_pos)
            sprite.timer += 1
            sprite.rect.y -= 1
            if sprite.timer > 25:
                sprite.kill()

        # level up
        for sprite in sorted(level_up_group.sprites(),key = lambda sprite: sprite.rect.center):
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image,offset_pos)
            sprite.move()       

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,max_vel,rotation_vel):
        super().__init__()
        ship_1 = pygame.image.load('graphics/ship_up1.png').convert_alpha()
        ship_1 = pygame.transform.scale_by(ship_1, 2.25)
        ship_2 = pygame.image.load('graphics/ship_up2.png').convert_alpha()
        ship_2 = pygame.transform.scale_by(ship_2, 2.25)
        ship_still = pygame.image.load('graphics/ship_up0.png').convert_alpha()
        ship_still = pygame.transform.scale_by(ship_still, 2.25)
        ship_damage = pygame.image.load('graphics/ship_damage.png').convert_alpha()
        ship_damage = pygame.transform.scale_by(ship_damage, 2.25)
        self.ship_state = [ship_1, ship_2, ship_still, ship_damage]
        self.ship_index = 0

        # upgradeable attributes
        self.fire_rate = 1000
        self.max_health = 100
        self.remaining_health = 100
        self.speed = 1
        self.health_regen = 1000
        self.damage = 5
        self.proj_speed = 1

        self.xp = 0
        self.lvl = 1

        self.image = self.ship_state[self.ship_index]
        self.rect = self.image.get_rect(center = (0,0))

        self.angle = 0
        self.rotation_vel = rotation_vel
        self.max_vel = max_vel
        
        self.position = pygame.Vector2((x,y))
        self.velocity = 0
        self.acceleration = 0.1

        self.coins = 0

        self.active = False
        self.damage_cooldown = 0
        self.death_timer = 0

    def animate_ship(self,moved=False):
        if self.damage_cooldown == 0:
            if moved:
                self.ship_index += 0.1
                if self.ship_index > 2: self.ship_index = 0
                self.image = self.ship_state[int(self.ship_index)]
            else:
                self.image = self.ship_state[2]
        else:
            self.image = self.ship_state[3]
            self.damage_cooldown -= 1


    def move_player(self):
        if self.active:
            radians = math.radians(self.angle)

            self.vertical = math.cos(radians) * self.velocity
            self.horizontal = math.sin(radians) * self.velocity

            self.position.x -= (self.horizontal * self.velocity) * self.speed
            self.position.y -= (self.vertical * self.velocity) * self.speed

    def increase_speed(self):
        if self.active:
            self.velocity = min(self.velocity + self.acceleration, self.max_vel)
            self.move_player()

    def reduce_speed(self):
        if self.active:
            self.velocity = max(self.velocity - self.acceleration/5, 0)
            self.move_player()

    def rotate(self,left=False,right=False):
        if self.active:
            if left:
                self.angle += self.rotation_vel
            elif right:
                self.angle -= self.rotation_vel

    def create_bullet(self):
        return Projectile(screen.get_width() / 2, screen.get_height() / 2,
        self.angle, self.position)

    def reset(self):
        self.xp = 0
        self.lvl = 0
        self.coins = 0
        self.max_health = 100
        self.position.x = 0
        self.position.y = 0
        self.velocity = 0
        self.angle = 0
        self.damage = 5
        self.fire_rate = 1000
        self.remaining_health = 100
        self.speed = 1
        self.health_regen = 1000
        self.proj_speed = 1
        self.death_timer = 125
        self.damage_cooldown = 0

class Projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,angle,position):
        super().__init__()
        self.image = pygame.image.load('graphics/bullet.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect(center= (position))
        self.position = pygame.math.Vector2()
        self.velocity = 10 + ship.proj_speed
        self.radians = math.radians(angle)

        self.vertical = math.cos(self.radians) * self.velocity
        self.horizontal = math.sin(self.radians) * self.velocity

        self.position.x -= self.horizontal
        self.position.y -= self.vertical

    def move_bullet(self):
        self.rect.midtop += self.position
        x_diff = self.rect.x - ship.position.x
        y_diff = self.rect.y - ship.position.y
        if abs(x_diff) > 1500 or abs(y_diff) > 1500:
            self.kill()

    def check_collision(self):
        for sprite in sorted(monster_group.sprites(),key = lambda sprite: sprite.rect.centery):
            if pygame.Rect.colliderect(sprite.rect,self.rect):
                sprite.image = sprite.frames[2]
                sprite.animation_timer = 10
                sprite.health -= (ship.damage / sprite.armor)
                self.kill()
                if sprite.health <= 0:
                    damage_group.add(Damage(self.rect.centerx,self.rect.centery,sprite.armor))
                    x_pos = sprite.rect.centerx
                    y_pos = sprite.rect.centery
                    explosion_group.add(Explosion(x_pos,y_pos)) 
                    self.kill()
                    sprite.kill()
                    ship.xp += 50
                    return pickup_group.add(PickUp(x_pos,y_pos))
                    # return coin_group.add(Coin(x_pos,y_pos))
                return damage_group.add(Damage(sprite.rect.centerx,sprite.rect.centery,sprite.armor))

class Monster(pygame.sprite.Sprite):
    def __init__(self,monster_type,skin,scale,speed,health,armor,x_pos,y_pos):
        super().__init__()
        frame1 = pygame.image.load(f"graphics/{monster_type}{skin}_0.png").convert_alpha()
        frame1 = pygame.transform.scale_by(frame1, scale)
        frame2 = pygame.image.load(f"graphics/{monster_type}{skin}_1.png").convert_alpha()
        frame2 = pygame.transform.scale_by(frame2, scale)
        damage_frame = pygame.image.load(f'graphics/{monster_type}_damage.png').convert_alpha()
        damage_frame = pygame.transform.scale_by(damage_frame, scale)
        self.frames = [frame1,frame2,damage_frame]
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

        self.speed = speed
        self.health = health
        self.armor = armor

        self.type = monster_type
        self.scale = scale

        self.animation_timer = 0

    def move(self):
        dx = ship.rect.centerx - self.rect.centerx
        dy = ship.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 80:
            dx, dy = dx / distance, dy / distance
            self.rect.centerx += dx * self.speed  
            self.rect.centery += dy * self.speed
        else:
            ship.remaining_health -= 20
            ship.damage_cooldown = 10
            self.kill()
            
    def animate_sprite(self):
        if self.animation_timer == 0:
            self.animation_index += 0.025
            if self.animation_index >= 2:
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
        else:
            self.animation_timer -= 1

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos):
        super().__init__()
        frame1 = pygame.image.load('graphics/explosion_0.png').convert_alpha()
        frame1 = pygame.transform.scale_by(frame1, 3)
        frame2 = pygame.image.load('graphics/explosion_1.png').convert_alpha()
        frame2 = pygame.transform.scale_by(frame2, 3)
        frame3 = pygame.image.load('graphics/explosion_2.png').convert_alpha()
        frame3 = pygame.transform.scale_by(frame3, 3)
        frame4 = pygame.image.load('graphics/explosion_3.png').convert_alpha()
        frame4 = pygame.transform.scale_by(frame4, 3)
        self.frames = [frame1,frame2,frame3,frame4]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

class Level:
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((0,50))
        self.image.fill("light blue") 
        self.rect = self.image.get_rect(midbottom = (650,870))
        self.xp_cap = 100

    def xp_bar_blit(self,xp,level):
        pixel_multiplier = self.xp_cap / 400
        self.image = pygame.Surface((ship.xp / pixel_multiplier,50))
        if ship.xp >= self.xp_cap:
            ship.lvl += 1
            ship.xp -= self.xp_cap
            self.xp_cap *= 1.15
            upgrades.attribute_points += 1
            return level_up_group.add(LevelUp(ship.position.x,ship.position.y))
        self.image.fill("light blue")
        screen.blit(self.image,self.rect)

class LevelUp(pygame.sprite.Sprite):
    def __init__(self,ship_posx,ship_posy):
        super().__init__()
        self.image = small_font.render('Level up!',False,'green')
        self.rect = self.image.get_rect(center = (ship_posx,ship_posy))
        self.timer = 0

    def move(self):
        self.rect.y -= 1
        self.timer += 1
        if self.timer > 100:
            self.kill()

class Upgrades:
    def __init__(self):
        super().__init__()
        self.max_health_lvl = 0        # 1
        self.damage_lvl = 0            # 2
        self.proj_speed_lvl = 0        # 3
        self.fire_rate_lvl = 0         # 4
        self.speed_lvl = 0             # 5
        self.health_regen_lvl = 0      # 6

        self.attribute_points = 150
        
    def lvl_up(self,allow_upgrades):
        keys = pygame.key.get_pressed()
        if self.attribute_points > 0:
            if allow_upgrades:
                if keys[pygame.K_1] and self.max_health_lvl <= 24: # health
                    self.max_health_lvl += 1
                    self.attribute_points -= 1
                    ship.max_health += (upgrades.max_health_lvl * 10)
                    return False
                if keys[pygame.K_2] and self.damage_lvl <= 24: # damage
                    self.damage_lvl += 1
                    self.attribute_points -= 1
                    ship.damage += 7.5
                    # print(ship.damage)
                    return False
                if keys[pygame.K_3] and self.proj_speed_lvl <= 24: # proj speed
                    self.proj_speed_lvl += 1
                    self.attribute_points -= 1
                    ship.proj_speed += 1.75
                    # print(ship.proj_speed)
                    return False
                if keys[pygame.K_4] and self.fire_rate_lvl <= 24: # fire rate
                    self.fire_rate_lvl += 1
                    self.attribute_points -= 1
                    ship.fire_rate -= 39
                    # print(ship.fire_rate)
                    return False
                if keys[pygame.K_5] and self.speed_lvl <= 24: # speed
                    self.speed_lvl += 1
                    self.attribute_points -= 1
                    ship.speed += 0.1
                    # print(ship.speed)
                    return False
                if keys[pygame.K_6] and self.health_regen_lvl <= 24:
                    self.health_regen_lvl += 1
                    self.attribute_points -= 1
                    ship.health_regen -= 30
                    # print(ship.health_regen)
                    return False

    def reset(self):
        self.max_health_lvl = 0     
        self.health_regen_lvl = 0   
        self.damage_lvl = 0           
        self.proj_speed_lvl = 0      
        self.fire_rate_lvl = 0        
        self.speed_lvl = 0
        self.attribute_points = 0

class Damage(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos,armor):
        super().__init__()
        if ship.damage < 10:
            self.image = small_font.render(f'{int(ship.damage / armor * 100) / 100}',False,'white')
        elif ship.damage < 30:
            self.image = small_font.render(f'{int(ship.damage / armor * 100) / 100}',False,'yellow')
        elif ship.damage < 75:
            self.image = small_font.render(f'{int(ship.damage / armor * 100) / 100}',False,'orange')
        else:
            self.image = small_font.render(f'{int(ship.damage / armor * 100) / 100}',False,'red')

        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.timer = 0

class PickUp(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos):
        super().__init__()
        item_pickup = random.randrange(1,10)
        if item_pickup == 0:
            pickup_list = ["freeze","heal","nuke"]
        else:
            pickup_list = ["xp"]
        choose_pickup = random.choice(pickup_list)
        if choose_pickup == "freeze":
            self.image = pygame.image.load('graphics/.png').convert_alpha()
        elif choose_pickup == "heal":
            self.image = pygame.image.load('graphics/.png').convert_alpha()
        elif choose_pickup == "nuke":
            self.image = pygame.image.load('graphics/.png').convert_alpha()
        elif choose_pickup == "xp":
            self.image = pygame.image.load('graphics/xp.png').convert_alpha()
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

pygame.init()
clock = pygame.time.Clock()
game_timer = pygame.time.Clock()
screen = pygame.display.set_mode((1700,900))
running = True
game_active = False
alive = True
dt = 0

title_font = pygame.font.Font('graphics/PixelType.ttf', 150)
gui_font = pygame.font.Font('graphics/PixelType.ttf', 75)
small_font = pygame.font.Font('graphics/PixelType.ttf', 40)

camera_group = CameraGroup()
sprite_groups = []
projectile_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
damage_group = pygame.sprite.Group()
level_up_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
pickup_group = pygame.sprite.Group()
sprite_groups = [projectile_group,asteroid_group,monster_group,damage_group,level_up_group,explosion_group,pickup_group]
player_level = Level()

ground5 = Ground(-850,-450)
ground4 = Ground(-9850,-450)
ground1 = Ground(-9850,-9450)
ground7 = Ground(-9850,8550)
ground2 = Ground(-850,-9450)
ground8 = Ground(-850,8550)
ground6 = Ground(8150,-450)
ground9 = Ground(8150,8550)
ground3 = Ground(8150,-9450)
ground_list = [ground1,ground2,ground3,ground4,ground5,ground6,ground7,ground8,ground9]
for ground in ground_list:
    ground_group.add(ground)

ship = Player(0,0,1.5,4)
camera_group.add(ship)

upgrades = Upgrades()

fire_bullet = pygame.USEREVENT + 1
pygame.time.set_timer(fire_bullet, ship.fire_rate)

spawn_asteroid = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_asteroid, 1000)

monster_timer = 500
spawn_monster = pygame.USEREVENT + 3
pygame.time.set_timer(spawn_monster, monster_timer)

upgrade_timer = pygame.USEREVENT + 5
pygame.time.set_timer(upgrade_timer, 100)

regen_health = pygame.USEREVENT + 6
pygame.time.set_timer(regen_health,ship.health_regen)

allow_upgrades = True

minutes = 0
seconds = 0
blit_health = False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not game_active:
            break
        if event.type == fire_bullet:
            pygame.time.set_timer(fire_bullet, ship.fire_rate)
            projectile_group.add(ship.create_bullet())
        if event.type == spawn_asteroid:
            asteroid_group.add(create_asteroid())
        if event.type == spawn_monster:
            monster_group.add(create_monster(minutes,seconds // 1000))
            pygame.time.set_timer(spawn_monster, monster_timer)
        if event.type == upgrade_timer:
            allow_upgrades = True
        if event.type == regen_health:
            pygame.time.set_timer(regen_health,ship.health_regen)
            if ship.remaining_health < ship.max_health:
                ship.remaining_health += (ship.max_health / 100) * (upgrades.health_regen_lvl / 5)
                if ship.remaining_health > ship.max_health:
                    temp = ship.remaining_health - ship.max_health
                    ship.remaining_health -= temp
        
    if not game_active:
        screen.blit(ground.ground_surf,ground.ground_rect)
        
        ship.animate_ship(True)
        camera_group.custom_draw(ship,alive,game_active)

        title = title_font.render('SPACE SHOOTER',False,'white')
        title_rect = title.get_rect(center = (850,250))
        screen.blit(title,title_rect)

        start = gui_font.render('Press space to start!',False,'white')
        start_rect = start.get_rect(center = (850,650))
        screen.blit(start,start_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            game_timer = pygame.time.Clock()
            ship.active = True
            game_active = True

    else:
        if alive:
            screen.fill('white')

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

            camera_group.custom_draw(ship,alive,game_active)

            coordinates = gui_font.render(f'{math.floor(ship.position.x)} {math.floor(ship.position.y)}',False,'red')
            coordinates_rect = coordinates.get_rect(topleft= (10,10))
            screen.blit(coordinates,coordinates_rect)

            coins = gui_font.render(f'coins: {ship.coins}',False,'white')
            coins_rect = coins.get_rect(bottomright= (1700,830))
            screen.blit(coins,coins_rect)

            lvl = gui_font.render(f'lvl {ship.lvl}',False,'white')
            lvl_rect = lvl.get_rect(midbottom = (575,875))
            screen.blit(lvl,lvl_rect)
            
            seconds += game_timer.tick(60)

            if seconds // 1000 >= 60:
                seconds = 0
                minutes += 1
            if minutes < 1:
                if seconds // 1000 < 10:
                    game_time = gui_font.render(f'00: 0{seconds // 1000}',False,'white')
                else:
                    game_time = gui_font.render(f'00: {seconds // 1000}',False,'white')
            elif minutes >= 1 and minutes < 10:
                if seconds // 1000 < 10:
                    game_time = gui_font.render(f'0{minutes}: 0{seconds // 1000}',False,'white')
                else:
                    game_time = gui_font.render(f'0{minutes}: {seconds // 1000}',False,'white')
            elif minutes >= 10:
                if seconds // 1000 < 10:
                    game_time = gui_font.render(f'{minutes}: 0{seconds // 1000}',False,'white')
                else:
                    game_time = gui_font.render(f'{minutes}: {seconds // 1000}',False,'white')

            game_time_rect = game_time.get_rect(center = (850,160))
            screen.blit(game_time,game_time_rect)

            player_level.xp_bar_blit(ship.xp,ship.lvl)

            lvl_up_tokens = gui_font.render(f'tokens: {upgrades.attribute_points}',False,'white')
            lvl_up_tokens_rect = lvl_up_tokens.get_rect(midleft= (10,450))
            screen.blit(lvl_up_tokens,lvl_up_tokens_rect)

            allow_upgrades = upgrades.lvl_up(allow_upgrades)

            attribute_list = [upgrades.max_health_lvl,upgrades.damage_lvl,upgrades.proj_speed_lvl,upgrades.fire_rate_lvl,upgrades.speed_lvl,upgrades.health_regen_lvl]
            counter = 0

            for attribute_lvl in attribute_list:
                display_level = gui_font.render(f'{attribute_lvl}',False,'white')
                display_level_rect = display_level.get_rect(bottomleft = (50 + counter,850))
                screen.blit(display_level,display_level_rect)
                counter += 75

            if ship.remaining_health == ship.max_health:
                blit_health = False
            else:
                blit_health = True

            max_health = pygame.Surface((75 * blit_health,9))
            max_health.fill('red')
            max_health_rect = max_health.get_rect(center = (850,390))
            screen.blit(max_health,max_health_rect)

            if ship.remaining_health > 0:
                pixel_per_percent = 75 / (ship.max_health / ship.remaining_health)
                remaining_health = pygame.Surface((pixel_per_percent * blit_health,9))
                remaining_health.fill('green')
                remaining_health_rect = max_health.get_rect(center = (850,390))
                screen.blit(remaining_health,remaining_health_rect)

            else:
                player_explosion = Explosion(ship.position.x,ship.position.y)
                explosion_group.add(player_explosion)
                ship.death_timer = 125
                alive = False
                
        else:
            screen.fill('white')
            camera_group.custom_draw(ship,alive,game_active)

            if ship.death_timer != 1:
                ship.death_timer -= 1
            if ship.death_timer == 1:
                game_over = gui_font.render('Game over!',False,'white')
                game_over_rect = game_over.get_rect(center = (850,400))
                screen.blit(game_over,game_over_rect)
                spacebar = gui_font.render('Press space to restart',False,'white')
                spacebar_rect = spacebar.get_rect(center = (850,450))
                screen.blit(spacebar,spacebar_rect)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    alive = restart_game(sprite_groups)
                    seconds = 0
                    minutes = 0
                    game_timer = pygame.time.Clock()

    pygame.display.update()
    dt = clock.tick(60) / 1000

pygame.quit()