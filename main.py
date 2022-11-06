from maze_generators.backtracking_iterative import BacktrackingIterativeGenerator
from visual.svg_visualize import SVGVisualize

if __name__ == "__main__":
    maze = BacktrackingIterativeGenerator(height=10)
    maze.generate()

    SVGVisualize(maze.maze_grid)
