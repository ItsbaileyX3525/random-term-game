import os
import time
from playsound import playsound
import random
import threading
import json

#print("Josh has become death")
#print("I am the bringer of death")

equipment_list = {}

with open("equipment.json" , "r", encoding="utf-8") as f:
    equipment_list = json.load(f)

sounds = {
    "fight_start" : "sounds/pokemon-battle.mp3",
    "genug" : "sounds/genug.mp3",
    "doit" : "sounds/doit.mp3",
        }

def _playsound(sound):
    playsound(sound)

def playSound(sound):
    t1 = threading.Thread(target=_playsound, args=(sound,))
    t1.start()
    return

def clamp(n, min, max):
    if n < min:
        return min
    if n > max:
        return max
    return n

class Player(): #TODO: Finish player class
    def __init__(self):
        self.hp = 100.0
        self.level = 1.0
        self.atkPwr = 1.0
        self.defence = 0.0
        self.critChance = 1.0 #1 = 1%
        self.armor = {
            "helmet" : "None",
            "chestplate" : "None",
            "leggings" : "None",
            "boots": "None"
                }
        self.inventory = [    
                { #Dynamically grows
                    "minor_health_potion" : 
                    {
                        "type" : "potion",
                        "potion_type" : "health",
                        "strength" : "1", #1 is lowest possible strength
                        "available" : 1,
                    }
                },
                
            ]
        self.mainhand = {
            "item_equipped" : False,
            "item_name" : "None",
            "item_type" : "None",
            "item_properties" : {},
                }
        self.offhand = {
            "item_equipped" : False,
            "item_name" : "None",
            "item_type" : "None",
            "item_properties" : {},
                }
    
    def get_hp(self):
        return self.hp

    def use_item(self, page, itemIdx):
        print("using item")
        item = ""
        realItemIdx = (itemIdx - 1) + (10 * (page - 1))
        for itemName, itemData in self.inventory[realItemIdx].items():
            item = itemName
        print("Used", item)

    def get_item_list(self, page = 1):
        itemsPerPage = 10
        startIdx = (page - 1) * itemsPerPage
        endIdx = startIdx + itemsPerPage

        pageItems = self.inventory[startIdx:endIdx]

        if not pageItems:
            return "No items found on ts page"

        itemList = ""

        for i, itemDict in enumerate(pageItems, start=startIdx + 1):
            for itemName, itemData in itemDict.items():
                available = itemData.get("available", 0)
                itemList += f"{i} - {itemName} (Amount: {available})\n"
        
        itemList += f"page {page}"

        return itemList 
                

    def get_atk_pwr(self):
        totalPower = self.atkPwr
        if self.mainhand["item_type"] == "weapon":
            totalPower = self.atkPwr * self.mainhand["item_properties"]["atk_boost"]
        #If they dont have a weapon, just default to assuming its nothing in the hand, even if its a potion...
        return totalPower

    def get_random_atk(self):
        curr_pwr = self.get_atk_pwr()
        rand_range = random.uniform((curr_pwr * 0.8), (curr_pwr * 1.2))
        crit_chance = random.randint(0,100)
        max_chance = 100 - self.critChance
        if crit_chance >= max_chance:
            rand_range *= 1.15
        return round(rand_range, 2)

