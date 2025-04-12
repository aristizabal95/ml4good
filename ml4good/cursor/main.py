import pygame
import sys
from game.engine import GameEngine
from game.ui import GameUI
from game.config import GameConfig

def main():
    # Initialize pygame
    pygame.init()
    
    # Load configuration
    config = GameConfig()
    
    # Initialize game components
    engine = GameEngine(config)
    ui = GameUI(config)
    
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    engine.handle_input(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    action = ui.handle_click(event.pos)
                    if action:
                        if action == 'reload':
                            engine.handle_input(pygame.K_r)
                        elif action == 'retrain':
                            engine.handle_input(pygame.K_t)
                        elif action == 'shutdown':
                            engine.handle_input(pygame.K_s)
                        elif action == 'railguards':
                            engine.purchase_railguards()
        
        # Update game state
        engine.update()
        
        # Render game
        ui.render(engine.get_game_state())
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 