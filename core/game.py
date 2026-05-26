import pygame
import sys
from assets import config
from core.screen import GameScreen
from core.snake import Snake
from core.apple import Apple
from core.hud import HUD

def run_game():
    pygame.init()
    screen = GameScreen()
    clock = pygame.time.Clock()
    
    snake = Snake()
    apple = Apple(snake.body)
    hud = HUD()
    
    SNAKE_MOVE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SNAKE_MOVE_EVENT, 1000 // config.INITIAL_SPEED)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == SNAKE_MOVE_EVENT:
                current_head = snake.body[0]
                new_head = [
                    current_head[0] + snake.direction[0],
                    current_head[1] + snake.direction[1]
                ]
                
                if new_head == apple.position:
                    snake.body.insert(0, new_head)
                    apple.randomize_position(snake.body)
                else:
                    snake.move()
                
                # Sistema de Colisões (Game Over)
                head = snake.body[0]
                hit_wall_x = head[0] < 0 or head[0] >= config.SCREEN_WIDTH
                hit_wall_y = head[1] < 0 or head[1] >= config.SCREEN_HEIGHT
                hit_self = snake.check_self_collision()
                
                if hit_wall_x or hit_wall_y or hit_self:
                    # --- NOVO: Salva o recorde antes de resetar o jogo ---
                    current_score = len(snake.body) - 3
                    hud.save_high_score(current_score)
                    
                    # Reset do Jogo
                    snake = Snake()
                    apple = Apple(snake.body)
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
        
        screen.render_background()
        
        snake.draw(screen.surface)
        apple.draw(screen.surface)
        hud.draw_score(screen.surface, len(snake.body))
        
        screen.update()
        clock.tick(config.FPS)

if __name__ == "__main__":
    run_game()