class Enemy(): #TODO: Finish enemy class
    def __init__(self):
        self.max_hp = 0.0
        self.hp = 0.0
        self.level = 1.0
        self.name = ""
        self.atkPwr = 0.0
        self.defence = 0.0
        self.armor = {
            "helmet" : "None",
            "chestplate" : "None",
            "leggings" : "None",
            "boots" : "None",
                }
        self.mainhand = {}
        self.offhand = {}

    def get_health(self):
        return self.hp

    def get_name(self):
        return self.name

    def turn(self, player):
        pass

    def attempt_escape(self, player):
        chance = 100 #100% chance of escape
        hp_diff = (self.max_hp / self.hp) / 10
        if hp_diff > .60: #Have at least 60% of hp left
            chance -= clamp(6.25 * (1 + hp_diff), 6.25, 35)

        if self.level > player.level: #If higher than player level
            diff = self.level - player.level
            chance -= clamp((2.25 * diff), 2.25, 25)

        rng = random.randint(0,100)
        if chance > rng:
            return True
        else:
            return False


    def hit(self, amount = 1.0):
        defence_modifier = clamp(random.uniform((self.defence) * .8, (self.defence) * 1.2), 1, self.defence * 1.2)
        real_damage = (amount / defence_modifier)
        self.hp -= real_damage
        self.hp = round(self.hp, 2)
        if self.hp < 0:
            self.hp = 0.0
        return self.hp

    def get_rarity(self):
        tiers = ["Wooden", "Stone", "Iron", "Diamond", "Netherite"]

        level = clamp(self.level, 3, 50)

        if level >= 50:
            return "Netherite"

        targetIdx = (level - 3) / 47.0 * 4.0

        chosenIdx = int(round(random.gauss(targetIdx, .8)))

        chosenIdx = clamp(chosenIdx, 0, len(tiers) - 1)

        return tiers[chosenIdx]

    def pick_helmet(self):
        rarity = self.get_rarity()

        helmetName, helmetStats = random.choice(list(equipment_list["Armor"][rarity]["Helmets"].items()))
        print(helmetName, "\n", helmetStats)

    def pick_chestplate(self):
        rarity = self.get_rarity()

        chestplateName, chestplateStats = random.choice(list(equipment_list["Armor"][rarity]["Chestplates"].items()))
        print(chestplateName, "\n", chestplateStats)
    
    def pick_leggings(self):
        rarity = self.get_rarity()

        leggingsName, leggingsStats = random.choice(list(equipment_list["Armor"][rarity]["Leggings"].items()))
        print(leggingsName, "\n", leggingsStats)

    def pick_boots(self):
        rarity = self.get_rarity()

        bootsName, bootsStats = random.choice(list(equipment_list["Armor"][rarity]["Boots"].items()))
        print(bootsName, "\n", bootsStats)

    def build_enemy(self, information):
        self.level = float(information["level"])
        base_hp = 10
        real_hp = base_hp * random.uniform((self.level) * .8, (self.level) * 1.2)
        
        helmetChance = 0
        chestplateChance = 0
        leggingsChance = 0
        bootsChance = 0

        self.hp = real_hp
        self.max_hp = real_hp
        self.name = information["name"]

        self.atkPwr = clamp((self.level * random.uniform(.1, 1.425)), .8, 999999999)
        self.defence = self.level * random.uniform(0, 1.35)

        if self.level >= 3: #Start gaining armor at level 3 onwards
            helmetRN = random.randint(0, 10)
            chestplateRN = random.randint(0, 10)
            leggingsRN = random.randint(0, 10)
            bootsRN = random.randint(0, 10)
            helmetChance = helmetRN * (self.level * .8)
            chestplateChance = chestplateRN * (self.level * .8)
            leggingsChance = leggingsRN * (self.level * .8)
            bootsChance = bootsRN * (self.level * .8)

            if helmetChance >= 45: #Helmet and boots don't provide as much protection like minecraft :3
                self.pick_helmet()
            if chestplateChance >= 60:
                self.pick_chestplate()
            if leggingsChance >= 60:
                self.pick_leggings()
            if bootsChance >= 45:
                self.pick_boots()

        #Add more stuff here tbf

def input_pause():
    input("Please press enter to continue... ")

def create_fight(enemyInformation = {}):
    playSound(sounds["fight_start"])
    enemy = Enemy()
    enemy.build_enemy(enemyInformation)
    newHealth = 0.0
    while enemy.get_health() > 0:
        options = input("What would you like to do?\natk - attack the enemy\nrun - attempt to run away\nitem - use an item\n").lower().strip()
        if options == "atk" or options == "a":
            playerAttack = player.get_random_atk()
            newHealth = enemy.hit(playerAttack)
            print(f"Dealt {playerAttack} damage!")
            print(f"{enemy.get_name()} has {newHealth}hp left!")
            enemy.turn(player)
        elif options == "run" or options == "r":
            can_escape = enemy.attempt_escape(player)
            if can_escape:
                print("Escaped!")
                break
            else:
                print("Failed escape")
                enemy.turn(player)
        elif options == "item" or options == "i":
            page = 1
            while True:
                print(player.get_item_list(page))
                print("Type 'page [page]' to go to another page or 'quit' to finish")
                item = input("Please enter the number of item you wish to use: ")
                if item.startswith("page"):
                    newPage = item.split(" ")
                    page = int(newPage[1])
                    continue
                elif item.startswith("exit"):
                    break
                player.use_item(page, int(item))
            enemy.turn(player)
        else:
            print("That is not a valid action!")
            input_pause()
            continue

        input_pause()
    print("Enemy killed!")


#playsound("Downloads/genug.mp3")

print("Welcome to your journey")
input_pause()
print("Here is where your story is told, fight enemies, get gold and win the hearts of your entire home village!")
input_pause()
cont = input("Are you ready to get started on your journey to the forbidden world? (Y/n) ").lower()
if cont == "n" or cont == "no":
    print("Oh that's a shame, come back when you are ready then.")
    time.sleep(2)
    exit()

print("Great. Let the story begin.")
input_pause()
player = Player()

print("You think to yourself, 'What a wonderful morning! I can't wait to start adventuring today, I wonder what foes await me!'")
input_pause()

playSound(sounds["doit"])
cont = input("You look around and just a little ahead of you, you see a slime, just minding its own business. Would you like to go attack it? (y/N) ").lower().strip()

if cont == "n" or cont == "no" or cont == "":
    print("You decide that the slime is not worth your time and you continue on with your day")
else:
    print("You walk over to the slime and say to it, 'Mr. Slime. I regret to inform you that I will be battling you now!'")
    create_fight({"name" : "Slime", "level" : "1"})

