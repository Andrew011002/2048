import torch
import os
import stable_baselines3 as sb3
from env2 import Env2048

def train(model, timesteps=10000, iters=100, path=None, interval=1):

    dirname = os.path.dirname(path)
    os.makedirs(dirname, exist_ok=True)
    log_name = path.split("/")[-1]

    for i in range(iters):
        model.learn(total_timesteps=timesteps, reset_num_timesteps=False, tb_log_name=log_name, log_interval=interval)
        model.save(f"{path}-{i + 1}")

def retrain(env, timesteps, iters, path):

    dirname = os.path.dirname(path)
    log_name = path.split("/")[-1]
    name, steps = log_name.split('-') 
    model = sb3.PPO.load(path) 
    model.set_env(env, force_reset=True)

    for i in range(iters):
        model.learn(total_timesteps=timesteps, reset_num_timesteps=False, tb_log_name=log_name)
        model.save(f"{dirname}/{name}-{int(steps) + i + 1}")

def simulate(model, env, episodes=1, verbose=False):

    for ep in range(episodes):
        done = False
        obs, info = env.reset() 

        if verbose:
            print(f"Trial: {ep + 1}")
            env.render()

        while not done:
            action, state = model.predict(obs)
            obs, reward, done, truncation, info = env.step(action.item())

            if verbose:
                env.render() 
                print(f'Oberservation: {obs}')
                print(f"Action: {action}\nReward: {reward}") 
                print(f'Info: {info}')

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    env = Env2048(size=4) 
    log_directory = "logs/"
    path = "models/model"
    model = sb3.PPO("MlpPolicy", env, tensorboard_log=log_directory, device=device, verbose=1)
    train(model, timesteps=10000, iters=5000, path=path, interval=5)

if __name__ == "__main__":
    main()