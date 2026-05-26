import pygame
from assets import config  # Importa referenciando a raiz do projeto

class GameScreen:
    def __init__(self):
        self.width = config.SCREEN_WIDTH
        self.height = config.SCREEN_HEIGHT
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(config.GAME_TITLE)

    def render_background(self):
        self.surface.fill(config.COLOR_BACKGROUND)

    def update(self):
        pygame.display.flip()