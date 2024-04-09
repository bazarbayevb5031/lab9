import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint Program Extended")
another_layer = pygame.Surface((800, 600))
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
current_color = BLACK

# Tools
tools = ['draw', 'rectangle', 'circle', 'eraser', 'square', 'right triangle', 'equilateral triangle', 'rhombus']
current_tool = 'draw'

# Drawing variables
drawing = False
start_pos = None

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
            drawing = True
            if current_tool == 'eraser':
                pygame.draw.circle(screen, BLACK, event.pos, 10)
                
        # Mouse motion event
        if event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == 'draw':
                pygame.draw.line(screen, current_color, start_pos, event.pos, 2)
                start_pos = event.pos
            elif current_tool == 'eraser':
                pygame.draw.circle(screen, BLACK, event.pos, 10)
            elif current_tool == 'rectangle':
                end_pos = event.pos
                screen.blit(another_layer, (0, 0))
                pygame.draw.rect(screen, current_color, pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])))
            elif current_tool == 'circle':
                end_pos = event.pos
                screen.blit(another_layer, (0, 0))
                radius = int(((start_pos[0] - end_pos[0]) ** 2 + (start_pos[1] - end_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius)
            elif current_tool == 'square':
                end_pos = event.pos
                screen.blit(another_layer, (0, 0))
                pygame.draw.rect(screen, current_color, pygame.Rect(start_pos, (min(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]), min(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))))
            elif current_tool == 'right triangle':
                end_pos = event.pos
                screen.blit(another_layer, (0, 0))
                pygame.draw.line(screen, current_color, start_pos, end_pos)
                pygame.draw.line(screen, current_color, (start_pos[0], end_pos[1]), end_pos)
                pygame.draw.line(screen, current_color, start_pos, (start_pos[0], end_pos[1]))
            elif current_tool == 'equilateral triangle':
                end_pos = event.pos
                screen.blit(another_layer, (0, 0))
                pygame.draw.line(screen, current_color, ((start_pos[0] + end_pos[0]) / 2, start_pos[1]), end_pos)
                pygame.draw.line(screen, current_color, (start_pos[0], end_pos[1]), end_pos)
                pygame.draw.line(screen, current_color, ((start_pos[0] + end_pos[0]) / 2, start_pos[1]), (start_pos[0], end_pos[1]))
            elif current_tool == 'rhombus':
                end_pos = event.pos
                screen.blit(another_layer, (0, 0))
                pygame.draw.line(screen, current_color, ((start_pos[0] + end_pos[0]) / 2, start_pos[1]), (end_pos[0], (end_pos[1] + start_pos[1]) / 2))
                pygame.draw.line(screen, current_color, (start_pos[0], (end_pos[1] + start_pos[1]) / 2), ((start_pos[0] + end_pos[0]) / 2, end_pos[1]))
                pygame.draw.line(screen, current_color, ((start_pos[0] + end_pos[0]) / 2, start_pos[1]), (start_pos[0], (end_pos[1] + start_pos[1]) / 2))
                pygame.draw.line(screen, current_color, (end_pos[0], (end_pos[1] + start_pos[1]) / 2), ((start_pos[0] + end_pos[0]) / 2, end_pos[1]))
            
                # Tool selection with keyboard (simplified)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tool = 'draw'
            elif event.key == pygame.K_2:
                current_tool = 'rectangle'
            elif event.key == pygame.K_3:
                current_tool = 'circle'
            elif event.key == pygame.K_4:
                current_tool = 'eraser'
            elif event.key == pygame.K_5:
                current_tool = 'square'
            elif event.key == pygame.K_6:
                current_tool = 'right triangle'
            elif event.key == pygame.K_7:
                current_tool = 'equilateral triangle'
            elif event.key == pygame.K_8:
                current_tool = 'rhombus'
            # Color selection
            elif event.key == pygame.K_r:
                current_color = RED
            elif event.key == pygame.K_g:
                current_color = GREEN
            elif event.key == pygame.K_b:
                current_color = BLUE

        # Mouse button up event
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            another_layer.blit(screen, (0, 0))
                
            
            
                

    pygame.display.flip()
