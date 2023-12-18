
class Monster:
    def __init__(self,func):
        self.func = func

class Attacks:
    def bite(self):
        print("the monster used bite")
    def strike(self):
        print("the monster used strike")
    def slash(self):
        print("the monster used slash")
    def kick(self):
        print("the monster used kick")

attacks = Attacks()
monster = Monster(func = attacks.bite)
monster.func()
# create a monster class with a parameter called func, store this func as parameter
# create another class, called attacks, that has 4 methods:
# bite, strike, slash, kick (each method just prints some text)

# create a monster object and give it one of the attack methods from the attack class