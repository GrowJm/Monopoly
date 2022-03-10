import pygame_menu


class Menu:
    __isInitialized = False
    main_menu = None

    @staticmethod
    def initialize():
        if not Menu.__isInitialized:
            Menu.__isInitialized = True

            menu_theme = pygame_menu.themes.THEME_DARK.copy()
            menu_theme.set_background_color_opacity(0.5)

            Menu.main_menu = pygame_menu.Menu("Welcome to Monopoly", 400, 300,
                                              theme=menu_theme)
            Menu.main_menu.add.text_input('Name: ', default='Player', maxchar=12)
            Menu.main_menu.add.button('Play', Menu.start_the_game)

            settings_submenu = pygame_menu.Menu('Settings', 400, 250)
            Menu.main_menu.add.button('Settings', settings_submenu)
            # TODO: add volume sliders
            # https://pygame-menu.readthedocs.io/en/4.2.5/

    @staticmethod
    def start_the_game():
        pass

