"""A grid world example (see [Russel_Norvig]_ Chapter 17).

Note
-----
There are four actions: L, R, U, D.

"""
import logging
from enum import Enum
import random
from itertools import product

import matplotlib.pyplot as plt
from matplotlib import patches

log = logging.getLogger(__name__)

DEFAULT_TRANSITION_PROBA = {'R': {'R': .8, 'U': .1, 'D': .1},
                            'L': {'L': .8, 'U': .1, 'D': .1},
                            'U': {'U': .8, 'L': .1, 'R': .1},
                            'D': {'D': .8, 'L': .1, 'R': .1}}

class CellKind(Enum):
    """Grid cell kind."""
    FORBIDDEN = -1
    "Cell cannot be visited."

    STANDARD = 0
    "Standard cell."

    TERMINAL = 1
    "Terminal cell."

class Coordinate:
    """Grid coordinate."""
    def __init__(self, x, y):
        """Initialize instance."""
        self.x, self.y = x, y

    def neighbour(self, direction):
        """Return coordinates of a potential neighbour in a given direction."""
        if direction == 'L': return Coordinate(self.x - 1, self.y)
        if direction == 'R': return Coordinate(self.x + 1, self.y)
        if direction == 'U': return Coordinate(self.x, self.y + 1)
        if direction == 'D': return Coordinate(self.x, self.y - 1)

        raise ValueError(f'Unknown direction {direction}.')

    def is_equal(self, other):
        """Check for equality (I don't want to overload ==)."""
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __repr__(self):
        return f'Coordinate: {self.x}, {self.y}'

class Cell:
    """Define a grid cell."""
    def __init__(self, center=None, reward=0.0, kind=CellKind.STANDARD, color='w'):
        """Initialize instance.

        Parameters
        -----------
        center : :obj:`Coordinate` or ``None``
            Cell center.
        reward : :obj:`float`
            Instantaneous reward.
        kind : :obj:`CellKind`
            Cell type.
        color : :obj:`str`
            Cell color (``None`` to use a default color).

        """
        self._center, self.kind, self.reward = center, kind, reward
        self.color = color
        self.neighbors = {}

    @property
    def center(self):
        """Return cell center."""
        return self._center

    @center.setter
    def center(self, center):
        """Set cell center."""
        self._center = center

    def get_neighbor(self, direction):
        """Return the neighbor in a diven direction."""
        return self.neighbors[direction]

    def set_neighbor(self, direction, cell):
        """Set the neighbor in a diven direction."""
        self.neighbors[direction] = cell

    def __repr__(self):
        """Describe instance."""
        out = f'Cell: {self.kind.name}, reward: {self.reward}, center: {self.center}\n'
        for key, cell in self.neighbors.items():
            out += f'  {key}: {cell.center}, {cell.kind.name} \n'
        return out

    def plot(self, ax):
        """Plot cell.

        Parameters
        ----------
        ax : :obj:`pyplot.axis`
            Axis.

        """
        rect = patches.Rectangle((self.center.x-1/2, self.center.y-1/2), 1, 1,
                                 linewidth=1, edgecolor='b', facecolor=self.color)
        ax.add_patch(rect)

