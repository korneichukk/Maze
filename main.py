from maze_generators.backtracking_iterative import BacktrackingIterativeGenerator
from visual.text_visualize import visualize

if __name__ == "__main__":
    maze = BacktrackingIterativeGenerator(height=10)
    maze.generate()

    visualize(maze.maze_grid, show_cli=False, export=True)
