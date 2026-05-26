import pygame
from assets import config

class Snake:
    def __init__(self):
        """Inicializa a cobrinha no centro da tela com 3 blocos de comprimento."""
        self.block_size = config.BLOCK_SIZE
        
        # Posições iniciais (corpo da cobra). Cada bloco é uma lista [x, y]
        # Começa no centro da tela e se estende para a esquerda
        self.body = [
            [config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2],
            [(config.SCREEN_WIDTH // 2) - self.block_size, config.SCREEN_HEIGHT // 2],
            [(config.SCREEN_WIDTH // 2) - (2 * self.block_size), config.SCREEN_HEIGHT // 2]
        ]
        
        # Direções de movimento (X, Y) em pixels por passo
        # Começa se movendo para a DIREITA
        self.direction = [self.block_size, 0]

    def change_direction(self, new_direction):
        """
        Altera a direção da cobra, impedindo que ela faça 
        uma curva de 180 graus diretamente sobre si mesma.
        """
        # Se estiver indo para a direita, não pode ir para a esquerda instantaneamente, etc.
        if new_direction == "UP" and self.direction != [0, self.block_size]:
            self.direction = [0, -self.block_size]
        elif new_direction == "DOWN" and self.direction != [0, -self.block_size]:
            self.direction = [0, self.block_size]
        elif new_direction == "LEFT" and self.direction != [self.block_size, 0]:
            self.direction = [-self.block_size, 0]
        elif new_direction == "RIGHT" and self.direction != [-self.block_size, 0]:
            self.direction = [self.block_size, 0]

    def move(self):
        """Move a cobra calculando a nova cabeça e removendo a ponta do rabo."""
        # Calcula a nova posição da cabeça baseada na direção atual
        current_head = self.body[0]
        new_head = [
            current_head[0] + self.direction[0],
            current_head[1] + self.direction[1]
        ]
        
        # Insere a nova cabeça no início da lista
        self.body.insert(0, new_head)
        
        # Remove o último bloco do rabo (mantém o tamanho estável ao andar)
        self.body.pop()

    def draw(self, surface):
        """Desenha cada bloco do corpo da cobrinha na tela."""
        for block in self.body:
            rect = pygame.Rect(block[0], block[1], self.block_size, self.block_size)
            pygame.draw.rect(surface, config.COLOR_SNAKE, rect)

    def check_self_collision(self):
            """Retorna True se a cabeça da cobra colidir com qualquer parte do seu corpo."""
            head = self.body[0]
            # Verifica se a cabeça está presente no restante do corpo (do índice 1 em diante)
            return head in self.body[1:]