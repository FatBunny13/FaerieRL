class Equippable:
    def __init__(self, slot, power_bonus=0,willpower_bonus=0, defense_bonus=0,constitution_bonus=0, max_hp_bonus=0,max_mana_bonus=0,ac_bonus=0,accuracy_bonus=0):
        self.slot = slot
        self.power_bonus = power_bonus
        self.willpower_bonus = willpower_bonus
        self.defense_bonus = defense_bonus
        self.constitution_bonus = constitution_bonus
        self.max_hp_bonus = max_hp_bonus
        self.ac_bonus = ac_bonus
        self.accuracy_bonus = accuracy_bonus
        self.max_mana_bonus = max_mana_bonus
