import pygame
import time
import math
import random

def game_over(seconds,minutes): 
    # function that compacts all end screen msgs into a dictionary and blits them 
    gui = {}

    game_over = gui_font.render('Game over!',False,'white')
    game_over_rect = game_over.get_rect(center = (850,200))

    monsters_killed = gui_font.render(f'Monsters killed: {ship.monster_count}',False,'white')
    monsters_killed_rect = monsters_killed.get_rect(center = (850,300))

    time_elapsed = gui_font.render(f'Time elapsed: {print_time(seconds,minutes)}',False,'white')
    time_elapsed_rect = time_elapsed.get_rect(center = (850,350))

    ship_level = gui_font.render(f'Ship level reached: {ship.lvl}',False,'white')
    ship_level_rect = ship_level.get_rect(center = (850,400))

    asteroids_destroyed = gui_font.render(f'Asteroids demolished: {ship.asteroid_count}',False,'white')
    asteroids_destroyed_rect = asteroids_destroyed.get_rect(center = (850,450))

    xp_orbs_collected = gui_font.render(f'Xp orbs collected: {ship.xp_count}',False,'white')
    xp_orbs_collected_rect = xp_orbs_collected.get_rect(center = (850, 500))

    powerups_collected = gui_font.render(f'Powerups collected: {ship.powerup_count}',False,'white')
    powerups_collected_rect = powerups_collected.get_rect(center = (850,550))

    spacebar = gui_font.render('Press space to restart',False,'white')
    spacebar_rect = spacebar.get_rect(center = (850,700))
    
    gui[game_over] = game_over_rect
    gui[monsters_killed] = monsters_killed_rect
    gui[time_elapsed] = time_elapsed_rect
    gui[ship_level] = ship_level_rect
    gui[spacebar] = spacebar_rect
    gui[asteroids_destroyed] = asteroids_destroyed_rect
    gui[xp_orbs_collected] = xp_orbs_collected_rect
    gui[powerups_collected] = powerups_collected_rect

    for surf, rect in gui.items():
        screen.blit(surf,rect)

def print_time(seconds,minutes):
    # prints time elapsed to display correctly on the screen
    if minutes < 1:
        if seconds // 1000 < 10:
            game_time = f'00: 0{seconds // 1000}'
        else:
            game_time = f'00: {seconds // 1000}'
    elif minutes >= 1 and minutes < 10:
        if seconds // 1000 < 10:
            game_time = f'0{minutes}: 0{seconds // 1000}'
        else:
            game_time = f'0{minutes}: {seconds // 1000}'
    elif minutes >= 10:
        if seconds // 1000 < 10:
            game_time = f'{minutes}: 0{seconds // 1000}'
        else:
            game_time = f'{minutes}: {seconds // 1000}'
    return game_time

def restart_game(sprite_groups):
    # restarts game by emptying sprite groups, resetting game_timer/upgrades/ship attributes etc.
    for group in sprite_groups:
        group.empty()
    player_level.xp_cap = 100
    ship.reset()
    upgrades.reset()
    game_timer = pygame.time.Clock()
    alive = True
    return alive

def blit_rotate_center(surface, image, top_left, angle):
    # changes the player's sprite based on its angle
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center= image.get_rect(center= top_left).center)
    return rotated_image, new_rect.topleft

def create_asteroid():
    # creates a randomized asteroid object (direction,type,scale)
    direction_horizontal = ['none','left','right']
    direction_vertical = ['none','up','down']
    direction = pygame.math.Vector2((0,0))
    multiplier = 2 # changes the speed of the asteroids
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
    # creates a randomized enemy (direction,skin,starting_pos)
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

class Asteroid(pygame.sprite.Sprite): # Asteroid class called when initializing an asteroid
    def __init__(self,direction,x_pos,y_pos,rand_img,scale):
        super().__init__()
        frame1 = pygame.image.load(f'graphics/{rand_img}.png')
        frame1 = pygame.transform.scale_by(frame1, scale)
        damage_frame = pygame.image.load(f'graphics/{rand_img}_damage.png')
        damage_frame = pygame.transform.scale_by(damage_frame, scale)
        frozen_frame = pygame.image.load(f'graphics/{rand_img}_frozen.png')
        frozen_frame = pygame.transform.scale_by(frozen_frame, scale)

        self.scale = 1 + (scale * 5)
        self.frames = [frame1,damage_frame,frozen_frame]
        self.image = frame1
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.direction = pygame.math.Vector2((0,0))
        self.direction += direction
        self.health = 100

        self.animation_timer = 0
        self.death_sound = pygame.mixer.Sound('audio/asteroid_explosion.wav')

    def move(self): # moves the asteroid
        self.rect.center += self.direction

    def check_collision(self):
        # checks whether the asteroid has collided with the player's sprite
        if self.rect.colliderect(ship.rect):
            ship.remaining_health -= 50
            ship.damage_cooldown = 10
            self.kill()

        # deletes the asteroid if it goes out of a certain range from the player to reduce lag
        for sprite in sorted(asteroid_group.sprites(),key = lambda sprite: sprite.rect.centery):
            if abs(self.rect.x) + abs(ship.position.x) > 5000 or abs(self.rect.y) + abs(ship.position.y) > 5000:
                self.kill()

