import os
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from grid import Grid
from stable_baselines3.common.env_checker import check_env
from threading import Thread

class Env2048(gym.Env):

    def __init__(self, size=4, dtype=np.float32, eps=1e-9):
        super(Env2048, self).__init__()
        self.size = size
        self.dtype = dtype
        self.eps = eps
        self.reward_range = (-1, 1)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=1, shape=(size * size,), dtype=dtype)
        self.gui = None

    def step(self, action):
        mappings = {0: "left", 1: "right", 2: "up", 3: "down"}
        direction = mappings[action]
        reward = self.move(direction)
        done = self.game_over()
        self.observation = self.reshape_and_normalize(self.grid)
        self.info = {"reward": reward, "done": done, "score": self.score(), "moves": self.moves(), "points": self.points()}
        return self.observation, reward, done, False, self.info

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.grid = Grid(size=self.size)
        self.observation = self.reshape_and_normalize(self.grid)
        self.info = {"reward": 0, "done": False, "score": 0, "moves": 0, "points": 0}
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
            return -1

        scale = 1/ (1 + np.exp(-points / 1024))
        shift = 1 / (1 + moves)
        base = self.normalize_scalar(score, 0, 25000)

        reward = base * scale + shift
        return reward
    
    def normalize_scalar(self, value, low, high, eps=1e-9):
        scaled = (value - low) / (high - low) + eps
        return scaled
        
    def game_over(self):
        return self.grid.game_over()

    def numpy(self):
        return self.grid.numpy()
    
    def score(self):
        return self.grid.score
    
    def moves(self):
        return self.grid.moves
    
    def points(self):
        return self.grid.points
    
    def render(self, mode="console"):
        if mode != "console":
            raise NotImplementedError("Mode not supported")
        print(self.grid)
        
def simulate(env, episodes=100, store_result=False, verbose=True):

    for _ in range(episodes):

        net_reward = 0
        done = False 
        obs = env.reset() 

        if verbose:
            env.render()

        while not done:

            action = env.action_space.sample()
            obs, reward, done, truncated, info = env.step(action)
            net_reward += reward

            if verbose:
                print(f"Observation: {list(obs)}")
                print(f"Action: {'left' if not action else 'right' if action == 1 else 'up' if action == 2 else 'down'}")
                print(f"Reward {reward}")
                print(f"Info: {info}")
                print("Resultant Grid:")
                env.render()

        if verbose:
            print(f"Net Reward: {net_reward}")    

        if store_result:
            dirname = os.path.dirname(__file__)
            max_tile = np.max(env.numpy())
            os.makedirs(f"{dirname}/game_data", exist_ok=True)
            path = os.path.join(dirname, f"{'game_data'}/data.txt")
            with open(path, mode="a", encoding="utf-8") as file:
                file.write(f"Max Tile: {int(max_tile)} Info: {info} Net Reward: {net_reward}\n")

def run_simulations(workers=10, episodes=100):

    threads = []

    for _ in range(workers):
        env = Env2048()
        thread = Thread(target=simulate, args=(env, episodes, True, False))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def main():

    np.set_printoptions(linewidth=100)
    env = Env2048(dtype=np.float16) 

    check_env(env) 
    # simulate(env, episodes=1000, store_result=True)

    run_simulations(workers=10, episodes=100)

if __name__ == "__main__":
    main()