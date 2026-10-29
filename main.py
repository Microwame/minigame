import math
import random

player_name = input("Choose your name: ")

class Entity:
    def __init__(self, name: str, hp: int, attack: int, defense: int):
        self.name = name
        self.hp = hp
        self.atk = attack
        self.defense = defense
    def attack(self, object: Entity):
        base_atk = max(1, max(1, self.atk - object.defense))
        object.hp -= random.randint(
                                math.floor(base_atk / 0.5),
                                base_atk * 2
                                )
        if object.hp <= 0:
            object.die()
    def die(self):
        if self.name != player_name:
            del self
        else:
            lose()
            
player = Entity(player_name, 100, 25, 15)
    
def lose():
    print("You lost!")
    quit()