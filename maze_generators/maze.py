from typing import Dict


class Maze(object):
    """Class represents the whole maze"""

    class Cell:
        """Class represents the specific cell"""

        OPPOSITE_DIR = {
            "L": "R",
            "R": "L",
            "U": "D",
            "D": "U",
        }

        def __init__(self, col_id: int, row_id: int) -> None:
            self.x = col_id
            self.y = row_id
            self.type = ""

            self.visited = False
            self.neighbours: Dict[str, Maze.Cell or None] = {
                "L": None,
                "R": None,
                "U": None,
                "D": None,
            }
            self.walls = {
                "L": True,
                "R": True,
                "U": True,
                "D": True,
            }

        def cell_type(self):
            """Function returns string with possible directions to move from given cell
               in ordered manner (L-R-U-D)

            Returns:
                str: string with directions where you can move
                    example:
                        "L": ──┐
                             ──┘

                        "RUD": │ └
                               │ ┌
            """
            self.type = "".join([dirr for dirr, wall in self.walls.items() if not wall])
            return self.type

    def __init__(self, height: int = 20, width: int = 20) -> None:
        self.height = height
        self.width = width

        # populate grid with cells
        self.maze_grid = [
            [Maze.Cell(col_id=col_id, row_id=row_id) for col_id in range(self.width)]
            for row_id in range(self.height)
        ]

        # calculates a new cell coordinates after the move
        self.directions = {
            "L": lambda x, y: (x - 1, y),
            "R": lambda x, y: (x + 1, y),
            "U": lambda x, y: (x, y - 1),
            "D": lambda x, y: (x, y + 1),
        }

        # populate the neighbours for each cell
        self.fill_cell_neighbours()

    def fill_cell_neighbours(self):
        """Function parse through each cell and assigns neighbour cells for each direction"""
        for row_id, row in enumerate(self.maze_grid):
            for col_id, cell in enumerate(row):
                for dirr, shift in self.directions.items():
                    neighbour_coor = shift(col_id, row_id)

                    # drop if possible neighbour is out of bounds
                    if (
                        neighbour_coor[0] < 0
                        or neighbour_coor[0] >= self.width
                        or neighbour_coor[1] < 0
                        or neighbour_coor[1] >= self.height
                    ):
                        continue

                    cell.neighbours[dirr] = self.maze_grid[neighbour_coor[1]][
                        neighbour_coor[0]
                    ]