class Ground(pygame.sprite.Sprite): # Ground class creates the space background
    def __init__(self,x,y):
        super().__init__()
        self.ground_surf = pygame.image.load('graphics/space_1.png').convert_alpha()
        self.ground_surf = pygame.transform.scale_by(self.ground_surf, 3)
        self.ground_rect = self.ground_surf.get_rect(center = (x,y))

class CameraGroup(pygame.sprite.Group): # Used to display sprites on the screen relative to the player's location
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
    
    def center_target_camera(self,target): # centers the camera so the player is always at the center
        self.offset.x = target.position.x - self.half_w
        self.offset.y = target.position.y - self.half_h

    def custom_draw(self,player,alive,game_active): 
        # alive is a boolean value that is used to qualify certain actions from happening
        # ex: if alive is False, the ship is not blit'd onto the screen because the ship has lost
        # all of its remaining health

        # game_active is a boolean value used on the title screen to prevent the ship from shooting bullets

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
            if sprite.animation_timer > 0:
                sprite.animation_timer -= 1
                sprite.image = sprite.frames[1]
            else:
                sprite.image = sprite.frames[0]
            if ship.freeze_timer == 0:
                sprite.move()
            else:
                sprite.image = sprite.frames[2]
            offset_pos = sprite.rect.topleft - self.offset
            sprite.check_collision()
            self.display_surface.blit(sprite.image,offset_pos)

        # monsters
        for sprite in sorted(monster_group.sprites(),key = lambda sprite: sprite.rect.center):
            sprite.animate_sprite()
            if ship.freeze_timer == 0:
                sprite.move()
            else:
                sprite.image = sprite.frames[3]
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

        # camera_group (player)
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            if alive:
                sprite.image, sprite.rect.topleft = blit_rotate_center(screen, player.image, player.position, player.angle)
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image,offset_pos)

        # pickups
        for sprite in sorted(pickup_group.sprites(),key = lambda sprite: sprite.rect.centery):
            sprite.pickup_timer -= 1
            if ship.magnet_timer > 0:
                dx, dy = sprite.move(sprite.rect.centerx,sprite.rect.centery)
                sprite.rect.centerx += dx * 10
                sprite.rect.centery += dy * 10
            if sprite.pickup_timer < 100:
                sprite.kill()
            if sprite.pickup_timer < 500:
                multiplier = (500 - sprite.pickup_timer) / 100
                if sprite.animation_index < 2:
                    sprite.animation_index += 0.1 * multiplier
                if sprite.animation_index >= 2:
                    sprite.animation_index = 0
            sprite.image = sprite.frames[int(sprite.animation_index)]
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            if pygame.Rect.colliderect(ship.rect,sprite.rect):
                sprite.pickup()

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

