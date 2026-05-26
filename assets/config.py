# assets/config.py

# Screen Configurations
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 600
GAME_TITLE    = 'Snake Game'
FPS           = 60

# Grid Configurations
BLOCK_SIZE = 20

# Colors (RGB)
COLOR_BACKGROUND = (30, 30, 30)
COLOR_APPLE      = (231, 76,  60)   # Vermelho

# Cobra 1 — Verde
COLOR_SNAKE_1       = (46, 204, 113)
COLOR_SNAKE_1_HEAD  = (39, 174,  96)

# Cobra 2 — Azul
COLOR_SNAKE_2       = (52, 152, 219)
COLOR_SNAKE_2_HEAD  = (41, 128, 185)

# Game Mechanics
INITIAL_SPEED = 10

# Font Configurations
FONT_NAME   = 'Arial'
FONT_SIZE   = 25
COLOR_SCORE = (255, 255, 255)

# Controles — Jogador 1: Setas | Jogador 2: WASD
CONTROLS_P1 = {
    'UP':    'K_UP',
    'DOWN':  'K_DOWN',
    'LEFT':  'K_LEFT',
    'RIGHT': 'K_RIGHT',
}

CONTROLS_P2 = {
    'UP':    'K_w',
    'DOWN':  'K_s',
    'LEFT':  'K_a',
    'RIGHT': 'K_d',
}