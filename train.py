import torch
import os
import stable_baselines3 as sb3
from env2 import Env2048
from argparse import ArgumentParser

def train(model, timesteps=10000, iters=100,  save_path=None, log_name=None, log_interval=1):

    dirname = os.path.dirname(save_path)
    os.makedirs(dirname, exist_ok=True)

    for i in range(iters):
        model.learn(total_timesteps=timesteps, reset_num_timesteps=False, tb_log_name=log_name, log_interval=log_interval)
        model.save(f"{save_path}-{i + 1}")

def retrain(model, timesteps, iters, load_path, log_name):

    dirname = os.path.dirname(load_path)
    name, steps = os.path.basename(load_path).replace(".zip", "").split("-")

    for i in range(iters):
        model.learn(total_timesteps=timesteps, reset_num_timesteps=False, tb_log_name=log_name)
        model.save(f"{dirname}/{name}-{int(steps) + i + 1}")

def simulate(model, env, episodes=1, verbose=False):

    for episode in range(episodes):
        done = False
        observation, info = env.reset() 

        if verbose:
            print(f"Trial: {episode + 1}")
            env.render()

        while not done:
            action, state = model.predict(observation)
            observation, reward, done, truncation, info = env.step(action.item())

            if verbose:
                print(f"{'-' * 20}\nResults\n{'-' * 20}")
                env.render() 
                print(f"Oberservation: {list(observation)}\nAction: {action}\nReward: {reward}\nInfo: {info}") 

def main():

    parser = ArgumentParser(description="Determine whether to train, retrain, or simulate a model")
    parser.add_argument("--path", type=str, help="Path for models (saving or loading).", default="models/model")
    subpasrers = parser.add_subparsers(title="commands", dest="command")
    subpasrers.add_parser(name="train", help="Command for training a model.")
    subpasrers.add_parser(name="retrain", help="Command for retraining a model.")
    subpasrers.add_parser(name="simulate", help="Command for simulating a model.")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    env = Env2048(size=4) 
    timesteps = 10000
    iterations = 5000
    log_intervals = 5
    args = parser.parse_args()
    path = args.path

    if args.command == "train":
        log_name = "logs"
        model = sb3.DQN("MlpPolicy", env, tensorboard_log=log_name, device=device, verbose=1)
        train(model, timesteps=timesteps, iters=iterations, save_path=path, log_name=log_name, log_interval=log_intervals)

    elif args.command == "retrain":
        log_name = "logs"
        model = sb3.DQN.load(path, env, device=device, print_system_info=True)
        retrain(model, timesteps=timesteps, iters=iterations, log_name=log_name, load_path=path)

    elif args.command == "simulate":
        episodes = 1
        model = sb3.DQN.load(path, env, device=device, print_system_info=True)
        simulate(model, env, episodes, verbose=1)

if __name__ == "__main__":
    main()