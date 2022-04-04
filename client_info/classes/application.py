import pygame
import sys
from client_info.classes.images import *
import pygame_menu
pygame.init()
pygame.font.init()

class Application():
    @staticmethod
    def application():
        while True:
            SCREEN = pygame.display.set_mode((1920,1000))
            SCREEN.blit(BG_menu,(0,0))
            pygame.display.set_caption("Menu")
            scale_play_button = pygame.transform.scale(play_button, (250, 150))
            SCREEN.blit(scale_play_button,[0,100])
            pygame.display.flip()





            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

