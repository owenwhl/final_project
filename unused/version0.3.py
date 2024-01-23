import pygame
import random

# pygame setup
pygame.init()
width = 1650
height = 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

camera_group = pygame.sprite.Group()


player = pygame.image.load("graphics/unused/ship_up0.png")

enemy = pygame.image.load("graphics/unused/enemy.png")
scale = (50,50)
enemy = pygame.transform.scale(enemy, scale)

class Player:
    def __init__(self,x,y):
        self.position = pygame.Vector2(x, y) # position is determined by a 2d vector
        self.velocity = pygame.Vector2(0, 0) # velocity is a seperate vector starting at 0,0 
        self.acceleration = 0.3 # larger number makes player faster
        self.friction = 0.03 # larger number makes player slower (cannot be 1)

    def move(self, direction): # move method takes an integer as input
        self.velocity += direction * self.acceleration # calculates velocity by multiplying by acceleration
        self.velocity.x *= 1 - self.friction           # and then divides (mutiply by decimal) by friction
        self.velocity.y *= 1 - self.friction

        self.position += self.velocity # velocity is then added to position

class Enemy:
    def __init__(self,x,y,health):
        self.health = health
        self.position = pygame.Vector2(x, y)

    def move(self):
        direction = ["up","down","left","right"] # list of four cardinal directions
        if self.position.x <= 0: # removes direction if enemy is at the edge of the screen
            direction.remove("left")
        elif self.position.x >= screen.get_width() - 50:
            direction.remove("right")
        if self.position.y <= 0:
            direction.remove("up")
        elif self.position.y >= screen.get_height() - 50:
            direction.remove("down")

        choice = random.choice(direction) # chooses a random direction from the list

        if choice == "left": # moves enemy
            self.position.x -= 50
        elif choice == "right":
            self.position.x += 50
        elif choice == "up":
            self.position.y -= 50
        elif choice == "down":
            self.position.y += 50

ship = Player(0, 0) 
n_monsters = 10
monsters = []
for i in range(n_monsters):
    monsters.append(Enemy(random.randrange(50,1600,50),random.randrange(50,750,50),100))

MOVE = pygame.USEREVENT + 1 # custom event that allows the enemy to move
pygame.time.set_timer(MOVE, 100) # evenet occurs every 100 frames

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOVE: # every 100 frames execute the move function from Enemy class
            for i in range(n_monsters):
                monsters[i].move()

    screen.fill("white")
    screen.blit(player, ship.position)

    keys = pygame.key.get_pressed()

    # screen.blit(player, ship.position) # updates the player position every frame

    for i in range(n_monsters):
        screen.blit(enemy, monsters[i].position) # updates the enemy position every frame

    move_direction = pygame.Vector2(0, 0) # resets direction vector to 0 every frame.
    # ** velocity is calculated seperately using the move method. 5 represents the base speed and changes
    # depending on the velocity

    if keys[pygame.K_a]:
        move_direction.x -= 5

    if keys[pygame.K_d]:
        move_direction.x += 5

    if keys[pygame.K_w]:
        move_direction.y -= 5

    if keys[pygame.K_s]:
        move_direction.y += 5

    ship.move(move_direction) # using the move method along with the variable move_direction defined above

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()