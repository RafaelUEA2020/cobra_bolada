# core/game.py

import pygame
import sys

from assets import config
from core.screen import GameScreen
from core.snake  import Snake
from core.apple  import Apple
from core.hud    import HUD
from client.controls import handle_keydown


def _occupied(snake1: Snake, snake2=None) -> list:
    if snake2:
        return snake1.body + snake2.body
    return snake1.body


def _new_round(multiplayer: bool):
    s1 = Snake(1)
    if multiplayer:
        s2 = Snake(2)
        apple = Apple(_occupied(s1, s2))
        return s1, s2, apple
    else:
        apple = Apple(_occupied(s1))
        return s1, None, apple


def run_game():
    pygame.init()
    screen = GameScreen()
    clock = pygame.time.Clock()
    hud    = HUD()

    # ── Estados ───────────────────────────────────────────────────
    in_menu           = True
    is_paused         = False
    is_confirming_exit = False
    winner            = None   # None=jogando | 0=empate | 1 | 2
    multiplayer       = False  # definido na seleção do menu

    snake1, snake2, apple = _new_round(multiplayer)

    SNAKE_MOVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SNAKE_MOVE_EVENT, 1000 // config.INITIAL_SPEED)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                # MENU 
                if in_menu:
                    if event.key == pygame.K_1:
                        multiplayer = False
                        snake1, snake2, apple = _new_round(multiplayer)
                        winner = None; is_paused = False; in_menu = False
                    elif event.key == pygame.K_2:
                        multiplayer = True
                        snake1, snake2, apple = _new_round(multiplayer)
                        winner = None; is_paused = False; in_menu = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # TELA DE VENCEDOR / FIM DE JOGO 
                elif winner is not None:
                    if event.key == pygame.K_SPACE:
                        snake1, snake2, apple = _new_round(multiplayer)
                        winner = None; is_paused = False
                    elif event.key == pygame.K_ESCAPE:
                        in_menu = True; winner = None

                # CONFIRMANDO SAÍDA
                elif is_confirming_exit:
                    if event.key == pygame.K_y:
                        is_confirming_exit = False
                        is_paused = False
                        in_menu = True
                        winner = None
                        snake1, snake2, apple = _new_round(multiplayer)
                    elif event.key in (pygame.K_n, pygame.K_ESCAPE):
                        is_confirming_exit = False

                # JOGO EM ANDAMENTO
                else:
                    if event.key == pygame.K_ESCAPE:
                        is_confirming_exit = True
                    else:
                        is_paused = handle_keydown(
                            event.key, snake1, snake2, is_paused, multiplayer
                        )

            # MOVIMENTO
            elif (
                event.type == SNAKE_MOVE_EVENT
                and not in_menu
                and not is_paused
                and not is_confirming_exit
                and winner is None
            ):
                next1 = snake1.get_next_head()

                # SINGLE PLAYER 
                if not multiplayer:
                    if next1 == apple.position:
                        snake1.grow(next1)
                        apple.randomize_position(_occupied(snake1))
                    else:
                        snake1.move()

                    head = snake1.body[0]
                    dead = (
                        snake1.check_wall_collision() or
                        snake1.check_self_collision()
                    )
                    if dead:
                        hud.save_high_score(len(snake1.body) - 3)
                        winner = 1  # "fim de jogo" — reusa tela de winner com msg especial

                # ── MULTIPLAYER ───────────────────────────────────────
                else:
                    next2 = snake2.get_next_head()

                    # Resolve quem come a maçã (prioridade: quem chegar primeiro;
                    # se os dois chegarem no mesmo frame, cobra1 tem prioridade)
                    ate1 = (next1 == apple.position)
                    ate2 = (next2 == apple.position)

                    if ate1:
                        snake1.grow(next1)
                        apple.randomize_position(_occupied(snake1, snake2))
                        # Recalcula next2 para evitar que cobra2 "coma" a posição antiga
                        ate2 = False
                    else:
                        snake1.move()

                    if ate2:
                        snake2.grow(next2)
                        apple.randomize_position(_occupied(snake1, snake2))
                    else:
                        snake2.move()

                    dead1 = (
                        snake1.check_wall_collision() or
                        snake1.check_self_collision() or
                        snake1.check_collision_with(snake2)
                    )
                    dead2 = (
                        snake2.check_wall_collision() or
                        snake2.check_self_collision() or
                        snake2.check_collision_with(snake1)
                    )

                    if dead1 or dead2:
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
            snake1.draw(screen.surface)
            if multiplayer and snake2:
                snake2.draw(screen.surface)
            apple.draw(screen.surface)
            hud.draw_score(screen.surface, snake1, snake2 if multiplayer else None)

            if winner is not None:
                hud.draw_winner(screen.surface, winner, multiplayer)
            elif is_paused:
                hud.draw_paused(screen.surface)
            elif is_confirming_exit:
                hud.draw_exit_confirmation(screen.surface)

        screen.update()
        clock.tick(config.FPS)