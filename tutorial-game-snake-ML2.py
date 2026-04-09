import pygame
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import os

# ─── CONFIG ──────────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 15

ACTION_SPACE = 3  # 0: 직진, 1: 우회전, 2: 좌회전
STATE_SIZE = 11   # [위험3, 방향4, 먹이방향4]

# ─── SNAKE ENVIRONMENT ──────────────────────────────────────────────────────────
class SnakeEnv:
    def __init__(self, render=True):
        self.render_flag = render
        if self.render_flag:
            pass
        self.reset()

    def reset(self):
        self.head = [GRID_SIZE * 5, GRID_SIZE * 5]
        self.body = [list(self.head),
                     [self.head[0] - GRID_SIZE, self.head[1]],
                     [self.head[0] - 2 * GRID_SIZE, self.head[1]]]
        self.dir_idx = 1  # 0:UP, 1:RIGHT, 2:DOWN, 3:LEFT
        self.food = self._spawn_food()
        self.score = 0
        self.steps = 0
        self.done = False
        return self._get_state()

    def _spawn_food(self):
        pass

    def _is_collision(self, point):
        return (point[0] < 0 or point[0] >= WIDTH or
                point[1] < 0 or point[1] >= HEIGHT or
                point in self.body)

    def _get_state(self):
        head = self.head
        dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # UP, RIGHT, DOWN, LEFT
        
        # 현재 방향 기준 상대적 방향 (직진, 우회전, 좌회전)
        rel_dirs = [dirs[self.dir_idx], dirs[(self.dir_idx+1)%4], dirs[(self.dir_idx+3)%4]]
        
        # 1. 전방/우측/좌측 충돌 여부
        danger = [self._is_collision([head[0]+d[0]*GRID_SIZE, head[1]+d[1]*GRID_SIZE]) for d in rel_dirs]
        
        # 2. 현재 방향 (One-hot)
        direction = [1 if i == self.dir_idx else 0 for i in range(4)]
        
        # 3. 먹이 상대 위치
        food_dir = [self.food[0] < head[0], self.food[0] > head[0],
                    self.food[1] < head[1], self.food[1] > head[1]]
        
        return np.array([*danger, *direction, *food_dir], dtype=np.float32)

    def step(self, action):
        # action: 0=straight, 1=right, 2=left
        if action == 1: self.dir_idx = (self.dir_idx + 1) % 4
        elif action == 2: self.dir_idx = (self.dir_idx + 3) % 4
        
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.dir_idx]
        self.head = [self.head[0] + dx*GRID_SIZE, self.head[1] + dy*GRID_SIZE]
        self.body.insert(0, list(self.head))
        
        reward = 0
        self.steps += 1
        
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.food = self._spawn_food()
        else:
            self.body.pop()
            reward = -0.1  # 속도 장려 페널티

        # 사망 체크
        if self._is_collision(self.head):
            self.done = True
            reward = -10
            
        # 무한 루프 방지
        if self.steps > 100 * (len(self.body) + 3):
            self.done = True
            reward = -10

        if self.render_flag:
            self._render()
            
        return self._get_state(), reward, self.done, self.score

    def _render(self):
        #self.screen.fill((0, 0, 0))
        #pygame.display.update()
        #self.clock.tick(FPS)
        pass

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

    def replay(self):
        if len(self.memory) < self.batch_size: return
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = map(np.array, zip(*batch))
        
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
    env = SnakeGame(render=True)  # 학습 시 렌더링 OFF (속도 향상)
    agent = DQNAgent()
    scores = []
    
    print(f"🚀 Training started on {agent.device}")
    for ep in range(1, epochs + 1):
        state = env.reset()
        while True:
            action = agent.act(state)
            next_state, reward, done, score = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
            state = next_state
            if done: break
            
        scores.append(score)
        if ep % target_update == 0:
            agent.update_target()
        if ep % 50 == 0:
            avg = np.mean(scores[-50:])
            print(f"Ep {ep:4d} | Score: {score:3d} | Eps: {agent.epsilon:.3f} | Avg50: {avg:.2f}")
            
    torch.save(agent.policy_net.state_dict(), "snake_dqn.pth")
    print("✅ Model saved to snake_dqn.pth")

def play1():
    if not os.path.exists("snake_dqn.pth"):
        print("❌ 학습된 모델이 없습니다. 먼저 train()을 실행하세요.")
        return
    env = SnakeEnv(render=True)
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
    env = SnakeEnv(render=True)    
    state = env.reset()
    done=False
    while True:
        #env.process
        #action = agent.act(state)
        #state, _, done, _ = env.step(action)
        #if done:
        #    env.reset()


if __name__ == "__main__":
    #import sys
    #mode = sys.argv[1] 
    #if len(sys.argv) > 1 else "train"
    mode = "play"
    if mode == "train":
        train(epochs=1000)
    elif mode == "play":
        play()
    else:
        print("Usage: python snake_dqn.py [train|play]")