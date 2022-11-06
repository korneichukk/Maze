from maze_generators.backtracking_iterative import BacktrackingIterativeGenerator
from visual.text_visualize import visualize

if __name__ == "__main__":
    maze = BacktrackingIterativeGenerator()
    maze.generate()

    visualize(maze.maze, show_cli=False, export=True)
