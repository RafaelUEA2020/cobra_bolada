# core/apple.py

import pygame
import random
from assets import config


class Apple:
    def __init__(self, occupied: list):
        """
        occupied — lista de posições já usadas (corpo das duas cobras).
        """
        self.block_size = config.BLOCK_SIZE
        self.position   = [0, 0]
        self.randomize_position(occupied)

    def randomize_position(self, occupied: list):
        """Gera posição aleatória alinhada ao grid e fora de 'occupied'."""
        max_x = config.SCREEN_WIDTH  // self.block_size
        max_y = config.SCREEN_HEIGHT // self.block_size

        while True:
            pos = [
                random.randint(0, max_x - 1) * self.block_size,
                random.randint(0, max_y - 1) * self.block_size,
            ]
            if pos not in occupied:
                self.position = pos
                break

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0], self.position[1],
            self.block_size, self.block_size
        )
        pygame.draw.rect(surface, config.COLOR_APPLE, rect)
        # Brilho simples no canto superior esquerdo da maçã
        shine = pygame.Rect(
            self.position[0] + 3, self.position[1] + 3, 5, 5
        )
        pygame.draw.rect(surface, (255, 160, 150), shine)