import pygame
import random

# parameters 
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
LEVEL_UP_SCORE = 5
pygame.font.init()
score_font = pygame.font.SysFont("Verdana", 20)  
score = 0
level = 1

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# initialize pygame
pygame.init()

# setting up display
display_surf = pygame.display.set_mode((WIDTH, HEIGHT))

# setting up clock
clock = pygame.time.Clock()

# snake and food initialization
snake_pos = [[WIDTH//2, HEIGHT//2]]
snake_speed = [0, BLOCK_SIZE]
food_pos = []
green_food_pos = []

#Generates a food position that doesn't collide with the snake
def generate_food():
    food_pos = [random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE]
    while food_pos in snake_pos or food_pos == green_food_pos:
        food_pos = [random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE]
    return food_pos

def generate_green_food():
    """Generates a position for green food that doesn't collide with the snake or red food."""
    green_food_pos = [random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                      random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE]
    while green_food_pos in snake_pos or green_food_pos == food_pos:
        green_food_pos = [random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                          random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE]
    return green_food_pos

food_pos = generate_food()
green_food_pos = generate_green_food()

#Draws snake, food, and score on the window
def draw_objects():
    display_surf.fill((0, 0, 0))
    for pos in snake_pos:
        pygame.draw.rect(display_surf, WHITE, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(display_surf, RED, pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(display_surf, GREEN, pygame.Rect(green_food_pos[0], green_food_pos[1], BLOCK_SIZE, BLOCK_SIZE))  # Draw green food
    
    # Render the score and level
    score_text = score_font.render(f"Score: {score} Level: {level}", True, WHITE)
    display_surf.blit(score_text, (10, 10))  # draws the score and level on the top-left corner
   
   
def update_snake():
    global food_pos, score, level,  green_food_pos
    new_head = [snake_pos[0][0] + snake_speed[0], snake_pos[0][1] + snake_speed[1]]
    
    if new_head[0] >= WIDTH:
        new_head[0] = 0
    elif new_head[0] < 0:
        new_head[0] = WIDTH - BLOCK_SIZE
    if new_head[1] >= HEIGHT:
        new_head[1] = 0
    elif new_head[1] < 0:
        new_head[1] = HEIGHT - BLOCK_SIZE

    # Eating red food
    if new_head == food_pos:
        food_pos = generate_food()
        score += 1  # Increment score for red food
        if score % LEVEL_UP_SCORE == 0:
            level += 1  # Increase level every LEVEL_UP_SCORE foods eaten
    elif new_head == green_food_pos:  # Eating green food
        green_food_pos = generate_green_food()
        score += 2  # Increment score by 2 for green food
    else:
        snake_pos.pop()  # Remove tail if no food eaten
    
    snake_pos.insert(0, new_head)  # Move snake head

def game_over():
    return snake_pos[0] in snake_pos[1:]

def game_over_screen():
    global score
    display_surf.fill((0, 0, 0))
    game_over_font = pygame.font.SysFont("consolas", 50)
    game_over_text = game_over_font.render(f"Game Over! Score: {score}", True, WHITE)
    display_surf.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run()  # replay the game
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()  # quit the game
                    return

def run():
    global snake_speed, snake_pos, food_pos, score, level, green_food_pos
    snake_pos = [[WIDTH//2, HEIGHT//2]]
    snake_speed = [0, BLOCK_SIZE]
    food_pos = generate_food()
    green_food_pos = generate_green_food()
    score = 0
    level = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # keys = pygame.key.get_pressed()
            # for key in keys:
            #     if keys[pygame.K_UP]:
            #         # when UP is pressed but the snake is moving down, ignore the input
            #         if snake_speed[1] == BLOCK_SIZE:
            #             continue
            #         snake_speed = [0, -BLOCK_SIZE]
            #     if keys[pygame.K_DOWN]:
            #         # when DOWN is pressed but the snake is moving up, ignore the input
            #         if snake_speed[1] == -BLOCK_SIZE:
            #             continue
            #         snake_speed = [0, BLOCK_SIZE]
            #     if keys[pygame.K_LEFT]:
            #         # when LEFT is pressed but the snake is moving right, ignore the input
            #         if snake_speed[0] == BLOCK_SIZE:
            #             continue
            #         snake_speed = [-BLOCK_SIZE, 0]
            #     if keys[pygame.K_RIGHT]:
            #         # when RIGHT is pressed but the snake is moving left, ignore the input
            #         if snake_speed[0] == -BLOCK_SIZE:
            #             continue
            #         snake_speed = [BLOCK_SIZE, 0]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake_speed[1] != BLOCK_SIZE:  # Check if not moving down
                        snake_speed = [0, -BLOCK_SIZE]
                elif event.key == pygame.K_DOWN:
                    if snake_speed[1] != -BLOCK_SIZE:  # Check if not moving up
                        snake_speed = [0, BLOCK_SIZE]
                elif event.key == pygame.K_LEFT:
                    if snake_speed[0] != BLOCK_SIZE:  # Check if not moving right
                        snake_speed = [-BLOCK_SIZE, 0]
                elif event.key == pygame.K_RIGHT:
                    if snake_speed[0] != -BLOCK_SIZE:  # Check if not moving left
                        snake_speed = [BLOCK_SIZE, 0]

        draw_objects()
        update_snake()
        if game_over():
            game_over_screen()
            break
        pygame.display.update()
        clock.tick(10 + level * 2)
    pygame.quit()


if __name__ == '__main__':
    run()
    pygame.quit()
