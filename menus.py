import libtcodpy as libtcod


def menu(con, header, options, width, screen_width, screen_height):
    global key, mouse
    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def skill_menu(con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.skills.skills) == 0:
        options = ['You have no skills.']
    else:
        options = []

        for skill in player.skills.skills:
            options.append(skill.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)

def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'ChaosRL')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             'By Fatbunny')

    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.power),
               'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height)

def race_select_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['(a)Human (Levels fast)'.format(player.fighter.max_hp),
               '(b)Elf (+2 agility, -2 constitution)'.format(player.fighter.power),
               '(c)Dwarf (+2 constitution, -2 agility)'.format(player.fighter.defense),
               '(d)Halfling (+4 agility, -3 strength, -1 constitution)'.format(player.fighter.defense),
               '(e)Gnome (+2 constitution, +2 willpower, -4 strength)'.format(player.fighter.defense),
               '(f)Draconian (+3 strength, +3 constitution, -4 agility, too big for armour, Gets a breath weapon at level 7)'.format(player.fighter.defense),
               '(g)Orc (+2 strength, +1 constitution -3 agility)'.format(player.fighter.defense),
               '(h)Goblin (+2 agility, +1 willpower, -3 strength)'.format(player.fighter.defense),
               '(i)Fairy (+6 agility, -6 strength, -6 constitution, Can use a dance that gives them multiple attacks,too small for armour)'.format(player.fighter.defense),
               '(j)Giant Turtle (+8 constitution, +3 strength, -12 agility, too big for most armour.)'.format(player.fighter.defense),
               '(k)Lizardperson (+3 strength, -2 agility, Can spit acid)'.format(player.fighter.defense),
               '(l)Frogperson (+3 agility, -2 strength, Can cover themselves in slime that makes them able to dodge attacks more easily)'.format(player.fighter.defense),
               '(m)Giant (+5 strength, +5 constitution, -7 agility, too big for most armours.)'.format(player.fighter.defense),
               '(n)Troll (+4 strength, +2 constitution, -7 agility, too big for most armours, Carnivores, Sharp claws.)'.format(player.fighter.defense),
               '(o)Skeleton (+1 strength, +1 constitution, Can create a shield of bones to protect themselves)'.format(player.fighter.defense),
               '(p)Biter (+4 agility, -2 constitution, They are extra skilled at wrestiling, But they lack arms '.format(player.fighter.defense),
               '(q)Kobold (+3 agility, -3 strength, carnivorous, and very small)'.format(player.fighter.defense),
               '(r)Chaosling (+2 strength, +2 constitution, +2 strength, -6 willpower, The very idea of lawfulness hurts them.)'.format(player.fighter.defense),
               '(s)Reaper (+4 strength, +2 constitution, -10 willpower, has to kill enemies or they will die)'.format(player.fighter.defense),
               '(t)Nymph (+5 agility, -5 strength, can steal items effortlessly)'.format(player.fighter.defense),
               '(u)Octopode (+3 agility, Can\'t wear armour but can wear 8 rings and braclets on its 8 tentacles)'.format(player.fighter.defense),
               '(v)Housecat (+6 agility, -3 constitution, Can\'t wear armour.)'.format(player.fighter.defense),
               '(w)Merfolk (+3 agility, +3 constitution, -4 strength, Can swim in water. from {0})'.format(player.fighter.defense),
               '(x)Mud Man (+3 agility, -3 constitution, Can sacrifice parts of them to use as weapons)'.format(player.fighter.defense),
               '(y)Dryad (+4 strength, -4 agility, They are flammable and fear fire. But are very strong with nature magic.)'.format(player.fighter.defense),
               '(z)Naga (+4 agility, -4 strength, They cant wear leg armour but they have a poisonous bite.)'.format(player.fighter.defense),
               '(A)Rogue Golem (+10 agility, +10 strength, +13 constitution, As artifical beings they cannot gain class levels.)'.format(player.fighter.defense),
               '(B)Tengu (+4 defense, -2 strength, -3 constitution, They can fly to avoid attacks and go over obstacles.)'.format(player.fighter.defense),]

    menu(con, header, options, menu_width, screen_width, screen_height)

def job_selection_menu(con, header, player, menu_width, screen_width, screen_height):

    options = ['Priest'.format(player.fighter.max_hp),
               'Fighter '.format(player.fighter.max_hp),
               'Thief'.format(player.fighter.max_hp),
               'Magician'.format(player.fighter.max_hp),]

    menu(con, header, options, menu_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))
    libtcod.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'AC: {0}'.format(player.fighter.ac))
    libtcod.console_print_rect_ex(window, 0, 10, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Will: {0}'.format(player.fighter.will))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