class Player(pygame.sprite.Sprite): # Main class for player stats and movement
    def __init__(self,x,y,max_vel,rotation_vel):
        super().__init__()
        # loads each ship sprite and puts them in a list (ship_state)
        # alternates ship_index in order to change between the states
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

        self.image = self.ship_state[self.ship_index] 
        self.rect = self.image.get_rect(center = (0,0))

        # movement attributes (vel stands for velocity)
        self.angle = 0 
        self.rotation_vel = rotation_vel
        self.max_vel = max_vel
        self.position = pygame.Vector2((x,y))
        self.velocity = 0
        self.acceleration = 0.1

        # upgradeable attributes
        self.fire_rate = 1000
        self.max_health = 100
        self.remaining_health = 100
        self.speed = 1
        self.health_regen = 1000
        self.damage = 5
        self.proj_speed = 1

        # Leveling
        self.xp = 0
        self.lvl = 1

        self.active = False # prevents the player from moving when not True (increase/reduce speed,move,rotate)
        self.damage_cooldown = 0 # used to prevent sprite from changing when in a damaged state
        self.death_timer = 0 # used when the player dies so there is a delay when displaying game over

        # counts stats to display at the end of the game
        self.monster_count = 0
        self.asteroid_count = 0
        self.xp_count = 0
        self.powerup_count = 0

        # timers that are used for powerups
        self.magnet_timer = 0
        self.nuke_timer = 0
        self.freeze_timer = 0

        # initializing sound that plays when the player dies
        self.death_sound = pygame.mixer.Sound('audio/player_death.wav')
        self.death_sound.set_volume(0.25)

    def animate_ship(self,moved=False): # function for changing the ship's sprite to simulate animation
        if self.damage_cooldown == 0:
            if moved:
                self.ship_index += 0.1
                if self.ship_index > 2: self.ship_index = 0
                self.image = self.ship_state[int(self.ship_index)]
            else:
                self.image = self.ship_state[2]
        else:
            self.image = self.ship_state[3] # ship_state[3] is the damage state (filled in with red)
            self.damage_cooldown -= 1

    def move_player(self): # moves the player based on its angle
        if self.active:
            radians = math.radians(self.angle) # changes angle to radians

            # calculates displacement
            self.vertical = math.cos(radians) * self.velocity
            self.horizontal = math.sin(radians) * self.velocity

            # adds this value to the position vector of the ship
            self.position.x -= (self.horizontal * self.velocity) * self.speed 
            self.position.y -= (self.vertical * self.velocity) * self.speed

    def increase_speed(self): # simulates acceleration
        if self.active:
            self.velocity = min(self.velocity + self.acceleration, self.max_vel)
            self.move_player()

    def reduce_speed(self): # simulates deacceleration
        if self.active:
            self.velocity = max(self.velocity - self.acceleration/5, 0)
            self.move_player()

    def rotate(self,left=False,right=False): # changes the ship's angle based on player's input
        if self.active:
            if left:
                self.angle += self.rotation_vel
            elif right:
                self.angle -= self.rotation_vel

    def create_bullet(self): # initializes a bullet object from the projectile class
        return Projectile(screen.get_width() / 2, screen.get_height() / 2,
        self.angle, self.position)

    def reset(self): # function that is ran when the player presses space to reset the game
        # returns all ship values to their default values
        self.xp = 0
        self.lvl = 0
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

