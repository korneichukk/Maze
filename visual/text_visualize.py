import os

"""
CELL TYPES:
    L: ──┐
       ──┘
    R: ┌──
       └──
    U: │ │
       └─┘
    D: ┌─┐
       │ │
    LR: ───
        ───
    LU: ┘ │
        ──┘
    LD: ──┐
        ┐ │
    RU: │ └
        └──
    RD: ┌──
        │ ┌
    UD: │ │
        │ │
    LRU: ┘ └
         ───
    LRD: ───
         ┐ ┌
    LUD: ┘ │
         ┐ │
    RUD: │ └
         │ ┌
    LRUD: ┘ └
          ┐ ┌
"""

CELL_TYPES = {
    "L": ("──┐", "──┘"),
    "R": ("┌──", "└──"),
    "U": ("│ │", "└─┘"),
    "D": ("┌─┐", "│ │"),
    "LR": ("───", "───"),
    "LU": ("┘ │", "──┘"),
    "LD": ("──┐", "┐ │"),
    "RU": ("│ └", "└──"),
    "RD": ("┌──", "│ ┌"),
    "UD": ("│ │", "│ │"),
    "LRU": ("┘ └", "───"),
    "LRD": ("───", "┐ ┌"),
    "LUD": ("┘ │", "┐ │"),
    "RUD": ("│ └", "│ ┌"),
    "LRUD": ("┘ └", "┐ ┌"),
}


def visualize(maze, show_cli: bool = True, export: bool = False):
    assert maze

    text_maze = ""

    for row in maze.maze_grid:
        row_cell_types = [cell.cell_type() for cell in row]
        text_maze += "".join([CELL_TYPES[cell_type][0] for cell_type in row_cell_types])
        text_maze += "\n"
        text_maze += "".join([CELL_TYPES[cell_type][1] for cell_type in row_cell_types])
        text_maze += "\n"

    if show_cli:
        print(text_maze.strip())

    if export:
        PATH = os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "text_mazes",
        )

        os.makedirs(PATH, exist_ok=True)

        PATH = os.path.join(PATH, f"{len(maze.maze_grid)}*{len(maze.maze_grid[0])}.txt")

        with open(PATH, "w") as file:
            file.write(text_maze.strip())
