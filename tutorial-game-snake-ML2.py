import pygame
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import os

from tutorial_game_snake import SnakeGame

# ─── CONFIG ──────────────────────────────────────────────────────────────────────

ACTION_SPACE = 3  # 0: 직진, 1: 우회전, 2: 좌회전
STATE_SIZE = 11   # [위험3, 방향4, 먹이방향4]

# ─── SNAKE ENVIRONMENT ──────────────────────────────────────────────────────────
class SnakeEnv(SnakeGame):
    def __init__(self, render=True):
        SnakeGame.__init__(self,render)
        self.steps = 0
        #self.render_flag = render
        #if self.render_flag:
        #    pass
        #self.reset()
        #self.game_init()
        self.FPS=100

    def reset(self):
        self.done = False
        self.steps =0 #!!!
        self.game_init()
        return self._get_state()

    
    def _get_state(self): # 
        head = self.head_pos #
        dirs = self.dirs
        #self.dir_idx=self.direction #hmm
        
        # 현재 방향 기준 상대적 방향 (직진, 우회전, 좌회전)    
        rel_dirs = [dirs[self.dir_idx], dirs[(self.dir_idx+1)%4], dirs[(self.dir_idx+3)%4]] 
        
        # 1. 전방/우측/좌측 충돌 여부, 미리 예측 하는 건뎅....
        danger = [self.is_collision([head[0]+d[0], head[1]+d[1]]) for d in rel_dirs]
                
        direction = [1 if i == self.dir_idx else 0 for i in range(4)] # 2. 현재 방향 (One-hot)
                
        food_dir = [self.food_pos[0] < head[0], self.food_pos[0] > head[0],  
                    self.food_pos[1] < head[1], self.food_pos[1] > head[1]] # 3. 먹이 상대 위치
        
        return np.array([*danger, *direction, *food_dir], dtype=np.float32)
    
    
    def step(self, action):
        #head = self.head_pos 
        #self.dir_idx=self.direction #hmm
        # action: 0=straight, 1=right, 2=left
        if action == 1: 
            self.dir_idx = (self.dir_idx + 1) % 4
        elif action == 2: 
            self.dir_idx = (self.dir_idx + 3) % 4
        
        #dx, dy = self.dir[self.dir_idx] #         
        #head = [head[0] + dx, head[1] + dy]
        #self.snake_body.insert(0, list(head))
        self.change_to = self.dir_idx                
        self.process_keyevent()
        self.process_game()
        self.steps += 1
        
        if self.steps > 100 * (len(self.snake_body) + 3): # 무한 루프 방지
            self.done = True
            self.reward -= 10
        
        if self.score > self.score_prev: # hit something!
            self.reward += 10 #
            self.score_prev = self.score
        
        if self.state == "GAME_OVER": # hit something!
            self.reward -= 10 # 
            self.done = True
            
        if self.render_flag:
            self.render()
            
        return self._get_state(), self.reward, self.done, self.score

    

# ─── DQN AGENT (PyTorch) ───────────────────────────────────────────────────────
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_size, 256), nn.ReLU(),
            nn.Linear(256, 256), nn.ReLU(),
            nn.Linear(256, action_size)
        )
    def forward(self, x):
        return self.net(x)

class DQNAgent:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy_net = DQN(STATE_SIZE, ACTION_SPACE).to(self.device)
        self.target_net = DQN(STATE_SIZE, ACTION_SPACE).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=1e-3)
        self.memory = deque(maxlen=20000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 64

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(ACTION_SPACE)
        state_t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            return torch.argmax(self.policy_net(state_t), dim=1).item()

    def learn(self): # learn
        if len(self.memory) < self.batch_size: 
            return
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = map(np.array, zip(*batch))
        #states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)
        #states, actions, rewards, next_states, dones = zip(*batch)
        """    torch.tensor(np.array(states), dtype=torch.float32),
           torch.tensor(np.array(actions), dtype=torch.long).unsqueeze(1),
           torch.tensor(np.array(rewards), dtype=torch.float32).unsqueeze(1),
           torch.tensor(np.array(next_states), dtype=torch.float32),
           torch.tensor(np.array(dones), dtype=torch.float32).unsqueeze(1)
           """
        s_t = torch.FloatTensor(states).to(self.device)
        ns_t = torch.FloatTensor(next_states).to(self.device)
        a_t = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        r_t = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        d_t = torch.FloatTensor(dones).unsqueeze(1).to(self.device)

        curr_q = self.policy_net(s_t).gather(1, a_t)
        next_q = self.target_net(ns_t).max(1, keepdim=True)[0]
        target_q = r_t + self.gamma * next_q * (1 - d_t)

        loss = nn.MSELoss()(curr_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

# ─── TRAINING & INFERENCE ───────────────────────────────────────────────────────
def train(epochs=1000, target_update=10):
    
    env = SnakeEnv(render=False)  # 학습 시 렌더링 OFF (속도 향상)
    agent = DQNAgent()
    if os.path.exists("snake_dqn.pth"):
        print("❌ 학습된 모델이 있음")
        #agent.policy_net.load_state_dict(torch.load("snake_dqn.pth", map_location=agent.device))
        #agent.epsilon = 0.0  # Pure exploitation
 
    scores = []
    
    print(f"🚀 Training started on {agent.device}")
    for ep in range(1, epochs + 1):
        state = env.reset() 
        env.reward = 0
        #print("x1")
        while True:
            action = agent.act(state)
            next_state, reward, done, score = env.step(action)
            agent.remember(state, action, reward, next_state, done)            
            state = next_state
            if done: 
                break
        agent.learn()
        #scores.append(score)
        if ep % target_update == 0:
            agent.update_target()
        if ep % 50 == 0:
            avg = np.mean(scores[-50:])
            print(f"Ep {ep:4d} | Score: {score:3d} | Eps: {agent.epsilon:.3f} | Avg50: {avg:.2f}")
    env.quit()
    torch.save(agent.policy_net.state_dict(), "snake_dqn.pth")
    print("✅ Model saved to snake_dqn.pth")

def play1():
    if not os.path.exists("snake_dqn.pth"):
        print("❌ 학습된 모델이 없습니다. 먼저 train()을 실행하세요.")
        return
    env = SnakeEnv(render=False)
    agent = DQNAgent()
    agent.policy_net.load_state_dict(torch.load("snake_dqn.pth", map_location=agent.device))
    agent.epsilon = 0.0  # Pure exploitation
    
    print("🎮 Inference Mode - Press ESC to quit")
    state = env.reset()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
        action = agent.act(state)
        state, _, done, _ = env.step(action)
        if done:
            state = env.reset()

def play():
    if not os.path.exists("snake_dqn.pth"):
        print("❌ 학습된 모델이 없습니다. 먼저 train()을 실행하세요.")
        return
    env = SnakeEnv(render=True)
    agent = DQNAgent()
    agent.policy_net.load_state_dict(torch.load("snake_dqn.pth", map_location=agent.device))
    agent.epsilon = 0.0  # Pure exploitation
    
    print("🎮 Inference Mode - Press ESC to quit")
    done=False
    state = env.reset()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
        action = agent.act(state)
        state, _, done, _ = env.step(action)
        if done:
            state = env.reset()
            break    

if __name__ == "__main__":
    #import sys
    #mode = sys.argv[1] 
    #if len(sys.argv) > 1 else "train"
    mode = "train"
    if mode == "train":
        train(epochs=1000)
    elif mode == "play":
        play()
    else:
        print("Usage: python snake_dqn.py [train|play]")