class Projectile(pygame.sprite.Sprite): # class used for initializing the player's projectiles
    def __init__(self,x,y,angle,position): # uses player's position and angle to determine where the projectile fires initially
        super().__init__()
        self.image = pygame.image.load('graphics/bullet.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect(center= (position))
        self.position = pygame.math.Vector2()
        self.velocity = 10 + ship.proj_speed # proj_speed attribute adds to the bullet's velocity
        self.radians = math.radians(angle)

        # same logic as move_player
        self.vertical = math.cos(self.radians) * self.velocity
        self.horizontal = math.sin(self.radians) * self.velocity

        self.position.x -= self.horizontal
        self.position.y -= self.vertical

    def move_bullet(self): # function is ran every frame and uses the fixed values from the player's position vector from when it was fired
        self.rect.midtop += self.position # updates the bullet location based on its position vector
        x_diff = self.rect.x - ship.position.x
        y_diff = self.rect.y - ship.position.y
        if abs(x_diff) > 850 or abs(y_diff) > 450: # destroys bullet if it goes off the screen
            self.kill()

    def check_collision(self): # checks collisions between projectiles and enemies/asteroids
        for sprite in sorted(monster_group.sprites(),key = lambda sprite: sprite.rect.centery): # enemies
            if pygame.Rect.colliderect(sprite.rect,self.rect):
                sprite.image = sprite.frames[2] # damage frame
                sprite.animation_timer = 10 # used to time how many frames the sprite is filled in with red
                sprite.health -= (ship.damage / sprite.armor)
                self.kill() # kills projectile regardless of whether it kills the enemy or not
                if sprite.health <= 0: #
                    sprite.death_sound.play()
                    self.kill() # deletes projectile sprite
                    sprite.kill() # deletes monster sprite
                    damage_group.add(Damage(self.rect.centerx,self.rect.centery,sprite.armor)) # displays damage num above head
                    explosion_group.add(Explosion(sprite.rect.centerx,sprite.rect.centery,1)) # creates an explosion sprite
                    ship.monster_count += 1 # counts num of monsters the player has killed
                    return pickup_group.add(PickUp(sprite.rect.centerx,sprite.rect.centery)) # creates a powerup from the PickUp class
                return damage_group.add(Damage(sprite.rect.centerx,sprite.rect.centery,sprite.armor)) # displays damage num above head
        for sprite in sorted(asteroid_group.sprites(),key = lambda sprite: sprite.rect.centery): # asteroids
            if pygame.Rect.colliderect(sprite.rect,self.rect):
                sprite.animation_timer = 5 # used to simulate damage frames
                sprite.health -= ship.damage
                self.kill() # kills projectile regardless of whether it destroys the asteroid or not
                if sprite.health <= 0: # asteroids give the player a random attribute when destroyed
                    roll = [1,2,3,4,5,6]
                    if upgrades.max_health_lvl >= 25:
                        roll.remove(1)
                    if upgrades.damage_lvl >= 25:
                        roll.remove(2)
                    if upgrades.proj_speed_lvl >= 25:
                        roll.remove(3)
                    if upgrades.fire_rate_lvl >= 25:
                        roll.remove(4)
                    if upgrades.speed_lvl >= 25:
                        roll.remove(5)
                    if upgrades.health_regen_lvl >= 25:
                        roll.remove(6)
                    if roll:
                        pick = random.choice(roll)
                        upgrades.lvl_up(True, pick) # calls the lvl_up function and uses pick to overwrite bypass as a truthy value
                        level_up_group.add(LevelUp(ship.position.x,ship.position.y,pick)) # adds a +1 above the player's head
                        # to visually show when a player's attribute has increased
                    sprite.kill()
                    ship.asteroid_count += 1 # counts num of asteroids the player has destroyed
                    sprite.death_sound.play()
                    explosion_group.add(Explosion(sprite.rect.centerx,sprite.rect.centery,sprite.scale)) # creates explosion sprite

class Monster(pygame.sprite.Sprite): # Monster class that initializes objects using the arguments from the create_monster func
    def __init__(self,monster_type,skin,scale,speed,health,armor,x_pos,y_pos):
        super().__init__()
        frame1 = pygame.image.load(f"graphics/{monster_type}{skin}_0.png").convert_alpha()
        frame1 = pygame.transform.scale_by(frame1, scale)
        frame2 = pygame.image.load(f"graphics/{monster_type}{skin}_1.png").convert_alpha()
        frame2 = pygame.transform.scale_by(frame2, scale)
        damage_frame = pygame.image.load(f'graphics/{monster_type}_damage.png').convert_alpha()
        damage_frame = pygame.transform.scale_by(damage_frame, scale)
        frozen_frame = pygame.image.load(f'graphics/{monster_type}_frozen.png').convert_alpha()
        frozen_frame = pygame.transform.scale_by(frozen_frame, scale)
        self.frames = [frame1,frame2,damage_frame,frozen_frame] 
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

        # initializes the enemy's attributes
        self.speed = speed
        self.health = health
        self.armor = armor
        self.type = monster_type
        self.scale = scale

        self.animation_timer = 0
        self.death_sound = pygame.mixer.Sound('audio/explosion.wav')

    def move(self): # moves the enemy based on its distance from the player
        dx = ship.rect.centerx - self.rect.centerx
        dy = ship.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy) # creates a triangle using horizontal/vertical direction vectors (dx/dy)
        if distance > 80: # while the enemy has not reached the player
            dx, dy = dx / distance, dy / distance
            self.rect.centerx += dx * self.speed  
            self.rect.centery += dy * self.speed
        else: # if the enemy reaches the player
            ship.remaining_health -= 20
            ship.damage_cooldown = 10
            self.kill()
            
    def animate_sprite(self): # animates the monster sprite
        if self.animation_timer == 0:
            self.animation_index += 0.025
            if self.animation_index >= 2: # this is done so the code only alternates between the first two frames in self.frames
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]
        else:
            self.animation_timer -= 1

class Explosion(pygame.sprite.Sprite): # class used when initializing explosion objects when monsters/asteroids/player dies
    def __init__(self,x_pos,y_pos,scale):
        super().__init__()
        frame1 = pygame.image.load('graphics/explosion_0.png').convert_alpha()
        frame1 = pygame.transform.scale_by(frame1, 2 + scale)
        frame2 = pygame.image.load('graphics/explosion_1.png').convert_alpha()
        frame2 = pygame.transform.scale_by(frame2, 2 + scale)
        frame3 = pygame.image.load('graphics/explosion_2.png').convert_alpha()
        frame3 = pygame.transform.scale_by(frame3, 2 + scale)
        frame4 = pygame.image.load('graphics/explosion_3.png').convert_alpha()
        frame4 = pygame.transform.scale_by(frame4, 2 + scale)
        self.frames = [frame1,frame2,frame3,frame4]
        self.animation_index = 0
        self.image = self.frames[self.animation_index] # same logic as other classes, more frames are used to simulate explosion
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

