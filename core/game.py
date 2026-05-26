# core/game.py

import pygame
import sys

from assets import config
from core.screen import GameScreen
from core.snake  import Snake
from core.apple  import Apple
from core.hud    import HUD
from client.controls import handle_keydown


def _occupied(snake1: Snake, snake2: Snake) -> list:
    """Retorna todas as posições ocupadas pelas duas cobras."""
    return snake1.body + snake2.body


def _new_round():
    """Cria cobras e maçã para uma nova rodada."""
    s1 = Snake(1)
    s2 = Snake(2)
    apple = Apple(_occupied(s1, s2))
    return s1, s2, apple


def run_game():
    pygame.init()
    screen = GameScreen()
    clock = pygame.time.Clock()
    hud    = HUD()

    snake1, snake2, apple = _new_round()

    # ── Estados ───────────────────────────────────────────────────
    in_menu           = True
    is_paused         = False
    is_confirming_exit = False
    winner            = None   # None = jogo em curso | 0 = empate | 1 | 2

    SNAKE_MOVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SNAKE_MOVE_EVENT, 1000 // config.INITIAL_SPEED)

    while True:
        for event in pygame.event.get():

            # ── Fechar janela ────────────────────────────────────────
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                # ── MENU INICIAL ─────────────────────────────────────
                if in_menu:
                    if event.key == pygame.K_SPACE:
                        snake1, snake2, apple = _new_round()
                        winner    = None
                        is_paused = False
                        in_menu   = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # ── TELA DE VENCEDOR ─────────────────────────────────
                elif winner is not None:
                    if event.key == pygame.K_SPACE:          # novo jogo
                        snake1, snake2, apple = _new_round()
                        winner    = None
                        is_paused = False
                    elif event.key == pygame.K_ESCAPE:       # volta ao menu
                        in_menu = True
                        winner  = None

                # ── CONFIRMANDO SAÍDA ────────────────────────────────
                elif is_confirming_exit:
                    if event.key == pygame.K_y:
                        is_confirming_exit = False
                        is_paused          = False
                        in_menu            = True
                        winner             = None
                        snake1, snake2, apple = _new_round()
                    elif event.key in (pygame.K_n, pygame.K_ESCAPE):
                        is_confirming_exit = False

                # ── JOGO EM ANDAMENTO ────────────────────────────────
                else:
                    if event.key == pygame.K_ESCAPE:
                        is_confirming_exit = True
                    else:
                        is_paused = handle_keydown(
                            event.key, snake1, snake2, is_paused
                        )

            # ── MOVIMENTO DAS COBRAS ─────────────────────────────────
            elif (
                event.type == SNAKE_MOVE_EVENT
                and not in_menu
                and not is_paused
                and not is_confirming_exit
                and winner is None
            ):
                next1 = snake1.get_next_head()
                next2 = snake2.get_next_head()

                # --- Cobra 1 come a maçã? ---
                if next1 == apple.position:
                    snake1.grow(next1)
                    apple.randomize_position(_occupied(snake1, snake2))
                else:
                    snake1.move()

                # --- Cobra 2 come a maçã? ---
                if next2 == apple.position:
                    snake2.grow(next2)
                    apple.randomize_position(_occupied(snake1, snake2))
                else:
                    snake2.move()

                # --- Detecção de colisões ---
                dead1 = (
                    snake1.check_wall_collision()   or
                    snake1.check_self_collision()   or
                    snake1.check_collision_with(snake2)
                )
                dead2 = (
                    snake2.check_wall_collision()   or
                    snake2.check_self_collision()   or
                    snake2.check_collision_with(snake1)
                )

                if dead1 or dead2:
                    # Salva o maior placar da rodada
                    hud.save_high_score(
                        max(len(snake1.body) - 3, len(snake2.body) - 3)
                    )

                    if dead1 and dead2:
                        winner = 0     
                    elif dead1:
                        winner = 2      
                    else:
                        winner = 1     

        # ── Renderização ─────────────────────────────────────────────
        screen.render_background()
        
        if in_menu:
            hud.draw_menu(screen.surface)
        else:
            # Sempre desenha o estado atual do jogo como fundo
            snake1.draw(screen.surface)
            snake2.draw(screen.surface)
            apple.draw(screen.surface)
            hud.draw_score(screen.surface, snake1, snake2)
            if winner is not None:
                hud.draw_winner(screen.surface, winner)
            elif is_paused:
                hud.draw_paused(screen.surface)
            elif is_confirming_exit:
                hud.draw_exit_confirmation(screen.surface)
        screen.update()
        clock.tick(config.FPS)