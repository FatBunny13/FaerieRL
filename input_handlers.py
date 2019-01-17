import libtcodpy as libtcod

from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state in (GameStates.CHARACTER_SCREEN,GameStates.JOB_MENU):
        return handle_character_screen(key)
    elif game_state == GameStates.RACE_SELECTION:
        return handle_race_selection(key)
    elif game_state == GameStates.CLASS_SELECTION:
        return handle_class_selection(key)
    elif game_state == GameStates.SKILL_SELECTION:
        return handle_skill_keys(key)

    return {}


def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # Movement keys
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}
    elif key_char == 'z':
        return {'wait': True}

    elif key_char == 'g':
        return {'pickup': True}

    elif key_char == 's':
        return {'see_skills': True}

    elif key_char == 'i':
        return {'show_inventory': True}

    elif key_char == 'd':
        return {'drop_inventory': True}

    elif key.vk == libtcod.KEY_ENTER:
        return {'take_stairs': True}

    elif key_char == 'c':
        return {'show_character_screen': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}


def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}


def handle_inventory_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}

def handle_skill_keys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'skill_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}



def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_class_selection(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'job': 'fighter'}
        elif key_char == 'b':
            return {'job': 'wizard'}
        elif key_char == 'c':
            return {'job': 'thief'}
        elif key_char == 'd':
            return {'job': 'cleric'}

    return {}
def handle_race_selection(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'race': 'mern'}
        elif key_char == 'b':
            return {'race': 'elf'}
        elif key_char == 'c':
            return {'race': 'dwarf'}
        elif key_char == 'd':
            return {'race': 'halfling'}
        elif key_char == 'e':
            return {'race': 'gnome'}
        elif key_char == 'f':
            return {'race': 'draconian'}
        elif key_char == 'g':
            return {'race': 'orc'}
        elif key_char == 'h':
            return {'race': 'goblin'}
        elif key_char == 'i':
            return {'race': 'fairy'}
        elif key_char == 'j':
            return {'race': 'turtle'}
        elif key_char == 'k':
            return {'race': 'lizard'}
        elif key_char == 'l':
            return {'race': 'frog'}
        elif key_char == 'm':
            return {'race': 'giant'}
        elif key_char == 'n':
            return {'race': 'troll'}
        elif key_char == 'o':
            return {'race': 'skeleton'}
        elif key_char == 'p':
            return {'race': 'biter'}
        elif key_char == 'q':
            return {'race': 'kobold'}
        elif key_char == 'r':
            return {'race': 'chaosling'}
        elif key_char == 's':
            return {'race': 'reaper'}
        elif key_char == 't':
            return {'race': 'nymph'}
        elif key_char == 'u':
            return {'race': 'octopode'}
        elif key_char == 'v':
            return {'race': 'cat'}
        elif key_char == 'w':
            return {'race': 'merfolk'}
        elif key_char == 'x':
            return {'race': 'mud'}
        elif key_char == 'y':
            return {'race': 'dryad'}
        elif key_char == 'z':
            return {'race': 'naga'}
        elif key_char == 'a' and key.vk == key.SHIFT:
            return {'race': 'golem'}
        elif key_char == 'b' and key.vk == key.SHIFT:
            return {'race': 'tengu'}

    return {}


def handle_level_up_menu(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}

    return {}


def handle_character_screen(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'job_menu': True}
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
