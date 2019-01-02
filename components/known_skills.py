import libtcodpy as libtcod

from game_messages import Message

class Skills:
    def __init__(self, skill_capacity):
        self.skill_capacity = skill_capacity
        self.skills = []

    def add_skill(self, skill):
        results = []

        if len(self.skills) >= self.skill_capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': skill,
                'message': Message('You pick up the {0}!'.format(skill.name), libtcod.blue)
            })

            self.skills.append(skill)

        return results

    def use(self, skill_entity, **kwargs):
        results = []

        skill_component = skill_entity.skill

        if skill_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': skill_entity})
        else:
                kwargs = {**skill_component.function_kwargs, **kwargs}
                item_use_results = skill_component.use_function(self.owner, **kwargs)

                results.extend(item_use_results)

        return results