class Level: # class used for blitting the xp bar on the bottom of the screen
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((0,50))
        self.image.fill("light blue") 
        self.rect = self.image.get_rect(midbottom = (650,870))
        self.xp_cap = 100
        self.level_up_sound = pygame.mixer.Sound('audio/level_up.wav')

    def xp_bar_blit(self,xp,level): 
        # creates a rectangle based on the percentage of xp the player has gained in terms of the max xp required to level up
        pixel_multiplier = self.xp_cap / 400
        self.image = pygame.Surface((ship.xp / pixel_multiplier,50))
        if ship.xp >= self.xp_cap:
            self.level_up_sound.play()
            ship.lvl += 1
            ship.xp -= self.xp_cap
            self.xp_cap *= 1.15
            upgrades.attribute_points += 1 # allows the player to select an attribute upon leveling up
            return level_up_group.add(LevelUp(ship.position.x,ship.position.y,0))
        self.image.fill("light blue")
        screen.blit(self.image,self.rect)

class LevelUp(pygame.sprite.Sprite): # LevelUp class is used for displaying a message when the player levels up or gains an attribute
    def __init__(self,ship_posx,ship_posy,attribute):
        super().__init__()
        self.attributes = {}
        self.attributes[1] = '#FD7F84'
        self.attributes[2] = '#FDDD7F'
        self.attributes[3] = '#FDF97F'
        self.attributes[4] = '#7FFD89'
        self.attributes[5] = '#7F88FD'
        self.attributes[6] = '#BE7FFD'

        if not attribute:
            self.image = small_font.render('Level up!',False,'green')
        else:
            self.image = small_font.render('+1',False,self.attributes[attribute])
        self.rect = self.image.get_rect(center = (ship_posx,ship_posy))
        self.timer = 0

    def move(self): # moves the text at a constant rate for an amount of time using self.timer
        self.rect.y -= 1
        self.timer += 1
        if self.timer > 100:
            self.kill()

