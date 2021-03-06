import libtcodpy as libtcod

from death_functions import kill_monster, kill_player
from entity import Skill_Entity,get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from render_functions import clear_all, render_all
from components.skill import Skill
from item_functions import become_graceful,become_accurate,poison_bite,acid_spit,throw_mudball


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    mouse = libtcod.Mouse()
    key = libtcod.Key()

    game_state = GameStates.RACE_SELECTION
    previous_game_state = game_state

    targeting_item = None

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        see_skills = action.get('see_skills')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        skills_index = action.get('skill_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        job = action.get('job')
        show_character_screen = action.get('show_character_screen')
        race = action.get('race')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        job_menu = action.get('job_menu')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        print(game_state)

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if player.fighter.status_effects.grace == True:
                player.fighter.nutrition -= 50
            else:
                player.fighter.nutrition -= 1

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        elif wait:
            game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if job_menu:
            game_state = GameStates.JOB_MENU

        if see_skills:
            previous_game_state = game_state
            game_state = GameStates.SKILL_SELECTION

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if skills_index is not None and previous_game_state != GameStates.PLAYER_DEAD and skills_index < len(
                player.skills.skills):
            item = player.skills.skills[skills_index]

            if game_state == GameStates.SKILL_SELECTION:
                player_turn_results.extend(player.skills.use(item, entities=entities, fov_map=fov_map))

        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
                elif entity.upstairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.previous_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1
            game_state = GameStates.CLASS_SELECTION

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if job:
            if job == 'cleric':
                player.fighter.job.cleric_level += 1
            elif job == 'fighter':
                player.fighter.job.fighter_level += 1
            elif job == 'thief':
                player.fighter.job.thief_level += 1
            elif job == 'wizard':
                player.fighter.job.wizard_level += 1

            game_state = previous_game_state
        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                if targeting_item.skill:
                    item_use_results = player.skills.use(targeting_item, entities=entities, fov_map=fov_map,
                                                            target_x=target_x, target_y=target_y)
                else:
                    item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state == GameStates.JOB_MENU:
                game_state = GameStates.CHARACTER_SCREEN
            elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN,GameStates.SKILL_SELECTION):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state)

                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            skill_targeting = player_turn_result.get('skill_targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))

                    if dequipped:
                        message_log.add_message(Message('You dequipped the {0}'.format(dequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if skill_targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = skill_targeting

                message_log.add_message(targeting_item.skill.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('You gain {0} experience points.'.format(xp)))

                if leveled_up:

                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        if race:
            if race == 'mern':
                player.fighter.race = 'Human'
                player.fighter.levels_quickly = True
            elif race == 'elf':
                player.fighter.race = 'Elf'
                player.fighter.base_defense += 2
                player.fighter.base_constitution -= 2
            elif race == 'dwarf':
                player.fighter.race = 'Dwarf'
                player.fighter.base_defense -= 2
                player.fighter.base_constitution += 2
            elif race == 'halfling':
                player.fighter.race = 'Halfling'
                player.fighter.base_defense += 4
                player.fighter.base_power -= 3
                player.fighter.base_constitution -= 1
            elif race == 'gnome':
                player.fighter.race = 'Gnome'
                player.fighter.base_constitution += 2
                player.fighter.base_willpower += 2
                player.fighter.base_power -= 4
            elif race == 'draconian':
                player.fighter.race = 'Draconian'
                player.fighter.large = True
                player.fighter.base_constitution += 3
                player.fighter.base_defense -= 4
                player.fighter.base_power += 3
            elif race == 'orc':
                player.fighter.race = 'Orc'
                player.fighter.base_constitution += 1
                player.fighter.base_defense -= 3
                player.fighter.base_power += 2
            elif race == 'goblin':
                player.fighter.race = 'Goblin'
                player.fighter.base_constitution += 1
                player.fighter.base_defense -= 3
                player.fighter.base_power += 2
            elif race == 'fairy':
                player.fighter.race = 'Fairy'
                player.fighter.base_constitution -= 6
                player.fighter.base_defense += 6
                player.fighter.base_power -= 6
                skill_component = Skill(use_function=become_accurate)
                skill = Skill_Entity('Faerie Dance',skill=skill_component)
                player.skills.add_skill(skill)
            elif race == 'turtle':
                player.fighter.race = 'Giant Turtle'
                player.fighter.base_constitution += 8
                player.fighter.base_defense -= 12
                player.fighter.base_power += 3
                player.fighter.large = True
                player.fighter.cant_wear_armour = True
            elif race == 'lizard':
                player.fighter.race = 'Lizardperson'
                skill_component = Skill(use_function=acid_spit, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the spit, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25)
                skill = Skill_Entity('Acid Spit',skill=skill_component)
                player.skills.add_skill(skill)
                player.fighter.base_defense -= 2
                player.fighter.base_power += 3
            elif race == 'frog':
                player.fighter.race = 'Frogperson'
                player.fighter.base_defense += 3
                player.fighter.base_power -= 2
                skill_component = Skill(use_function=become_graceful)
                skill = Skill_Entity('Slimy Skin', skill=skill_component)
                player.skills.add_skill(skill)
            elif race == 'giant':
                player.fighter.race = 'Giant'
                player.fighter.base_defense -= 7
                player.fighter.base_power += 5
                player.fighter.base_constitution += 5
                player.fighter.large = True
            elif race == 'troll':
                player.fighter.race = 'Troll'
                player.fighter.base_defense -= 7
                player.fighter.base_power += 4
                player.fighter.base_constitution += 2
                player.fighter.large = True
                player.fighter.carnivore = True
                player.fighter.sharp_claws = True
            elif race == 'skeleton':
                player.fighter.race = 'Skeleton'
                player.fighter.base_power += 1
                player.fighter.base_constitution += 1
                player.fighter.base_defense -= 4
            elif race == 'biter':
                player.fighter.race = 'Biter'
                player.fighter.base_constitution -= 2
                player.fighter.base_defense += 4
                player.player.fighter.sharp_claws = True
            elif race == 'kobold':
                player.fighter.race = 'Kobold'
                player.fighter.base_power -= 3
                player.fighter.base_defense += 3
                player.fighter.large = True
            elif race == 'chaosling':
                player.fighter.race = 'chaosling'
                player.fighter.base_power += 2
                player.fighter.base_defense += 2
                player.fighter.base_constitution += 2
                player.fighter.base_willpower -= 6
                player.fighter.hates_law = True
            elif race == 'reaper':
                player.fighter.race = 'Reaper'
                player.fighter.base_power += 4
                player.fighter.base_constitution += 2
                player.fighter.base_willpower -= 10
                player.fighter.bloodthirsty = True
            elif race == 'nymph':
                player.fighter.race = 'Nymph'
                player.fighter.base_power -= 5
                player.fighter.base_defense += 5
            elif race == 'octopode':
                player.fighter.race = 'Octopode'
                player.fighter.base_defense += 3
                player.fighter.eight_arms = True
                player.fighter.cant_wear_armour = True
            elif race == 'cat':
                player.fighter.race = 'Housecat'
                player.fighter.base_defense += 6
                player.fighter.base_constitution -= 3
            elif race == 'merfolk':
                player.fighter.race = 'Merfolk'
                player.fighter.swimmer = True
                player.fighter.base_defense += 3
                player.fighter.base_constitution += 3
                player.fighter.base_power -= 4
            elif race == 'mud':
                player.fighter.race = 'Mud Man'
                skill_component = Skill(use_function=throw_mudball, targeting=True, targeting_message=Message(
                    'Left-click a target tile for the ball, or right-click to cancel.', libtcod.light_cyan),
                                        damage=25)
                skill = Skill_Entity('Throw Mudball', skill=skill_component)
                player.skills.add_skill(skill)
                player.fighter.base_defense += 3
                player.fighter.base_constitution -= 3
            elif race == 'dryad':
                player.fighter.race = 'Dryad'
                player.fighter.one_with_nature = True
                player.fighter.base_power += 4
                player.fighter.base_defence -= 4
            elif race == 'naga':
                player.fighter.race = 'Naga'
                skill_component = Skill(use_function=poison_bite, targeting=True, targeting_message=Message(
                    'Left-click a target tile for the bite, or right-click to cancel.', libtcod.light_cyan),
                                        damage=25)
                skill = Skill_Entity('Naga Bite', skill=skill_component)
                player.skills.add_skill(skill)
                player.fighter.base_defense += 4
                player.fighter.base_power -= 4
                player.fighter.no_legs = True
            elif race == 'golem':
                player.fighter.race = 'Rogue Golem'
                player.fighter.golem = True
                player.fighter.base_defense += 10
                player.fighter.base_power += 10
                player.fighter.base_willpower += 13
            elif race == 'tengu':
                player.fighter.race = 'Tengu'
                player.fighter.base_defense += 4
                player.fighter.base_power -= 2
                player.fighter.base_constitution -= 3
            libtcod.console_flush()
            game_state = GameStates.PLAYERS_TURN

        if game_state == GameStates.ENEMY_TURN:
            if player.fighter.nutrition < 1:
                game_state = GameStates.PLAYER_DEAD
                kill_player(player)

            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


def main():
    constants = get_constants()

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = libtcod.image_load('menu_background.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'],
                      constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, constants)

            show_main_menu = True


if __name__ == '__main__':
    main()
