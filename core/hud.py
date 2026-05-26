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

    # High Score

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

    # HUD em jogo

    def draw_score(self, surface, snake1, snake2=None):
        score1 = len(snake1.body) - 3
        if snake2:
            score2 = len(snake2.body) - 3
            best   = max(score1, score2)
        else:
            score2 = None
            best   = score1

        if best > self.high_score:
            self.high_score = best

        surf1 = self.font.render(f"P1: {score1}", True, config.COLOR_SNAKE_1)
        surf_hs = self.font_small.render(f"Record: {self.high_score}", True, (160, 160, 160))

        if snake2:
            # Multiplayer: P1 esquerda, P2 direita, recorde centralizado
            surf2 = self.font.render(f"P2: {score2}", True, config.COLOR_SNAKE_2)
            surface.blit(surf1, (10, 10))
            surface.blit(surf2, (config.SCREEN_WIDTH - surf2.get_width() - 10, 10))
            hs_x = (config.SCREEN_WIDTH - surf_hs.get_width()) // 2
            surface.blit(surf_hs, (hs_x, 14))
        else:
            # Single: só Score e Record
            surf_score = self.font.render(f"Score: {score1}", True, config.COLOR_SCORE)
            surface.blit(surf_score, (10, 10))
            surface.blit(surf_hs, (config.SCREEN_WIDTH - surf_hs.get_width() - 10, 14))

    # Menu — seleção de modo

    def draw_menu(self, surface):
        cx = config.SCREEN_WIDTH  // 2
        cy = config.SCREEN_HEIGHT // 2

        title = self.font_big.render(config.GAME_TITLE.upper(), True, config.COLOR_SNAKE_1)
        surface.blit(title, (cx - title.get_width() // 2, 80))

        # Caixas de seleção
        self._draw_mode_box(
            surface,
            x=cx - 220, y=180, w=180, h=160,
            key_label="[ 1 ]",
            title="SINGLE",
            subtitle="PLAYER",
            lines=["Setas: mover", "P: pausar", "ESC: menu"],
            color=config.COLOR_SNAKE_1,
        )
        self._draw_mode_box(
            surface,
            x=cx + 40, y=180, w=180, h=160,
            key_label="[ 2 ]",
            title="MULTI",
            subtitle="PLAYER",
            lines=["P1: Setas", "P2: W A S D", "P: pausar"],
            color=config.COLOR_SNAKE_2,
        )

        hint = self.font_small.render("Pressione 1 ou 2 para começar", True, (120, 120, 120))
        surface.blit(hint, (cx - hint.get_width() // 2, 380))

        hs = self.font_small.render(f"Record: {self.high_score}", True, (100, 100, 100))
        surface.blit(hs, (cx - hs.get_width() // 2, 420))

    def _draw_mode_box(self, surface, x, y, w, h, key_label, title, subtitle, lines, color):
        """Desenha uma caixa de modo com borda colorida."""
        # Fundo semi-transparente
        box = pygame.Surface((w, h))
        box.set_alpha(40)
        box.fill(color)
        surface.blit(box, (x, y))

        # Borda
        pygame.draw.rect(surface, color, (x, y, w, h), 2)

        # Tecla
        surf_key = self.font_small.render(key_label, True, color)
        surface.blit(surf_key, (x + w//2 - surf_key.get_width()//2, y + 8))

        # Título
        surf_t = self.font.render(title, True, (255, 255, 255))
        surf_s = self.font_small.render(subtitle, True, (200, 200, 200))
        surface.blit(surf_t, (x + w//2 - surf_t.get_width()//2, y + 32))
        surface.blit(surf_s, (x + w//2 - surf_s.get_width()//2, y + 60))

        # Linhas de controle
        ly = y + 85
        for line in lines:
            surf_l = self.font_small.render(line, True, (160, 160, 160))
            surface.blit(surf_l, (x + w//2 - surf_l.get_width()//2, ly))
            ly += 22

    # Tela de Vencedor / Game Over

    def draw_winner(self, surface, winner: int, multiplayer: bool):
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((10, 10, 10))
        surface.blit(overlay, (0, 0))

        if not multiplayer:
            msg   = "GAME OVER"
            color = (220, 220, 220)
        elif winner == 0:
            msg   = "EMPATE!"
            color = (200, 200, 200)
        elif winner == 1:
            msg   = "JOGADOR 1 VENCEU!"
            color = config.COLOR_SNAKE_1
        else:
            msg   = "JOGADOR 2 VENCEU!"
            color = config.COLOR_SNAKE_2

        surf_msg  = self.font_big.render(msg, True, color)
        surf_hint = self.font.render("SPACE — novo jogo  |  ESC — menu", True, (180, 180, 180))

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