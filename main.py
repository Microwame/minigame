import math
import random

PLAYER_NAME = input("Choose your name: ")

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
        if self.name != PLAYER_NAME:
            del self
        else:
            lose()

class Hero(Entity):
    def __init__(self, name: str, hp: int, attack: int, defense: int, starting_place="home"):
        super().__init__(name, hp, attack, defense)
        self.place = starting_place

player = Hero(PLAYER_NAME, 100, 25, 15)

places = {
    "home": {
        "description": f"House of {player.name}",
        "exits": ["city", "market"],
        "items": ["bwoken sword"],
        "enemies": [],
        "isShop": False,
    },
    "city": {
        "description": "big city",
        "exits": ["home", "market"],
        "items": ["half-eaten burger"],
        "enemies": ["Enemy1", "Enemy2"],
        "isShop": False,
    },
    "market": {
        "description": "City's market",
        "exits": ["home", "city"],
        "items": [],
        "enemies": ["Enemy3"],
        "isShop": True,
    },
}

enemies = {
    "Enemy1": {
        "name": "enemy1",
        "hp": "100",
        "attack": "25",
        "defense": "15",
    },
    "Enemy3": {
        "name": "enemy2",
        "hp": "100",
        "attack": "25",
        "defense": "15",
    },
    "Enemy3": {
        "name": "enemy2",
        "hp": "100",
        "attack": "25",
        "defense": "15",
    },
}

def choose_enemy(place):
    enemies_list = places[player.place]["enemies"]
    if enemies_list:
        return enemies[random.choice(enemies_list)].items()
    
def lose():
    print("You lost!")
    quit()
    
def game():
    print(f"=== Welcome to the minigame, {player.name}! ===")
    while True:
        print(f"You're currently in {player.place}, {places[player.place]["description"]}")
        print("What do you want to do?")
        print("1 - Explore")
        print("2 - Go to another location")
        if places[player.place]["isShop"]:
            print("3 - Sell Items")
            print("4 - Buy Items")