class Upgrades: # this class is used for managing the player's attributes
    def __init__(self):
        super().__init__()
        self.max_health_lvl = 0        # 1
        self.damage_lvl = 0            # 2
        self.proj_speed_lvl = 0        # 3
        self.fire_rate_lvl = 0         # 4
        self.speed_lvl = 0             # 5
        self.health_regen_lvl = 0      # 6

        self.attribute_points = 150 # num of points available to the player to spend on points

    def lvl_up(self,allow_upgrades,bypass): 
        # bypass is used when the player gains an attribute from destroying an asteroid
        keys = pygame.key.get_pressed()
        if self.attribute_points > 0 or bypass:
            if allow_upgrades or bypass:
                if self.max_health_lvl <= 24 and (keys[pygame.K_1] or bypass == 1): # health
                    self.max_health_lvl += 1
                    if bypass != 1:
                        self.attribute_points -= 1
                    ship.max_health += (upgrades.max_health_lvl * 10)
                    level_up_group.add(LevelUp(ship.position.x,ship.position.y,1))

                if self.damage_lvl <= 24 and (keys[pygame.K_2] or bypass == 2): # damage
                    self.damage_lvl += 1
                    if bypass != 2:
                        self.attribute_points -= 1
                    ship.damage += 7.5
                    level_up_group.add(LevelUp(ship.position.x,ship.position.y,2))

                if self.proj_speed_lvl <= 24 and (keys[pygame.K_3] or bypass == 3): # proj speed
                    self.proj_speed_lvl += 1
                    if bypass != 3:
                        self.attribute_points -= 1
                    ship.proj_speed += 1.75
                    level_up_group.add(LevelUp(ship.position.x,ship.position.y,3))

                if self.fire_rate_lvl <= 24 and (keys[pygame.K_4] or bypass == 4): # fire rate
                    self.fire_rate_lvl += 1
                    if bypass != 4:
                        self.attribute_points -= 1
                    ship.fire_rate -= 39
                    level_up_group.add(LevelUp(ship.position.x,ship.position.y,4))

                if self.speed_lvl <= 24 and (keys[pygame.K_5] or bypass == 5): # speed
                    self.speed_lvl += 1
                    if bypass != 5:
                        self.attribute_points -= 1
                    ship.speed += 0.1
                    level_up_group.add(LevelUp(ship.position.x,ship.position.y,5))

                if self.health_regen_lvl <= 24 and (keys[pygame.K_6] or bypass == 6): # health regen
                    self.health_regen_lvl += 1
                    if bypass != 6:
                        self.attribute_points -= 1
                    ship.health_regen -= 30
                    level_up_group.add(LevelUp(ship.position.x,ship.position.y,6))

                # sets allow_upgrades to false in order to have a cooldown on the amount of attributes the player can apply in a single frame
                return False 

    def print_gui(self): # prints the gui in the bottom left corner of the screen
        attribute_gui = pygame.image.load('graphics/attribute_gui.png')
        attribute_gui = pygame.transform.scale_by(attribute_gui, 3)
        attribute_gui_rect = attribute_gui.get_rect(bottomleft = (10,875))
        screen.blit(attribute_gui,attribute_gui_rect)
        self.max_health_font = attribute_font.render(f"Max Health Lvl: {self.max_health_lvl}",False,"black")
        self.max_health_font_rect = self.max_health_font.get_rect(midleft = (20, 680))
        self.damage_font = attribute_font.render(f"Damage Lvl: {self.damage_lvl}",False,"black")
        self.damage_font_rect = self.damage_font.get_rect(midleft = (20, 717))
        self.proj_speed_font = attribute_font.render(f"Proj Speed Lvl: {self.proj_speed_lvl}",False,"black")
        self.proj_speed_font_rect = self.proj_speed_font.get_rect(midleft = (20, 753))
        self.fire_rate_font = attribute_font.render(f"Fire Rate Lvl: {self.fire_rate_lvl}",False,"black")
        self.fire_rate_font_rect = self.fire_rate_font.get_rect(midleft = (20, 789))
        self.speed_font = attribute_font.render(f"Speed Lvl: {self.speed_lvl}",False,"black")
        self.speed_font_rect = self.speed_font.get_rect(midleft = (20, 825))
        self.health_regen_font = attribute_font.render(f"Health Regen Lvl: {self.health_regen_lvl}",False,"black")
        self.health_regen_font_rect = self.health_regen_font.get_rect(midleft = (20, 862))
        self.attribute_token_font = attribute_font.render(f"Attribute tokens: {self.attribute_points}",False,"white")
        self.attribute_token_font_rect = self.attribute_token_font.get_rect(midleft = (20, 645))

        self.attributes = {} # puts them into a dictionary where the key is the surf and the value is the rect
        self.attributes[self.max_health_font] = self.max_health_font_rect
        self.attributes[self.damage_font] = self.damage_font_rect
        self.attributes[self.proj_speed_font] = self.proj_speed_font_rect
        self.attributes[self.fire_rate_font] = self.fire_rate_font_rect
        self.attributes[self.speed_font] = self.speed_font_rect
        self.attributes[self.health_regen_font] = self.health_regen_font_rect
        self.attributes[self.attribute_token_font] = self.attribute_token_font_rect

        for attribute, rect in self.attributes.items(): # iterates through the dictionary to display gui
            screen.blit(attribute,rect)

    def reset(self): # resets attributes when game is restarted
        self.max_health_lvl = 0     
        self.health_regen_lvl = 0   
        self.damage_lvl = 0           
        self.proj_speed_lvl = 0      
        self.fire_rate_lvl = 0        
        self.speed_lvl = 0
        self.attribute_points = 0  

class Damage(pygame.sprite.Sprite): # class used for initializing damage numbers above enemy heads when they are hit with projectiles
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

