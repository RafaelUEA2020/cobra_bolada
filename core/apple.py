import pygame
import random
from assets import config

class Apple:
    def __init__(self, snake_body):
        """Inicializa a maçã em uma posição aleatória válida."""
        self.block_size = config.BLOCK_SIZE
        self.position = [0, 0]
        self.randomize_position(snake_body)

    def randomize_position(self, snake_body):
        """
        Gera uma nova coordenada (X, Y) aleatória para a maçã, 
        garantindo que ela esteja alinhada ao grid e fora do corpo da cobra.
        """
        # Calcula quantos blocos cabem na largura e altura da tela
        max_blocks_x = config.SCREEN_WIDTH // self.block_size
        max_blocks_y = config.SCREEN_HEIGHT // self.block_size

        while True:
            # Sorteia um bloco aleatório e multiplica pelo tamanho dele para achar o pixel exato
            random_x = random.randint(0, max_blocks_x - 1) * self.block_size
            random_y = random.randint(0, max_blocks_y - 1) * self.block_size
            new_position = [random_x, random_y]

            # Se a posição sorteada não colidir com nenhuma parte da cobra, aceita a posição
            if new_position not in snake_body:
                self.position = new_position
                break

    def draw(self, surface):
        """Desenha a maçã na tela."""
        rect = pygame.Rect(self.position[0], self.position[1], self.block_size, self.block_size)
        pygame.draw.rect(surface, config.COLOR_APPLE, rect)