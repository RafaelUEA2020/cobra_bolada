import pygame
from assets import config

class HUD:
    def __init__(self):
        """Inicializa o sistema de fontes para o HUD."""
        # pygame.font.init() garante que o módulo de texto esteja ativo
        pygame.font.init()
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE)

    def draw_score(self, surface, snake_length):
        """Calcula e renderiza a pontuação com base no tamanho da cobra."""
        # Tamanho inicial da cobra é 3, então cada maçã comida vale 1 ponto
        score = snake_length - 3
        
        # Renderiza o texto (Texto, Antialiasing, Cor)
        score_surface = self.font.render(f"Score: {score}", True, config.COLOR_SCORE)
        
        # Desenha o texto na tela (posição 10 pixels de margem do topo e da esquerda)
        surface.blit(score_surface, (10, 10))