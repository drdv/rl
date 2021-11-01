import numpy as np
import gym

from . grid_world import Grid

class GridEnv(gym.Env):
    def __init__(self, grid):
        self.grid = grid
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Dict({
            'x': gym.spaces.Discrete(self.grid.numb_cols),
            'y': gym.spaces.Discrete(self.grid.numb_rows)
        })

        self.counter = 0

    def step(self, action):
        done = self.grid.next_cell(action)
        obs = self.grid.current_cell.center.xy
        reward = self.grid.current_cell.reward

        return obs, reward, done, {}

    def reset(self):
        self.grid.reset()
        return self.grid.current_cell.center.xy

    def render(self, mode='human'):
        """To make the linter happy."""
        raise ValueError('Rendering has been disabled.')

    def __repr__(self):
        return f'GridEnv: {self.grid.position}'
