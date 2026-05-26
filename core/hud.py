# core/hud.py

import pygame
import os
from assets import config

class HUD:
    def __init__(self):
        pygame.font.init()
        self.font       = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE)
        self.font_big   = pygame.font.SysFont(config.FONT_NAME, 42)
        self.font_small = pygame.font.SysFont(config.FONT_NAME, 20)

        self.high_score_file = "high_score.txt"
        self.high_score      = self.load_high_score()

    # High Score baseado no jogador com maior pontuação

    def load_high_score(self) -> int:
        if os.path.exists(self.high_score_file):
            try:
                with open(self.high_score_file, "r") as f:
                    return int(f.read().strip())
            except ValueError:
                return 0
        return 0

    def save_high_score(self, score: int):
        if score > self.high_score:
            self.high_score = score
            with open(self.high_score_file, "w") as f:
                f.write(str(score))

    # HUD em jogo — placar dos dois jogadores

    def draw_score(self, surface, snake1, snake2):
        """
        Jogador 1 (verde) — canto superior esquerdo.
        Jogador 2 (azul)  — canto superior direito.
        """
        score1 = len(snake1.body) - 3
        score2 = len(snake2.body) - 3

        # Atualiza high score em tempo real
        best = max(score1, score2)
        if best > self.high_score:
            self.high_score = best

        surf1 = self.font.render(f"P1: {score1}", True, config.COLOR_SNAKE_1)
        surf2 = self.font.render(f"P2: {score2}", True, config.COLOR_SNAKE_2)
        surf_hs = self.font_small.render(
            f"Record: {self.high_score}", True, (160, 160, 160)
        )

        surface.blit(surf1, (10, 10))
        surface.blit(surf2, (config.SCREEN_WIDTH - surf2.get_width() - 10, 10))

        # Recorde centralizado no topo
        hs_x = (config.SCREEN_WIDTH - surf_hs.get_width()) // 2
        surface.blit(surf_hs, (hs_x, 14))

    # Tela de Menu

    def draw_menu(self, surface):
        title_surf = self.font_big.render(
            config.GAME_TITLE.upper(), True, config.COLOR_SNAKE_1
        )
        lines = [
            (self.font,       "Press SPACE to Start",            (255, 255, 255)),
            (self.font,       "── Controles ──",                  (120, 120, 120)),
            (self.font_small, "P1: Setas  |  P2: W A S D",       (180, 180, 180)),
            (self.font_small, "P: Pausar  |  ESC: Menu",         (180, 180, 180)),
        ]

        cx = config.SCREEN_WIDTH // 2
        surface.blit(title_surf, (cx - title_surf.get_width() // 2, 110))

        y = 220
        for font, text, color in lines:
            surf = font.render(text, True, color)
            surface.blit(surf, (cx - surf.get_width() // 2, y))
            y += 40

    # ------------------------------------------------------------------
    # Tela de Vencedor
    # ------------------------------------------------------------------

    def draw_winner(self, surface, winner: int):
        """
        Exibe quem ganhou e aguarda SPACE para voltar ao menu.
        winner = 0  →  empate (ambas colidiram ao mesmo tempo)
        winner = 1  →  Jogador 1 venceu
        winner = 2  →  Jogador 2 venceu
        """
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((10, 10, 10))
        surface.blit(overlay, (0, 0))

        if winner == 0:
            msg   = "EMPATE!"
            color = (200, 200, 200)
        elif winner == 1:
            msg   = "JOGADOR 1 VENCEU!"
            color = config.COLOR_SNAKE_1
        else:
            msg   = "JOGADOR 2 VENCEU!"
            color = config.COLOR_SNAKE_2

        surf_msg  = self.font_big.render(msg, True, color)
        surf_hint = self.font.render("SPACE — novo jogo  |  ESC — menu", True, (200, 200, 200))

        cx = config.SCREEN_WIDTH  // 2
        cy = config.SCREEN_HEIGHT // 2

        surface.blit(surf_msg,  (cx - surf_msg.get_width()  // 2, cy - 40))
        surface.blit(surf_hint, (cx - surf_hint.get_width() // 2, cy + 20))

    # ------------------------------------------------------------------
    # Pausa
    # ------------------------------------------------------------------

    def draw_paused(self, surface):
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((10, 10, 10))
        surface.blit(overlay, (0, 0))

        surf = self.font_big.render("PAUSADO", True, config.COLOR_SCORE)
        cx   = (config.SCREEN_WIDTH  - surf.get_width())  // 2
        cy   = (config.SCREEN_HEIGHT - surf.get_height()) // 2
        surface.blit(surf, (cx, cy))

    # ------------------------------------------------------------------
    # Confirmação de saída
    # ------------------------------------------------------------------

    def draw_exit_confirmation(self, surface):
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((10, 10, 10))
        surface.blit(overlay, (0, 0))

        surf1 = self.font.render("Voltar ao Menu Principal?", True, config.COLOR_SCORE)

        surf2 = self.font.render("Y — Sim   |   N / ESC — Não", True, config.COLOR_APPLE)

        cx = config.SCREEN_WIDTH  // 2
        cy = config.SCREEN_HEIGHT // 2

        surface.blit(surf1, (cx - surf1.get_width() // 2, cy - 30))
        surface.blit(surf2, (cx - surf2.get_width() // 2, cy + 15))