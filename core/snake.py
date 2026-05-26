# core/snake.py

import pygame
from assets import config


class Snake:
    def __init__(self, player: int):
        """
        Inicializa a cobra para o jogador 1 ou 2.

        Jogador 1 — começa na metade esquerda, se movendo para a direita.
        Jogador 2 — começa na metade direita, se movendo para a esquerda.
        """
        self.block_size = config.BLOCK_SIZE
        self.player     = player

        # Cores do corpo e da cabeça (diferentes por jogador)
        bs = self.block_size

        if player == 1:
            self.color      = config.COLOR_SNAKE_1
            self.head_color = config.COLOR_SNAKE_1_HEAD
            cx = ((config.SCREEN_WIDTH // 4) // bs) * bs
            cy = ((config.SCREEN_HEIGHT // 2) // bs) * bs
            self.direction = [bs, 0]
        else:
            self.color      = config.COLOR_SNAKE_2
            self.head_color = config.COLOR_SNAKE_2_HEAD
            cx = (((config.SCREEN_WIDTH * 3) // 4) // bs) * bs
            cy = ((config.SCREEN_HEIGHT // 2) // bs) * bs
            self.direction = [-bs, 0]

        # Fila de direção: aceita no máximo 1 input por frame de movimento
        self._next_direction = self.direction[:]

        # Corpo inicial com 3 blocos
        if player == 1:
            self.body = [
                [cx,          cy],
                [cx - bs,     cy],
                [cx - 2 * bs, cy],
            ]
        else:
            self.body = [
                [cx,          cy],
                [cx + bs,     cy],
                [cx + 2 * bs, cy],
            ]

    # ------------------------------------------------------------------
    # Direção
    # ------------------------------------------------------------------

    def change_direction(self, new_direction: str):
        """
        Registra a intenção de mudança de direção.
        A direção só é aplicada no próximo frame de movimento,
        evitando morte por dois inputs rápidos antes de um step.
        """
        bs = self.block_size
        opposites = {
            "UP":    [0,   bs],
            "DOWN":  [0,  -bs],
            "LEFT":  [bs,   0],
            "RIGHT": [-bs,  0],
        }
        moves = {
            "UP":    [0,  -bs],
            "DOWN":  [0,   bs],
            "LEFT":  [-bs,  0],
            "RIGHT": [bs,   0],
        }
        # Bloqueia 180° contra a direção ATUAL (não a pendente)
        if new_direction in moves and self.direction != opposites[new_direction]:
            self._next_direction = moves[new_direction]

    # ------------------------------------------------------------------
    # Movimento
    # ------------------------------------------------------------------

    def apply_direction(self):
        """
        Aplica a direção pendente. Deve ser chamado UMA VEZ por step,
        antes de get_next_head(), move() ou grow().
        """
        self.direction = self._next_direction[:]

    def get_next_head(self) -> list:
        """Retorna a posição que a cabeça ocupará no próximo passo."""
        return [
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1],
        ]

    def move(self):
        """Avança a cobra um passo (sem crescer)."""
        self.body.insert(0, self.get_next_head())
        self.body.pop()

    def grow(self, new_head: list):
        """Avança a cobra e a faz crescer (comeu uma maçã)."""
        self.body.insert(0, new_head)

    # ------------------------------------------------------------------
    # Colisões
    # ------------------------------------------------------------------

    def check_wall_collision(self) -> bool:
        """Retorna True se a cabeça saiu dos limites da tela."""
        hx, hy = self.body[0]
        return (
            hx < 0 or hx >= config.SCREEN_WIDTH or
            hy < 0 or hy >= config.SCREEN_HEIGHT
        )

    def check_self_collision(self) -> bool:
        """Retorna True se a cabeça colidiu com o próprio corpo."""
        return self.body[0] in self.body[1:]

    def check_collision_with(self, other: "Snake") -> bool:
        """
        Retorna True se a cabeça desta cobra colidiu com
        qualquer parte do corpo da cobra adversária.
        """
        return self.body[0] in other.body

    # ------------------------------------------------------------------
    # Renderização
    # ------------------------------------------------------------------

    def draw(self, surface):
        """Desenha o corpo da cobra. A cabeça tem cor diferenciada."""
        for i, block in enumerate(self.body):
            color = self.head_color if i == 0 else self.color
            rect  = pygame.Rect(block[0], block[1], self.block_size, self.block_size)
            pygame.draw.rect(surface, color, rect)

            # Borda interna sutil para separar os blocos visualmente
            pygame.draw.rect(surface, config.COLOR_BACKGROUND, rect, 1)