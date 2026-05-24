#import pygame
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import os


from tutorial_game_snake import SnakeGame

# ─── CONFIG ──────────────────────────────────────────────────────────────────────
#torch.set_default_device('cuda')
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
        self.FPS=30
        self.reward = 0
        self.step_count_without_reward=0

    def reset(self):
        self.done = False
        self.steps =0 #!!!
        self.reward = 0
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
                    self.food_pos[1] < head[1], self.food_pos[1] > head[1]] # 3. 먹이 상대 위치 ??? 이게뭐
                
        return np.array([*danger, *direction, *food_dir], dtype=np.float32)
    
    
    def step(self, action):
        #head = self.head_pos 
        #self.dir_idx=self.direction #hmm
        # action: 0=straight, 1=right, 2=left
        if action == 1: 
            self.dir_idx = (self.dir_idx + 1) % 4
        elif action == 2: 
            self.dir_idx = (self.dir_idx + 3) % 4
        
        self.change_to = self.dir_idx                
        self.process_keyevent()
        self.process_game() # game process        
        
        #if self.steps > 10 * (len(self.snake_body) + 3): # 무한 루프 방지
        #    self.reward -= 10
        #    self.done = True            
        if self.step_count_without_reward > 70 : # no eat then,             
            self.reward -=1
            self.step_count_without_reward=0
            self.done =True            
            #if self.reward < -30 :
            #    self.done = True
            #    #self.reward = -100
        
        if self.score > self.score_prev: # hit something!
            self.reward += 10 #
            self.step_count_without_reward=0
            self.score_prev = self.score
            self.done = True
        
        if self.state == "GAME_OVER": # hit something!
            self.reward -= 10 # 
            self.done = True
            
        if self.render_flag:
            self.render()
        self.steps += 1
        self.step_count_without_reward+=1
        
        return self._get_state(), self.reward, self.done, self.score

    

# ─── DQN AGENT (PyTorch) ───────────────────────────────────────────────────────
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_size, 256), nn.ReLU(),
            nn.Linear(256, 256), nn.ReLU(), # very important !
            nn.Linear(256, action_size)
        )
    def forward(self, x):
        return self.net(x)



class DQNAgent1:
    """
    with epsilon
    """
    def __init__(self,_policydict=None):
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.policy_net = DQN(STATE_SIZE, ACTION_SPACE) # t실제 사용되는 신경망
        #if _policydict !=None:            
        #    self.policy_net.load_state_dict(_policydict)
        self.target_net = DQN(STATE_SIZE, ACTION_SPACE)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=1e-3)
        self.memory = deque(maxlen=20000)
        self.gamma = 0.95
        
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.996
        self.batch_size = 50
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(ACTION_SPACE)
        
        state_t = torch.FloatTensor(state).unsqueeze(0)
        
        with torch.no_grad():
            return torch.argmax(self.policy_net(state_t), dim=1).item()

    def learn(self): # learn
        if len(self.memory) < self.batch_size: 
            return
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = map(np.array, zip(*batch))
        #states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)
        #states, actions, rewards, next_states, dones = zip(*batch)
        """  
            torch.tensor(np.array(states), dtype=torch.float32),
            torch.tensor(np.array(actions), dtype=torch.long).unsqueeze(1),
            torch.tensor(np.array(rewards), dtype=torch.float32).unsqueeze(1),
            torch.tensor(np.array(next_states), dtype=torch.float32),
            torch.tensor(np.array(dones), dtype=torch.float32).unsqueeze(1)
        """
        s_t = torch.FloatTensor(states)
        ns_t = torch.FloatTensor(next_states)
        a_t = torch.LongTensor(actions).unsqueeze(1)
        r_t = torch.FloatTensor(rewards).unsqueeze(1)
        d_t = torch.FloatTensor(dones).unsqueeze(1)

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

