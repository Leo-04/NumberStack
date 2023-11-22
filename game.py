from random import randint as rand
import json


class GameState:
    width: int
    height: int
    score: int
    grid: list[int]

    def __init__(self, width, height, score, grid):
        """Creates a game state"""
        
        self.width = width
        self.height = height
        self.score = score
        self.grid = grid

    def to_json(self) -> str:
        """Converts the game state into a json string"""


        return json.dumps({
            "width": self.width,
            "height": self.height,
            "score": self.score,
            "grid": self.grid
        }, indent=4)

    def from_json(self, json_str: str):
        """Converts a json string into a game state"""
        
        data = json.loads(json_str)
        self.width = data["width"]
        self.height = data["height"]
        self.score = data["score"]
        self.grid = data["grid"]

    @property
    def grid_size(self):
        return self.width * self.height

    @property
    def max_number(self):
        return max(self.grid)


class Game:
    state: GameState

    def __init__(self, state: GameState):
        self.state = state

    def get_combine_indexes(self, value: any) -> list[int]:
        """Gets the indexes of the grid with the same value"""
        
        indexes = []

        for i in range(self.state.grid_size):
            if self.state.grid[i] == value:
                indexes.append(i)

        return indexes

    def is_gameover(self):
        """Checks if there are no possible moves left"""

        # Check for zeros
        if any(i == 0 for i in self.state.grid):
            return False
        
        # Check if any combinations are left
        return all([
            len(self.get_combine_indexes(i)) <= 1
            for i in self.state.grid[:-1]
        ]) and len(
            self.get_combine_indexes(self.state.grid[-1])
        ) < 1

    def combine(self, index1, index2) -> int:
        """
        Combines 2 index together,
        the value is combined to index2,
        returns negitive on error
        """
        
        if index1 == index2:
            return -1
        elif (self.state.grid[index1] == self.state.grid[index2]) and self.state.grid[index1] > 0:
            self.state.grid[index2] += 1
            self.state.grid[index1] = 0
            self.state.score += 1
        elif self.state.grid[index2] == 0:
            self.state.grid[index2] = self.state.grid[index1]
            self.state.grid[index1] = 0
        else:
            return -2

        if index1 == self.state.grid_size:
            self.next_number()

    def load_state(self, state):
        self.state = state

    def next_number(self):
        """Genreates the next number and put it at the last index"""
        
        self.state.grid[self.state.grid_size] = (
            1
            if (self.state.grid_size < 2)
            else (rand(1, self.state.max_number + 1))
        )
