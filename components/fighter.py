import libtcodpy as libtcod
from random import randint

from game_messages import Message

class Status_Effects:
    def __init__(self,grace=False,accurate=False,poisoned=False,poison_timer=False):
        self.grace = grace
        self.accurate = accurate
        self.poisoned=poisoned
        self.poison_timer=poison_timer

class Jobs:
    def __init__(self,fighter_level=0,magician_level=0,cleric_level=0,thief_level=0):
        self.fighter_level = fighter_level
        self.magician_level = magician_level
        self.cleric_level=cleric_level
        self.thief_level=thief_level

class Fighter:
    def __init__(self, hp,mana, defense, power,willpower,constitution,attack_dice_minimum,attack_dice_maximum,ac=0,accuracy=0, xp=0,race=None,levels_quickly=False,cant_wear_armour=False,large=False,small=False,
                 herbivore=False,carnivore=False,sharp_claws=False,no_arms=False,no_legs=False,bloodthirsty=False,eight_arms=False,swimmer=False,resistance=None,one_with_nature=False,golem=False
                 ,status_effects=None,job=None,nutrition=None,shield=None,hates_law=False,flying=False):
        self.base_max_hp = hp
        self.hp = hp
        self.mana = mana
        self.base_max_mana = mana
        self.base_defense = defense
        self.base_power = power
        self.base_constitution=constitution
        self.base_willpower = willpower
        self.attack_dice_minimum = attack_dice_minimum
        self.attack_dice_maximum = attack_dice_maximum
        self.xp = xp
        self.race = race
        self.levels_quickly = levels_quickly
        self.cant_wear_armour = cant_wear_armour
        self.large = large
        self.small = small
        self.herbivore = herbivore
        self.carnivore = carnivore
        self.sharp_claws = sharp_claws
        self.no_arms = no_arms
        self.no_legs = no_legs
        self.bloodthirsty = bloodthirsty
        self.eight_arms = eight_arms
        self.swimmer = swimmer
        self.resistance = resistance
        self.one_with_nature = one_with_nature
        self.golem = golem
        self.base_ac = ac
        self.base_accuracy = accuracy
        self.status_effects = status_effects
        self.job = job
        self.nutrition = nutrition
        self.shield = shield
        self.hates_law = hates_law
        self.flying = flying

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + self.constitution + bonus

    @property
    def max_mana(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_mana_bonus
        else:
            bonus = 0

        return self.base_max_mana + self.willpower + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def willpower(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.willpower_bonus
        else:
            bonus = 0

        return self.base_willpower + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    @property
    def constitution(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.constitution_bonus
        else:
            bonus = 0

        return self.base_constitution + bonus

    @property
    def ac(self):
        dex_bonus=0
        if self.defense > 3:
            dex_bonus = round(self.defense/3)
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.ac_bonus + dex_bonus
        else:
            bonus = 0 + dex_bonus

        if self.owner.fighter.status_effects.grace == True:
            return (self.base_ac + bonus) * 2
        else:
            return self.base_ac + bonus

    @property
    def accuracy(self):
        power_bonus = 0
        if self.power > 3:
            power_bonus = round(self.power / 3)
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.accuracy_bonus + power_bonus
        else:
            bonus = 0 + power_bonus

        if self.owner.fighter.status_effects.accurate == True:
            return (self.base_accuracy + bonus) * 2
        else:
            return self.base_accuracy + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []

        damage = randint(self.attack_dice_minimum,self.attack_dice_maximum)
        hit_chance=randint(1,20+self.accuracy)
        dodge_chance = randint(1, 20 + self.ac)

        if hit_chance > dodge_chance:
            if damage > 0:
                results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                    self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
                results.extend(target.fighter.take_damage(damage))
            else:
                results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                    self.owner.name.capitalize(), target.name), libtcod.white)})
        else:
            results.append({'message': Message('{0} attacks {1} but misses.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})

        return results