class DQNAgent: 
    """
        without Epsilon!
        
        first make random than , make policy
        
    """
    def __init__(self,_policydict=None):       
        self.policy_net = DQN(STATE_SIZE, ACTION_SPACE) # 실제 사용되는 신경망
        self.target_net = DQN(STATE_SIZE, ACTION_SPACE) # 이건 ...
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=1e-3)
        self.memory = deque(maxlen=20000)
        self.gamma = 0.95        
        self.rand_count=0        
        self.batch_size = 64
        self.learn_count = 0
        
    def remember(self, state, action, reward, next_state, done):        
        self.memory.append((state, action, reward, next_state, done))

    def action(self, state):
        #if self.rand_count <= self.batch_size*10:
        #    return random.randrange(ACTION_SPACE)
        #    self.rand_count+=1
        if self.learn_count < 10 :
            return random.randrange(ACTION_SPACE)            
        
        state_t = torch.FloatTensor(state).unsqueeze(0)
        
        with torch.no_grad():
            return torch.argmax(self.policy_net(state_t), dim=1).item()

    def learn(self): # learn
        if len(self.memory) < self.batch_size: 
            return
        self.learn_count +=1
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = map(np.array, zip(*batch))
        
        s_t = torch.FloatTensor(states)
        ns_t = torch.FloatTensor(next_states)
        a_t = torch.LongTensor(actions).unsqueeze(1)
        r_t = torch.FloatTensor(rewards).unsqueeze(1)
        d_t = torch.FloatTensor(dones).unsqueeze(1)

        curr_q = self.policy_net(s_t).gather(1, a_t)
        next_q = self.target_net(ns_t).max(1, keepdim=True)[0]
        target_q = r_t + self.gamma * next_q * (1 - d_t)

        loss = nn.MSELoss()(curr_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())


# ─── TRAINING & INFERENCE ───────────────────────────────────────────────────────
def train(epochs=1000, target_update=300):
    
    env = SnakeEnv(render=True)  # 학습 시 렌더링 OFF (속도 향상)
    
    #agent = DQNAgent(torch.load("snake_dqn.pth"))
    agent = DQNAgent()
    #agent.policy_net.load_state_dict(torch.load("snake_dqn_base1.pth"))#, map_location=agent.device))
    #agent.epsilon = 0.0  # Pure exploitation  
    
    scores = []    
    #print(f"🚀 Training started on {agent.device}")
    for ep in range(1, epochs + 1):
        state = env.reset()         
        #print("x1")
        while True:
            _action = agent.action(state)
            next_state, reward, done, score = env.step(_action)
            agent.remember(state, _action, reward, next_state, done)            
            state = next_state            
            if done: 
                break
            
        agent.learn()        
        scores.append(score)
        if ep % target_update == 0:
            agent.update_target()
        if ep % 50 == 0:
            avg = np.mean(scores[-50:])
            print(f"Ep {ep:4d} | max: x | Avg50: {avg:.2f}", agent.rand_count)
            if avg > 28 :
                break
            
    torch.save(agent.policy_net.state_dict(), "snake_dqn.pth")
    print("✅ Model saved to snake_dqn.pth")
    env.quit()
    

def play():
    model="snake_dqn_base1.pth"
    if not os.path.exists(model):
        print("❌ 학습된 모델이 없습니다. 먼저 train()을 실행하세요.")
        return
    env = SnakeEnv(render=True)
    agent = DQNAgent1()
    agent.policy_net.load_state_dict(torch.load(model))#, map_location=agent.device))
    agent.epsilon = 0.0  # Pure exploitation
    
    print("🎮 Inference Mode - Press ESC to quit")
    state = env.reset()
    for ep in range(1, 50):    
        while True:
            _action = agent.action(state)
            state, _ , done, _ = env.step(_action)
            if done:
                state = env.reset()
                break
    env.quit()

if __name__ == "__main__":
    
    mode = "train"
    if mode == "train":
        train(epochs=5000)
    elif mode == "play":
        play()
    else:
        print("Usage: python snake_dqn.py [train|play]")