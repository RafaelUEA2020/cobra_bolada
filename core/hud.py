import pygame
import os
from assets import config

class HUD:
    def __init__(self):
        """Inicializa o sistema de fontes e carrega o High Score salvo."""
        pygame.font.init()
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE)
        
        # Caminho para o arquivo onde o recorde será salvo
        self.high_score_file = "high_score.txt"
        self.high_score = self.load_high_score()

    def load_high_score(self):
        """Lê o maior placar gravado no arquivo. Retorna 0 se o arquivo não existir."""
        if os.path.exists(self.high_score_file):
            try:
                with open(self.high_score_file, "r") as file:
                    return int(file.read().strip())
            except ValueError:
                return 0 # Se o arquivo estiver corrompido ou vazio, assume 0
        return 0

    def save_high_score(self, new_high_score):
        """Grava o novo recorde no arquivo de texto se ele for maior que o atual."""
        if new_high_score > self.high_score:
            self.high_score = new_high_score
            with open(self.high_score_file, "w") as file:
                file.write(str(self.high_score))

    def draw_score(self, surface, snake_length):
        """Calcula, renderiza e atualiza os placares (Atual e Recorde)."""
        current_score = snake_length - 3
        
        # Se a pontuação atual passar o recorde em tempo real, atualiza visualmente
        if current_score > self.high_score:
            self.high_score = current_score

        # Renderiza os textos
        score_surface = self.font.render(f"Score: {current_score}", True, config.COLOR_SCORE)
        high_score_surface = self.font.render(f"High Score: {self.high_score}", True, config.COLOR_SCORE)
        
        # Desenha na tela (Score na esquerda, High Score na direita com margem)
        surface.blit(score_surface, (10, 10))
        
        # Calcula a posição X do High Score para não sumir da tela
        high_score_x = config.SCREEN_WIDTH - high_score_surface.get_width() - 10
        surface.blit(high_score_surface, (high_score_x, 10))
        
    def draw_paused(self, surface):
        """Desenha uma mensagem de pausa centralizada na tela."""
        paused_surface = self.font.render("PAUSED", True, config.COLOR_SCORE)
        
        # Calcula o centro exato da tela para posicionar o texto
        text_x = (config.SCREEN_WIDTH - paused_surface.get_width()) // 2
        text_y = (config.SCREEN_HEIGHT - paused_surface.get_height()) // 2
        
        surface.blit(paused_surface, (text_x, text_y))