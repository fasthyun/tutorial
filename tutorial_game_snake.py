#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 21:44:18 2026

@author: hyun
perfect works!!

* 클래스와 차이점 진짜 예제로 좋다...(hyun)
* 그리고 추가할것이....

"""
import pygame
import random
import sys

# ─── CONFIGURATION ───────────────────────────────────────────────────────────────
SCREEN_WIDTH, SCREEN_HEIGHT = 640*2, 480*2
GRID_SIZE = 80
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SNAKE_COLOR = (0, 200, 0)
SNAKE_HEAD_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 50, 50)
GRID_COLOR = (30, 30, 30)



# ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────────

class SnakeBase:
    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    def draw_snake(self,snake_body):
        for i, segment in enumerate(snake_body):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            pygame.draw.rect(self.screen, color, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.screen, BLACK, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

    def draw_food(self,food_pos):
        pygame.draw.rect(self.screen, FOOD_COLOR, (food_pos[0]*GRID_SIZE, food_pos[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def show_score(self, score):
        text = self.font.render(f"Score: {score}", True, WHITE)
        self.screen.blit(text, (10, 10))

    def game_over_screen(self,score):
        # ─── GAME OVER SCREEN ────────────────────────────────────────────────────────────
        #self.screen.fill(BLACK)
        title = self.font.render("GAME OVER", True, (255, 50, 50))
        score_txt = self.font.render(f"Final Score: {score}", True, WHITE)
        prompt = self.small_font.render("Press [R] to Restart or [Q] to Quit", True, (150, 150, 150))
        
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
        self.screen.blit(score_txt, (SCREEN_WIDTH//2 - score_txt.get_width()//2, SCREEN_HEIGHT//2))
        self.screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, SCREEN_HEIGHT//3 * 2))

    
class SnakeGame(SnakeBase):
    def __init__(self, render=True):
        # Initialize pygame
        self.FPS = 10  # Controls game speed (classic snake feel) I Dont like this (hyun)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.render_flag = render
        if render == True:
            pygame.display.set_caption("Classic Snake Game")        
            self.font = pygame.font.SysFont("consolas", 32)
            self.small_font = pygame.font.SysFont("consolas", 24)                    
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))                               
        
        self.game_init()
    
    def quit(self):
        pygame.quit()
        sys.exit() 
        
    def xreset(self): # for ML_DQN
        #self.game_init()
        #self.dir_idx = 1  # 0:UP, 1:RIGHT, 2:DOWN, 3:LEFT
        #self.steps = 0
        #self.done = False
        #return self._get_state()
        pass
    
    def state(self): # for ML_DQN
        return
        
    # ─── MAIN GAME LOOP ──────────────────────────────────────────────────────────────
    def game_init(self):
        # Initial snake state (length 3, moving right)
        self.head_pos = [ 5,  5]
        self.snake_body = [
            list(self.head_pos),
            [self.head_pos[0] , self.head_pos[1]],
            [self.head_pos[0] - 2 , self.head_pos[1]] # length 3 
        ]
        
        # 벡터스타일 방향 표시 절대방향 4개 (dx,dy)
        self.dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # UP:0, RIGHT:1, DOWN:2, LEFT:3          
        self.direction = 1 # 0:UP, 1:RIGHT, 2:DOWN, 3:LEFT
        self.dir_idx = 1 # 0:UP, 1:RIGHT, 2:DOWN, 3:LEFT
        self.change_to = self.direction
        self.food_pos = self.spawn_food(self.snake_body)
        self.score = 0
        self.score_prev=0
        self.state = "START" # START, DEAD , GAME_OVER
    
    def spawn_food(self, snake_body):
        """Generates food at a random grid position, ensuring it doesn't spawn on the snake."""
        while True: # good? hmm...
            pos = [random.randrange(0, GRID_WIDTH),
                   random.randrange(0, GRID_HEIGHT)]
            if pos not in snake_body:
                return pos
    
    def autonomous(self):        
        head = self.head_pos #
        dirs = self.dirs        
        # 방향을 복잡하게 정의해버렸네(hyun) 절대방향에서 상대방향으로 바뀜 : self.direction ----> re        
        dir_idx = self.direction  # 0:UP, 1:RIGHT, 2:DOWN, 3:LEFT
        # 현재 방향 기준 상대적 방향 [직진, 우회전, 좌회전]
        rel_dirs = [dirs[dir_idx], dirs[(dir_idx+1)%4], dirs[(dir_idx+3)%4]]
        # 1. 전방/우측/좌측 충돌 여부 ===> 미리 예측 하는 건뎅....
        danger = [self.is_collision([head[0]+d[0], head[1]+d[1]]) for d in rel_dirs]
        
        direction = [1 if i == dir_idx else 0 for i in range(4)] # 2. 현재 방향 (One-hot) ===> 무의미한뎅...
        
        # 3. 먹이 상대 위치 ===> [dx,dy]
        food_dir = (self.food_pos[0] - head[0], self.food_pos[1] - head[1])
        
        _d=[self.is_collision([head[0]+d[0], head[1]+d[1]]) for d in rel_dirs]
        
        """  절대방향 방식은 안됨!!!
        if food_dir[0] < 0 :
            self.change_to =  3 # LEFT
        else :
            self.change_to =  1 # RIGHT
        
        if food_dir[1] < 0 :
            self.change_to =  0 # UP
        else :
            self.change_to =  2 # DOWN
        #for i,v in enumerate(self.dirs):
        #    if v == food_dir :
        #        self.change_to =  i
        #        pass
        """
        print(food_dir, self.change_to,danger,rel_dirs,direction)
    def process_keyevent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Prevent 180° turns (direct reversal)
                if self.state=="START":
                    if event.key == pygame.K_UP and self.direction != 2 : #"DOWN":
                        self.change_to = 0 #"UP"
                    elif event.key == pygame.K_DOWN and self.direction != 0 : #"UP":
                        self.change_to = 2 #"DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != 1 : #"RIGHT":
                        self.change_to = 3 #"LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction !=3 :# "LEFT":
                        self.change_to = 1 #"RIGHT"                                        
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
    
    def is_collision(self, _pos):        
        # ── COLLISION / EVASION LOGIC ──        
        # 1. Wall Evasion
        wall_hit = (_pos[0] < 0 or _pos[0] >= GRID_WIDTH or 
                    _pos[1] < 0 or _pos[1] >= GRID_HEIGHT)
        
        # 2. Self Evasion
        self_hit = _pos in self.snake_body[1:]
        
        if wall_hit or self_hit:
            return True
        else:
            return False
    
    
    def process_game(self):              
        self.direction = self.change_to        
        if self.state=="START":
            # ── MOVEMENT ──
            if self.direction == 0 :# "UP":
                self.head_pos[1] -= 1
            elif self.direction ==2  : #"DOWN":
                self.head_pos[1] += 1
            elif self.direction ==3: #"LEFT":
                self.head_pos[0] -= 1
            elif self.direction ==1: #"RIGHT":
                self.head_pos[0] += 1
    
            # Add new head to body
            self.snake_body.insert(0, list(self.head_pos))
    
            # ── FOOD CONSUMPTION ──
            if self.head_pos == self.food_pos:
                self.score += 1
                self.food_pos = self.spawn_food(self.snake_body)
            else:
                self.snake_body.pop()  # Remove tail if not eating
    
            if self.is_collision(self.head_pos):
                self.state="GAME_OVER"
                
        if self.state=="GAME_OVER":
            # do something
            pass
    
 
    def render(self):
        # ── RENDERING ──        
        if self.state=="START":
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_snake(self.snake_body)
            self.draw_food(self.food_pos)
            self.show_score(self.score)            
        if self.state=="GAME_OVER":
            self.game_over_screen(self.score)        
        
        if self.render_flag==True: # Temp!
            self.clock.tick(self.FPS) # delay? or sleep?               
        pygame.display.update()
        
# ─── ENTRY POINT ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _game=SnakeGame()
    _game.game_init()
    while True:        
        # ── EVENT HANDLING ──
        _game.process_keyevent()
        _game.autonomous()
        _game.process_game()
        _game.render()