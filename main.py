import os
import time
from playsound import playsound
import random
import threading

#print("Josh has become death")
#print("I am the bringer of death")

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
        self.inventory = []
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

    def calculate_defence(self):
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

    def build_enemy(self, information):
        self.level = float(information["level"])
        base_hp = 10
        real_hp = base_hp * random.uniform((self.level) * .8, (self.level) * 1.2)
        self.hp = real_hp
        self.max_hp = real_hp
        self.name = information["name"]
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
        elif options == "run" or options == "r":
            can_escape = enemy.attempt_escape(player)
            if can_escape:
                print("Escaped!")
            else:
                print("Failed escape")
        elif options == "item" or options == "i":
            pass
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

