"""
QWen3 

함수기반 sname 게임 

* 잘된점 
 1. 
 
* 큰 문제점 
 1. 
 
"""
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# ─── CONFIGURATION ───────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 12  # Controls game speed (classic snake feel)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SNAKE_COLOR = (0, 200, 0)
SNAKE_HEAD_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 50, 50)
GRID_COLOR = (30, 30, 30)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classic Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 32)
small_font = pygame.font.SysFont("consolas", 24)

# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────────
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_snake(snake_body):
    for i, segment in enumerate(snake_body):
        color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
        pygame.draw.rect(screen, color, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BLACK, (segment[0], segment[1], GRID_SIZE, GRID_SIZE), 2)

def draw_food(food_pos):
    pygame.draw.rect(screen, FOOD_COLOR, (food_pos[0], food_pos[1], GRID_SIZE, GRID_SIZE))

def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def spawn_food(snake_body):
    """Generates food at a random grid position, ensuring it doesn't spawn on the snake."""
    while True:
        pos = [random.randrange(0, GRID_WIDTH) * GRID_SIZE, 
               random.randrange(0, GRID_HEIGHT) * GRID_SIZE]
        if pos not in snake_body:
            return pos

# ─── GAME OVER SCREEN ────────────────────────────────────────────────────────────
def game_over_screen(score):
    screen.fill(BLACK)
    title = font.render("GAME OVER", True, (255, 50, 50))
    score_txt = font.render(f"Final Score: {score}", True, WHITE)
    prompt = small_font.render("Press [R] to Restart or [Q] to Quit", True, (150, 150, 150))

    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, HEIGHT//2))
    screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//3 * 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    return  # Restart game loop

# ─── MAIN GAME LOOP ──────────────────────────────────────────────────────────────
def game_loop():
    # Initial snake state (length 3, moving right)
    head_pos = [GRID_SIZE * 5, GRID_SIZE * 5]
    snake_body = [
        list(head_pos),
        [head_pos[0] - GRID_SIZE, head_pos[1]],
        [head_pos[0] - 2 * GRID_SIZE, head_pos[1]]
    ]
    
    direction = "RIGHT"
    change_to = direction
    food_pos = spawn_food(snake_body)
    score = 0

    running = True
    while running:
        # ── EVENT HANDLING ──
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Prevent 180° turns (direct reversal)
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        direction = change_to

        # ── MOVEMENT ──
        if direction == "UP":
            head_pos[1] -= GRID_SIZE
        elif direction == "DOWN":
            head_pos[1] += GRID_SIZE
        elif direction == "LEFT":
            head_pos[0] -= GRID_SIZE
        elif direction == "RIGHT":
            head_pos[0] += GRID_SIZE

        # Add new head to body
        snake_body.insert(0, list(head_pos))

        # ── FOOD CONSUMPTION ──
        if head_pos == food_pos:
            score += 1
            food_pos = spawn_food(snake_body)
        else:
            snake_body.pop()  # Remove tail if not eating

        # ── COLLISION / EVASION LOGIC ──
        # 1. Wall Evasion
        wall_hit = (head_pos[0] < 0 or head_pos[0] >= WIDTH or 
                    head_pos[1] < 0 or head_pos[1] >= HEIGHT)
        
        # 2. Self Evasion
        self_hit = head_pos in snake_body[1:]

        if wall_hit or self_hit:
            game_over_screen(score)
            return  # Exits to main menu/restart

        # ── RENDERING ──
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake_body)
        draw_food(food_pos)
        show_score(score)
        pygame.display.update()

        clock.tick(FPS)

# ─── ENTRY POINT ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        game_loop()