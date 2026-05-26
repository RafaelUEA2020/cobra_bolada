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

    def draw_menu(self, surface):
        """Desenha a tela de menu inicial com o título e instruções."""
        main_font = pygame.font.SysFont(config.FONT_NAME, 40)
        
        title_surf = main_font.render(config.GAME_TITLE.upper(), True, config.COLOR_SNAKE)
        start_surf = self.font.render("Press SPACE to Start", True, (255, 255, 255))
        
        # Instruções de controles atualizadas
        move_surf = self.font.render("Arrow Keys: Move Snake", True, (180, 180, 180))
        pause_surf = self.font.render("P Key: Pause / Unpause Game", True, (180, 180, 180))
        exit_surf = self.font.render("ESC Key: Quit Game (from Menu)", True, (180, 180, 180)) # Nova linha
        
        center_x = config.SCREEN_WIDTH // 2
        
        surface.blit(title_surf, (center_x - title_surf.get_width() // 2, 120))
        surface.blit(start_surf, (center_x - start_surf.get_width() // 2, 220))
        surface.blit(move_surf, (center_x - move_surf.get_width() // 2, 350))
        surface.blit(pause_surf, (center_x - pause_surf.get_width() // 2, 390))
        surface.blit(exit_surf, (center_x - exit_surf.get_width() // 2, 430)) # Desenha a nova linha
        
    def draw_exit_confirmation(self, surface):
        """Desenha uma tela de confirmação perguntando se o usuário quer voltar ao menu."""
        # Cria uma superfície semi-transparente para escurecer o fundo do jogo
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(150) # Nível de transparência (0 a 255)
        overlay.fill((10, 10, 10))
        surface.blit(overlay, (0, 0))

        # Renderiza os textos da mensagem
        msg_surf1 = self.font.render("Return to Main Menu?", True, config.COLOR_SCORE)
        msg_surf2 = self.font.render("Press Y (Yes) or N (No)", True, config.COLOR_APPLE)
        
        center_x = config.SCREEN_WIDTH // 2
        center_y = config.SCREEN_HEIGHT // 2
        
        # Desenha centralizado
        surface.blit(msg_surf1, (center_x - msg_surf1.get_width() // 2, center_y - 30))
        surface.blit(msg_surf2, (center_x - msg_surf2.get_width() // 2, center_y + 10))