class PickUp(pygame.sprite.Sprite): # class used for initializing pickups, which includes both xp orbs and powerups
    def __init__(self,x_pos,y_pos,nuke=False): # the nuke arg is used to auto set the drop to xp when a nuke goes off
        super().__init__()
        self.pickup_timer = 2000 # time required to pick up item before disappearing

        item_pickup = random.randrange(1,11) # rolls a 1/10 chance to spawn a random powerup instead of xp
        if item_pickup == 1:
            pickup_list = ["freeze","health","nuke","magnet"]
        else:
            pickup_list = ["xp"]

        self.pickup_type = random.choice(pickup_list)
        if nuke:
            self.pickup_type == "xp"
        
        if self.pickup_type == "freeze":
            frame1 = pygame.image.load('graphics/freeze.png').convert_alpha()
            frame1 = pygame.transform.scale_by(frame1, 0.05)
            sound = pygame.mixer.Sound('audio/freeze.wav')
        elif self.pickup_type == "magnet":
            frame1 = pygame.image.load('graphics/magnet.png').convert_alpha()
            frame1 = pygame.transform.scale_by(frame1, 0.025)
            sound = pygame.mixer.Sound('audio/magnet.wav')
        elif self.pickup_type == "health":
            frame1 = pygame.image.load('graphics/health.png').convert_alpha()
            frame1 = pygame.transform.scale_by(frame1, 2)
            sound = pygame.mixer.Sound('audio/health.wav')
            sound.set_volume(0.5)
        elif self.pickup_type == "nuke":
            frame1 = pygame.image.load('graphics/nuke.png').convert_alpha()
            frame1 = pygame.transform.scale_by(frame1, 0.01)
            sound = pygame.mixer.Sound('audio/nuke.wav')
        elif self.pickup_type == "xp":
            frame1 = pygame.image.load('graphics/xp_orb.png').convert_alpha()
            frame1 = pygame.transform.scale_by(frame1, 2)
            sound = pygame.mixer.Sound('audio/collect.wav')
            sound.set_volume(0.1)

        frame2 = pygame.image.load('graphics/None.png').convert_alpha()
        self.frames = [frame1,frame2]
        self.sound = sound
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
    
    def pickup(self): # func that executes when the player rect collides with the pickup rect
        self.sound.play()
        if self.pickup_type == "nuke":
            ship.powerup_count += 1
            ship.nuke_timer = 300
            for sprite in sorted(monster_group.sprites(),key = lambda sprite: sprite.rect.centery):
                pickup_group.add(PickUp(sprite.rect.centerx,sprite.rect.centery,True))
            monster_group.empty()
            asteroid_group.empty()
        if self.pickup_type == "xp":
            ship.xp_count += 1
            ship.xp += 50
        if self.pickup_type == "magnet":
            ship.powerup_count += 1
            ship.magnet_timer = 250
        if self.pickup_type == "health":
            ship.powerup_count += 1
            ship.remaining_health += (ship.max_health / 4)
            if ship.remaining_health > ship.max_health:
                ship.remaining_health = ship.max_health
        if self.pickup_type == "freeze":
            ship.powerup_count += 1
            ship.freeze_timer = 250
        self.kill()

    def move(self,x_pos,y_pos): # function executes upon picking up a magnet item
        dx = ship.rect.centerx - x_pos
        dy = ship.rect.centery - y_pos
        distance = math.hypot(dx, dy)
        dx, dy = dx / distance, dy / distance
        return dx, dy

pygame.init() # initializes pygame modules
clock = pygame.time.Clock()
game_timer = pygame.time.Clock()
screen = pygame.display.set_mode((1700,900))
running = True # used for game loop
game_active = False # used for title screen
alive = True # used for when player is alive
dt = 0 # delta time: used for fps calculation at the end of the game loop so it runs at a fixed fps

soundtrack = pygame.mixer.Sound('audio/soundtrack.wav')
soundtrack.set_volume(0.01)
soundtrack.play(loops = -1)

# fonts
title_font = pygame.font.Font('graphics/PixelType.ttf', 150)
gui_font = pygame.font.Font('graphics/PixelType.ttf', 75)
small_font = pygame.font.Font('graphics/PixelType.ttf', 40)
attribute_font = pygame.font.Font('graphics/PixelType.ttf', 32)
mutation_font = pygame.font.Font('graphics/PixelType.ttf',60)

# sprite groups
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

# initializes a 3x3 of the space background to make it bigger
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

ship = Player(0,0,1.5,4) # initializes player object
camera_group.add(ship) # adds the ship to camera_group

upgrades = Upgrades() # initializes upgrades object

# custom events used in the event loop that happen at select intervals
fire_bullet = pygame.USEREVENT + 1
pygame.time.set_timer(fire_bullet, ship.fire_rate)

spawn_asteroid = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_asteroid, 3000)

monster_timer = 2500
spawn_monster = pygame.USEREVENT + 3
pygame.time.set_timer(spawn_monster, monster_timer)

upgrade_timer = pygame.USEREVENT + 5
pygame.time.set_timer(upgrade_timer, 100)

regen_health = pygame.USEREVENT + 6
pygame.time.set_timer(regen_health,ship.health_regen)