class Grid:
    """Grid."""
    def __init__(self, numb_rows=3, numb_cols=4, fraction_forbidden=0.15,
                 standard_reward=-0.04, goal_reward=1, fail_reward=-1,
                 rand_init=True):
        """Initialize instance."""
        self.numb_rows, self.numb_cols = numb_rows, numb_cols
        self.fraction_forbidden = fraction_forbidden

        self.reward = {
            'standard': standard_reward,
            'goal': goal_reward,
            'fail': fail_reward
        }
        self.cells = []
        self.current_cell, self.previous_cell = None, None
        self._out_of_bounds_cell = Cell(kind=CellKind.FORBIDDEN)

        if rand_init and self.numb_cells > 0:
            self.create_cells()
            self.random_arrangement()
        self.done = False

    @property
    def numb_cells(self):
        return self.numb_rows * self.numb_cols

    @staticmethod
    def grid_4x3():
        """Return the standard 4x3 grid (see Figure 17.1)."""
        grid = Grid(numb_rows=3, numb_cols=4, rand_init=False)
        for x, y in product(range(4), range(3)):
            reward, kind, color = -0.04, CellKind.STANDARD, 'w'
            if x == 1 and y == 1:
                reward, kind, color = 0, CellKind.FORBIDDEN, 'gray'
            if x == 3 and y == 1:
                reward, kind, color = -1, CellKind.TERMINAL, 'red'
            if x == 3 and y == 2:
                reward, kind, color = 1, CellKind.TERMINAL, 'green'

            grid.cells.append(Cell(Coordinate(x=x, y=y), reward, kind, color))

        for cell in grid.cells:
            grid.populate_neighbours(cell)

        return grid

    def create_cells(self):
        """Create the required number of cells."""
        self.cells.append(Cell(kind=CellKind.TERMINAL,
                               reward=self.reward['fail'],
                               color='red'))
        self.cells.append(Cell(kind=CellKind.TERMINAL,
                               reward=self.reward['goal'],
                               color='green'))

        numb_forbidden = (self.numb_cells - 2) * self.fraction_forbidden
        for k in range(self.numb_cells - 2):
            if k < numb_forbidden:
                self.cells.append(Cell(kind=CellKind.FORBIDDEN, color='gray'))
            else:
                self.cells.append(Cell(kind=CellKind.STANDARD,
                                       reward=self.reward['standard']))

    def random_arrangement(self):
        """Arrange cells randomly."""
        rows = random.sample(range(self.numb_rows), self.numb_rows)
        cols = random.sample(range(self.numb_cols), self.numb_cols)
        pairs = list(product(rows, cols))
        random_pairs = random.sample(pairs, len(pairs))

        for cell, (row, col) in zip(self.cells, random_pairs):
            cell.center = Coordinate(x=col, y=row)

        for cell in self.cells:
            self.populate_neighbours(cell)

    def get_cell(self, center):
        """Return cell given its center."""
        for cell in self.cells:
            if cell.center.is_equal(center):
                return cell
        return self._out_of_bounds_cell

    def populate_neighbours(self, cell):
        """Find/set neighbors of a given cell."""
        for direction in ['L', 'R', 'U', 'D']:
            cell.set_neighbor(direction,
                              self.get_cell(cell.center.neighbour(direction)))

    def choose_standard_cell_at_random(self):
        """Return a random standard cell."""
        standard_cells = [cell for cell in self.cells
                          if cell.kind == CellKind.STANDARD]
        return random.choice(standard_cells)

    def set_init_cell(self, center=None):
        """Set which cell is currently occupied."""
        self.previous_cell = None
        if center is None:
            self.current_cell = self.choose_standard_cell_at_random()
        else:
            self.current_cell = self.get_cell(center)

    def next_cell(self, action, transition_proba=None):
        """Move to next cell according to an action."""
        if self.current_cell is None:
            raise ValueError('Set current cell first (set_init_cell).')

        if self.done:
            log.warning('Target state already reached.')
            return self.done

        if transition_proba is None:
            transition_proba = DEFAULT_TRANSITION_PROBA

        seq, proba = zip(*transition_proba[action].items())
        action = random.choices(seq, proba)[0]
        neighbor = self.current_cell.neighbors[action]
        # stay where we are if we bump into a forbidden cell
        self.previous_cell = self.current_cell
        if neighbor.kind != CellKind.FORBIDDEN:
            self.current_cell = neighbor

        self.done = self.current_cell.kind == CellKind.TERMINAL
        return self.done

    def reset(self, center=None):
        """Reset grid state."""
        self.done = False
        self.set_init_cell(center)

    def plot(self, figsize=(15, 8)):
        """Plot grid."""
        plt.figure(figsize=figsize)
        ax = plt.gca()
        for cell in self.cells:
            cell.plot(ax)
            if cell is self.previous_cell:
                ax.plot(cell.center.x, cell.center.y, 'yo', markersize=20, alpha=0.6)
            if cell is self.current_cell:
                ax.plot(cell.center.x, cell.center.y, 'ko')
        plt.axis('equal')
        plt.axis('off')

    def __repr__(self):
        return f'Grid:\n{self.cells}'
