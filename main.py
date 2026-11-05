lazy import math
lazy import random
lazy import time

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
    def __init__(self, name: str, hp: int, attack: int, defense: int, wallet: int = 0, starting_place="home", inventory: dict = {}):
        super().__init__(name, hp, attack, defense)
        self.place = starting_place
        self.wallet = wallet
        self.inventory = inventory

player = Hero(PLAYER_NAME, 100, 25, 15, wallet=10)

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
        "enemies": ["frog", "very meanacing skeleton"],
        "isShop": False,
    },
    "market": {
        "description": "City's market",
        "exits": ["home", "city"],
        "items": [],
        "enemies": ["fire-breathing dragon"],
        "isShop": True,
    },
}

products = {
    "bwoken sword": {
        "price": None,
        "sell_price": 10,
        "description": "A sword that is broken in half, it has no use in combat, but it can be sold for a good price.",
        "effect": [None, None]
    },
    "burger": {
        "price": 5,
        "sell_price": 2,
        "description": "A burger that is half-eaten, but still edible. Restores 20 HP.",
        "effect": ["hp", 20]
    },
    "potion": {
        "price": 10,
        "sell_price": 5,
        "description": "A potion that restores all HP.",
        "effect": ["hp", 100 - player.hp]
    },
    "shield": {
        "price": 15,
        "sell_price": 7,
        "description": "A shield that increases your defense by 5.",
        "effect": ["defense", 5]
    },
}

enemies = [
    {
        "name": "frog",
        "hp": 20,
        "attack": 5,
        "defense": 2,
    },
    {
        "name": "very meanacing skeleton",
        "hp": 125,
        "attack": 25,
        "defense": 15,
    },
    {
        "name": "fire-breathing dragon",
        "hp": 200,
        "attack": 35,
        "defense": 35,
    },
]

def choose_enemy(place) -> Entity | None:
    enemies_list = place[player.place]["enemies"]
    if enemies_list:
        enemy_name = random.choice(enemies_list)
        enemy_data = next((enemy for enemy in enemies if enemy["name"] == enemy_name), None)
        if enemy_data is None:
            return None
        return Entity(
            enemy_data["name"],
            enemy_data["hp"],
            enemy_data["attack"],
            enemy_data["defense"],
        )
    else:
        return None
    
def lose():
    print("You lost!")
    quit()
    
def explore():
    print(f"{player.name} decided to explore", end="")
    for _ in range(3):
        time.sleep(0.67)
        print(".", end="")
    print()
    match random.randint(1, 3):
        case 1: # Didnt find anything
            print("You didn't find anything! :(")
        case 2: # Found enemy
            enemy = choose_enemy(places)
            if enemy is not None:
                print(f"You found a/an {enemy.name}!")
                match input("Do you want to fight it? (y/n): ").lower():
                    case "y":
                        print(f"You chose to fight the {enemy.name}!")
                        time.sleep(1)
                        defeated_enemy = False
                        while enemy.hp > 0 and player.hp > 0:
                            print(f"Fighting: {enemy.name} (HP: {enemy.hp}, ATK: {enemy.atk}, DEF: {enemy.defense})")
                            print("What will you do?")
                            print("1 - Attack")
                            print("2 - Defend")
                            print("3 - Run")
                            match int(input("Choose your option: ")):
                                case 1:
                                    player.attack(enemy)
                                    print(f"You attacked the {enemy.name}!")
                                    if enemy.hp > 0:
                                        time.sleep(1)
                                        enemy.attack(player)
                                        print(f"The {enemy.name} attacked you!")
                                        if player.hp <= 0:
                                            lose()
                                    else:
                                        print(f"You defeated the {enemy.name}!")
                                        defeated_enemy = True
                                case 2:
                                    enemy_atk_before_defense = enemy.atk
                                    enemy.atk = max(1, enemy.atk - player.defense)
                                    print(f"You defended against the {enemy.name}'s attack!")
                                    print(f"It did {enemy.atk} damage to you!")
                                    enemy.atk = enemy_atk_before_defense
                                    if player.hp <= 0:
                                        lose()
                                case 3:
                                    match random.randint(1, 3):
                                        case 1:
                                            print("You successfully ran away!")
                                        case _:
                                            print("The enemy catched up to you and attacked!")
                            if defeated_enemy:
                                player.wallet += random.randint(enemy.hp // 2, enemy.hp * 2)
                    case "n":
                        print("You chose not to fight.")
            print("You didn't find anything! :(")
        case 3: # Found item
            if places[player.place]["items"]:
                item = places[player.place]["items"].pop()
                print(f"You found a/an {item}!")
    
def game():
    print(f"=== Welcome to the minigame, {player.name}! ===")
    while True:
        player_location = places[player.place]
        print("===============================================================================")
        print(f"You're currently in {player.place}, {player_location["description"]}")
        print("===============================================================================")
        print("What do you want to do?")
        print("1 - Explore")
        print("2 - Go to another location")
        print("3 - Use an item")
        if player_location["isShop"]:
            print("4 - Go to the shop")
        print("===============================================================================")
        match input("Choose your option: "):
            case "1":
                explore()
            case "2":
                print("Where do you want to go?")
                print("Available locations:")
                for exit in player_location["exits"]:
                    print(f"\t- {exit}")
                destination = input("Enter the location you want to go to: ")
                if destination in player_location["exits"]:
                    player.place = destination
                    print(f"You went to {destination}.")
            case "3":
                if player.inventory:
                    print("Which item do you want to use?")
                    for item in player.inventory:
                        print(f"\t- {item}")
                    item_to_use = input("Enter the item you want to use: ")
                    if item_to_use in player.inventory:
                        # Implement item usage logic here
                        pass
                    else:
                        print("You don't have that item!")
                else:
                    print("You don't have any items in your inventory!")
            case "4":
                if player_location["isShop"]:
                    print("Welcome to the shop! What do you want to do?")
                    print("1 - Sell Items")
                    print("2 - Buy Items")
                    match input("Choose your option: "):
                        case "1":
                            print("Which item do you want to sell?")
                            for key, value in products.items():
                                print(f"\t- {key} (Sell Price: {value['sell_price']})")
                            item_to_sell = input("Enter the item you want to sell: ")
                            if item_to_sell in player.inventory:
                                player.wallet += products[item_to_sell]["sell_price"]
                                player.inventory.pop(item_to_sell)
                                print(f"You sold {item_to_sell} for {products[item_to_sell]['sell_price']} coins!")
                            else:
                                print("You don't have that item!")
                        case "2":
                            print("Which item do you want to buy?")
                            for key, value in products.items():
                                print(f"\t- {key} (Price: {value['price']})")
                            item_to_buy = input("Enter the item you want to buy: ")
                            if item_to_buy in products and player.wallet >= products[item_to_buy]["price"]:
                                player.wallet -= products[item_to_buy]["price"]
                                player.inventory[item_to_buy] = products[item_to_buy]
                                print(f"You bought {item_to_buy} for {products[item_to_buy]['price']} coins!")
                            else:
                                print("You can't afford that item!")

if __name__ == "__main__":
    game()