import numpy as np
import gym

from . grid_world import Grid

ACTIONS = {0: 'L', 1: 'R', 2: 'U', 3: 'D'}

class GridEnv(gym.Env):
    def __init__(self, grid, max_count=100):
        self.grid = grid
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Dict({
            'x': gym.spaces.Discrete(self.grid.numb_cols),
            'y': gym.spaces.Discrete(self.grid.numb_rows)
        })

        self.counter = 0
        self.max_count = max_count

    def step(self, action):

        done = self.grid.next_cell(ACTIONS[action])
        obs = {'x': self.grid.current_cell.center.x,
               'y': self.grid.current_cell.center.y}
        reward = self.grid.current_cell.reward

        self.counter += 1
        if self.counter > self.max_count:
            done = True

        return obs, reward, done, {}

    def reset(self):
        self.grid.reset()
        return {'x': self.grid.current_cell.center.x,
                'y': self.grid.current_cell.center.y}

    def render(self, mode='human'):
        """To make the linter happy."""
        raise ValueError('Rendering has been disabled.')

    def __repr__(self):
        return f'GridEnv'
