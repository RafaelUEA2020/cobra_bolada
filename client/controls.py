# client/controls.py
#
# Mapeia os eventos de teclado do pygame para direções de movimento.
# Cada jogador tem seu próprio conjunto de teclas definido em config.py.
# A função handle_keydown() é chamada pelo game.py a cada KEYDOWN.

import pygame
from assets import config


# Mapas de tecla → direção para cada jogador
KEYMAP_P1 = {
    pygame.K_UP:    "UP",
    pygame.K_DOWN:  "DOWN",
    pygame.K_LEFT:  "LEFT",
    pygame.K_RIGHT: "RIGHT",
}

KEYMAP_P2 = {
    pygame.K_w: "UP",
    pygame.K_s: "DOWN",
    pygame.K_a: "LEFT",
    pygame.K_d: "RIGHT",
}


def handle_keydown(event_key, snake1, snake2, is_paused):
    """
    Recebe uma tecla pressionada e aplica a direção na cobra correta.
    Retorna is_paused (pode ser alternado pela tecla P).
    Não move as cobras — apenas registra a intenção de direção.
    """
    # Pausa (qualquer jogador pode pausar)
    if event_key == pygame.K_p:
        return not is_paused

    # Só muda direção se o jogo não estiver pausado
    if not is_paused:
        if event_key in KEYMAP_P1:
            snake1.change_direction(KEYMAP_P1[event_key])
        elif event_key in KEYMAP_P2:
            snake2.change_direction(KEYMAP_P2[event_key])

    return is_paused