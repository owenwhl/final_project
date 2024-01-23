class Monster:
    def __init__(self,health,energy):
        self.health = health
        self.energy = energy

    def attack(self,amount):
        print('the monster has attacked')
        print(f'{amount} damage has been dealt')
        self.energy -= 20
    
    def move(self,speed):
        print('the monster has moved')
        print(f'it has a speed of {speed}')

class Scorpion(Monster):
    def __init__(self,scorpion_health,scorpion_energy,poison_damage):
        super().__init__(health = scorpion_health,energy = scorpion_energy)
        self.poison_damage = poison_damage

    def attack(self):
        print('the scorpion has attacked')
        print(f'{self.poison_damage} poison damage has been dealt')
        self.energy -= 20

class Shark(Monster):
    def __init__(self,speed,health,energy):
        # Monster.__init__(self,health,energy)
        super().__init__(health,energy)
        self.speed = speed

    def bite(self):
        print("the shark has bitten")

    def move(self):
        print('The shark has moved')
        print(f'The speed of the shark is {self.speed}')

# exercise
# create a scorpion class that inherits from monster
# health and energy from the parent
# poison_damage attribute
# overwrite the damage method to show poison damage


shark = Shark(speed = 120, health = 100, energy = 80)
scorpion = Scorpion(scorpion_health = 100, scorpion_energy = 75, poison_damage = 10)
print(scorpion.health)
print(scorpion.energy)