import os
import stable_baselines3 as sb3
from env2 import Env2048

# trains model over certain amount of time steps, logs after n time steps, does this N iterations
def train(model, log_name, timesteps=10000, iters=100, save_directory=None):

    os.makedirs(save_directory, exist_ok=True)
    path = os.path.join(save_directory, log_name)

    for i in range(iters):
        model.learn(total_timesteps=timesteps, reset_num_timesteps=False, tb_log_name=log_name)
        model.save(f"{path}-{i + 1}")

# for retraining an already trained model
def retrain(env, log_name, timesteps, iters):
    name, steps = log_name.split('-') # get name of model, time steps
    model = sb3.PPO.load(f'models/{log_name}') # load model
    model.set_env(env, force_reset=True)

    # retrain the model (continuing from previous)
    for i in range(iters):
        model.learn(total_timesteps=timesteps, reset_num_timesteps=False, tb_log_name=log_name)
        model.save(f"models/{name}-{int(steps) + i + 1}")

def simulate(model, env, episodes=1, verbose=False):

    # create new sim for n episodes
    for ep in range(episodes):
        done = False
        obs, info = env.reset() # init

        # show info & env
        if verbose:
            print(f"Trial: {ep + 1}")
            env.render()

        # run sim until the agent is done (fails or wins)
        while not done:

            # predict based on env, then update env
            action, state = model.predict(obs)
            obs, reward, done, truncation, info = env.step(action.item())

            # show info & env
            if verbose:
                env.render() # show action made
                print(f'Oberservation: {obs}')
                print(f"Action: {action}\nReward: {reward}") # info
                print(f'Info: {info}')

def main():
    # Enviornment
    env = Env2048(size=4) # 4x4 2048 env

    # TRAINING
    # model = sb3.DQN("MlpPolicy", env, verbose=1, tensorboard_log="logs/") # Proximal Policy Optimization Algorithm
    # train(model, log_name="Agent", timesteps=10000, iters=5000, save_directory="models") # 50 million runs in the game
    
    # RETRAINING
    # ppo = sb3.PPO.load("models/ppo_4x4-100x10^4")
    # retrain(env, "ppo-6824", timesteps=10000, iters=5000)

    # SIMULATING
    tag = 1
    model = sb3.DQN.load(f"models/Agent-{tag}")
    simulate(model, env, episodes=1, verbose=True)

if __name__ == "__main__":
    main()