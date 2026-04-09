#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 21:44:18 2026

@author: hyun
perfect works!!

클래스와 차이점 진짜 예제로 좋다...

"""

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# ─── CONFIGURATION ───────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 640*2, 480*2
GRID_SIZE = 40
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


class SnakeGame:
    def __init__(self, render=True):
        self.render_flag = render
        if self.render_flag:
            #os.environ["SDL_VIDEODRIVER"] = "x11"  # 리눅스/맥 환경용 (필요시 주석)            
            #self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            #pygame.display.set_caption("Snake DQN - Inference")
            #self.clock = pygame.time.Clock()
            #elf.font = pygame.font.SysFont("consolas", 24)
            pass
        #self.reset()

        
    # ─── MAIN GAME LOOP ──────────────────────────────────────────────────────────────
    def game_init(self):
        # Initial snake state (length 3, moving right)
        self.head_pos = [GRID_SIZE * 5, GRID_SIZE * 5]
        self.snake_body = [
            list(self.head_pos),
            [self.head_pos[0] - GRID_SIZE, self.head_pos[1]],
            [self.head_pos[0] - 2 * GRID_SIZE, self.head_pos[1]]
        ]
        
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.food_pos = self.spawn_food(self.snake_body)
        self.score = 0
        self.state = "START" # START, DEAD , GAME_OVER
    
    def spawn_food(self, snake_body):
        """Generates food at a random grid position, ensuring it doesn't spawn on the snake."""
        while True:
            pos = [random.randrange(0, GRID_WIDTH) * GRID_SIZE, 
                   random.randrange(0, GRID_HEIGHT) * GRID_SIZE]
            if pos not in snake_body:
                return pos
    def process_keyevent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Prevent 180° turns (direct reversal)
                if self.state=="START":
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.change_to = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.change_to = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.change_to = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.change_to = "RIGHT"                                        
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit() 
                if self.state=="GAME_OVER":
                    if event.key == pygame.K_r:
                        self.game_init()
                    if event.key == pygame.K_q:                        
                        pygame.quit()
                        sys.exit() 
                    pass
    
    def do_process(self):              
        self.direction = self.change_to
        
        if self.state=="START":
            # ── MOVEMENT ──
            if self.direction == "UP":
                self.head_pos[1] -= GRID_SIZE
            elif self.direction == "DOWN":
                self.head_pos[1] += GRID_SIZE
            elif self.direction == "LEFT":
                self.head_pos[0] -= GRID_SIZE
            elif self.direction == "RIGHT":
                self.head_pos[0] += GRID_SIZE
    
            # Add new head to body
            self.snake_body.insert(0, list(self.head_pos))
    
            # ── FOOD CONSUMPTION ──
            if self.head_pos == self.food_pos:
                self.score += 1
                self.food_pos = self.spawn_food(self.snake_body)
            else:
                self.snake_body.pop()  # Remove tail if not eating
    
            # ── COLLISION / EVASION LOGIC ──
            # 1. Wall Evasion
            wall_hit = (self.head_pos[0] < 0 or self.head_pos[0] >= WIDTH or 
                        self.head_pos[1] < 0 or self.head_pos[1] >= HEIGHT)
            
            # 2. Self Evasion
            self_hit = self.head_pos in self.snake_body[1:]
    
            if wall_hit or self_hit:
                self.state="DEAD"
                #self.game_over_screen(self.score)
                #return  # Exits to main menu/restart
        if self.state=="DEAD":
            self.state="GAME_OVER"
            
        if self.state=="GAME_OVER":
            pass
    
    def render(self):
        # ── RENDERING ──
        if self.state=="START":
            screen.fill(BLACK)
            draw_grid()
            draw_snake(self.snake_body)
            draw_food(self.food_pos)
            show_score(self.score)            
        if self.state=="GAME_OVER":
            self.game_over_screen(self.score)
        pygame.display.update()
        clock.tick(FPS)
    
    def game_over_screen(self,score):
        # ─── GAME OVER SCREEN ────────────────────────────────────────────────────────────
        screen.fill(BLACK)
        title = font.render("GAME OVER", True, (255, 50, 50))
        score_txt = font.render(f"Final Score: {score}", True, WHITE)
        prompt = small_font.render("Press [R] to Restart or [Q] to Quit", True, (150, 150, 150))
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, HEIGHT//2))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//3 * 2))
 

# ─── ENTRY POINT ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _game=SnakeGame()
    _game.game_init()
    while True:        
        # ── EVENT HANDLING ──
        _game.process_keyevent()
        _game.do_process()
        _game.render()