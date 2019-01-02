import libtcodpy as libtcod

from game_messages import Message

class Status_Effects:
    def __init__(self,grace=False,accurate=True):
        self.grace = grace
        self.accurate = accurate

class Fighter:
    def __init__(self, hp, defense, power,willpower,constitution,attack_dice_minimum=None,attack_dice_maximum=None, xp=0,race=None,levels_quickly=False,cant_wear_armour=False,large=False,small=False,
                 herbivore=False,carnivore=False,sharp_claws=False,no_arms=False,no_legs=False,bloodthirsty=False,eight_arms=False,swimmer=False,resistance=None,one_with_nature=False,golem=False
                 ,ac=0,will=0,status_effects=None,nutrition=None,shield=None):
        self.base_max_hp = hp
        self.hp = hp
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
        self.base_will = will
        self.status_effects = status_effects
        self.nutrition = nutrition
        self.shield = shield

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

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
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.ac_bonus
        else:
            bonus = 0

        if self.owner.fighter.status_effects.grace == True:
            return (self.base_ac + bonus) * 2
        else:
            return self.base_ac + bonus

    @property
    def will(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.will_bonus
        else:
            bonus = 0

        if self.owner.fighter.status_effects.accurate == True:
            return (self.base_will + bonus) * 2
        else:
            return self.base_will + bonus

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

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})

        return results
