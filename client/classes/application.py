import sys
import pygame
from classes.menu import Menu


class Application:
    __isInitialized = False
    screen = None
    main_menu_background = None

    @staticmethod
    def __initialize():
        if not Application.__isInitialized:
            Application.__isInitialized = True

            pygame.init()

            Application.screen = pygame.display.set_mode((900, 600))
            pygame.display.set_caption("Monopoly")
            pygame.display.set_icon(pygame.image.load("assets/icon/caption-icon.png"))

            Application.main_menu_background = pygame.image.load("assets/background/main-bg.png")
            Menu.initialize()

    @staticmethod
    def run():
        Application.__initialize()

        while True:
            Menu.main_menu.mainloop(Application.screen, Application.menu_background)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()

    @staticmethod
    def menu_background():
        Application.screen.blit(Application.main_menu_background, (0, 0))