allow_upgrades = True # creates a cooldown in applying attributes
blit_health = False # used to display the player's health bar (if player health is full, this value is set to False)

# initializing the variables used for tracking game time and displaying it properly
minutes = 0
seconds = 0

while running: # game loop

    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT: # event occurs when the player presses the x on the window
            running = False
        elif not game_active: # used to prevent game from starting on the title screen
            break
        if event.type == fire_bullet: # creates bullet
            pygame.time.set_timer(fire_bullet, ship.fire_rate)
            projectile_group.add(ship.create_bullet())
        if event.type == spawn_asteroid: # spawns asteroid
            asteroid_group.add(create_asteroid())
        if event.type == spawn_monster: # spawns monster
            monster_group.add(create_monster(minutes,seconds // 1000))
            pygame.time.set_timer(spawn_monster, monster_timer)
        if event.type == upgrade_timer: # allows the player to upgrade atributtes
            allow_upgrades = True
        if event.type == regen_health: # regens player health
            pygame.time.set_timer(regen_health,ship.health_regen)
            if ship.remaining_health < ship.max_health:
                ship.remaining_health += upgrades.health_regen_lvl
                if ship.remaining_health > ship.max_health:
                    temp = ship.remaining_health - ship.max_health
                    ship.remaining_health -= temp
        
    if not game_active: # title screen
        screen.blit(ground.ground_surf,ground.ground_rect)
        
        ship.animate_ship(True)
        camera_group.custom_draw(ship,alive,game_active)

        title = title_font.render('SPACE ODYSSEY',False,'white')
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

    else: # else statement runs once game_active is set to True
        if alive:
            screen.fill('black')

            # powerup timers decrease every loop if they are above 0
            if ship.magnet_timer > 0:
                ship.magnet_timer -= 1
            if ship.freeze_timer > 0:
                ship.freeze_timer -= 1

            keys = pygame.key.get_pressed() # gets player input
            moved = False

            # controls player 
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

            camera_group.custom_draw(ship,alive,game_active) # calls the custom_draw func to display all sprites on the screen

            lvl = gui_font.render(f'lvl {ship.lvl}',False,'white')
            lvl_rect = lvl.get_rect(midbottom = (575,875))
            screen.blit(lvl,lvl_rect)
            player_level.xp_bar_blit(ship.xp,ship.lvl)
            
            # displays time on the screen
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

            if ship.remaining_health == ship.max_health: # removes health bar if player is at max health
                blit_health = False
            else:
                blit_health = True

            max_health = pygame.Surface((75 * blit_health,9))
            max_health.fill('red')
            max_health_rect = max_health.get_rect(center = (850,390))
            screen.blit(max_health,max_health_rect)

            if ship.remaining_health > 0: # overlaps a green rect over the red rect based on the player's remaining health
                pixel_per_percent = 75 / (ship.max_health / ship.remaining_health)
                remaining_health = pygame.Surface((pixel_per_percent * blit_health,9))
                remaining_health.fill('green')
                remaining_health_rect = max_health.get_rect(center = (850,390))
                screen.blit(remaining_health,remaining_health_rect)

            else: # player dies and the game ends
                player_explosion = Explosion(ship.position.x,ship.position.y,1)
                explosion_group.add(player_explosion)
                ship.death_sound.play()
                ship.death_timer = 125
                alive = False
            
            allow_upgrades = upgrades.lvl_up(allow_upgrades, 0)
            upgrades.print_gui() # prints attribute gui

            if ship.nuke_timer > 0: # creates a fading effect when a nuke powerup is picked up
                nuke = pygame.Surface((1700,900))
                nuke.fill('white')
                nuke_rect = nuke.get_rect(center = (850,450))
                nuke.set_alpha(ship.nuke_timer)
                screen.blit(nuke,nuke_rect)
                ship.nuke_timer -= 5
            
        else: # code executes if alive == False
            screen.fill('black')
            camera_group.custom_draw(ship,alive,game_active)
            soundtrack.stop()

            if ship.death_timer != 1: # used to create a delay between the player dying and the game ending
                ship.death_timer -= 1
            if ship.death_timer == 1:
                game_over(seconds,minutes)
            
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    soundtrack.play()
                    alive = restart_game(sprite_groups) # restarts the game after the player presses space
                    seconds = 0
                    minutes = 0
                    game_timer = pygame.time.Clock()

    pygame.display.update() # updates the display
    dt = clock.tick(60) / 1000 # stabilizes framerate

pygame.quit() # application closes