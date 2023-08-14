import time
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from grid import Grid
from stable_baselines3.common.env_checker import check_env

class Env2048(gym.Env):

    def __init__(self, size=4, dtype=np.float32, eps=1e-9):
        super(Env2048, self).__init__()
        self.size = size
        self.dtype = dtype
        self.eps = eps
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=1, shape=(size * size,), dtype=dtype)

    def step(self, action):
        mappings = {0: "left", 1: "right", 2: "up", 3: "down"}
        direction = mappings[action]
        reward = self.move(direction)
        done = self.game_over()
        self.observation = self.reshape_and_normalize(self.grid)
        self.info = {"reward": reward, "done": done}
        return self.observation, reward, done, False, self.info

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.grid = Grid(size=self.size)
        self.observation = self.reshape_and_normalize(self.grid)
        self.info = {"reward": 0, "done": False}
        return self.observation, self.info
    
    def move(self, direction):
        score, moves, points, moved = self.grid.move(direction)
        reward = self.calculate_reward(score, moves, points, moved)
        return reward
    
    def reshape_and_normalize(self, grid):
        z = grid.numpy().flatten() + self.eps
        scaled = z / np.linalg.norm(z)
        return scaled.astype(self.dtype)
    
    def calculate_reward(self, score, moves, points, moved):
        if not moved:
            return 0
        reward = (score + moves) / 1000 * points
        return reward
    
    def game_over(self):
        return self.grid.game_over()

    def numpy(self):
        return self.grid.numpy()
    
    def score(self):
        return self.grid.score
    
    def moves(self):
        return self.grid.moves
    
    def render(self, mode="console"):
        if mode != "console":
            raise NotImplementedError("Mode not supported")
        print(self.grid)
        
def simulate(env, episodes=100):

    for _ in range(episodes):

        net_reward = 0
        done = False 
        obs = env.reset() 
        env.render()

        while not done:

            action = env.action_space.sample()
            print(f"Observation: {list(obs)}")
            obs, reward, done, truncated, info = env.step(action)
            print(f"Action: {'left' if not action else 'right' if action == 1 else 'up' if action == 2 else 'down'}")
            print(f"Reward {reward}")
            print(f"Info: {info}")
            print("Resultant Grid:")
            env.render()
            net_reward += reward

        print(f"Net Reward: {net_reward}")

def main():

    np.set_printoptions(linewidth=100)
    env = Env2048(dtype=np.float16) 

    check_env(env) 
    simulate(env, episodes=1)

if __name__ == "__main__":
    main()