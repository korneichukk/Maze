import random

from .maze import Maze


class BacktrackingIterativeGenerator:
    def __init__(self, maze_height: int = 20, maze_width: int = 20) -> None:
        self.maze = Maze(height=maze_height, width=maze_width)

        # start point is left upper corner
        self.start_from = self.maze.maze_grid[0][0]

        self.stack = []

    def generate(self):
        self.stack.append(self.start_from)
        self.start_from.visited = True

        while self.stack:
            current_cell: Maze.Cell = self.stack.pop()

            # get possible moves among not visited neighbours
            possible_moves = [
                (dirr, neighbour)
                for dirr, neighbour in current_cell.neighbours.items()
                if neighbour and not neighbour.visited
            ]

            if not possible_moves:
                continue

            # if there are possible moves push current cell back into the stack
            self.stack.append(current_cell)

            # choose one of possible moves
            move = random.choice(possible_moves)

            # push new cell into stack
            self.stack.append(move[1])
            move[1].visited = True

            # remove walls between cells
            current_cell.walls[move[0]] = False
            move[1].walls[Maze.Cell.OPPOSITE_DIR[move[0]]] = False
