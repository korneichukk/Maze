from string import Template
from collections import namedtuple
import os

CELL_SIZE = 36  # size of each cell in px
HALF = CELL_SIZE / 2
THIRD = CELL_SIZE / 3
QUARTER = CELL_SIZE / 4
THREE_QUARTER = QUARTER * 3

COOR = namedtuple("Coordinate", "x y")


class SVG(object):
    def __init__(
        self,
        stroke_opacity: float = 1,
        stroke_width: float = 2,
        stroke_color: str = "black",
        fill: str = "none",
    ) -> None:
        self.stroke_opacity = stroke_opacity
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill = fill

        self.svg_path = self.path()
        self.d = ""

    def path(self) -> Template:
        return Template(
            f"""
                <path 
                    stroke-opacity="{self.stroke_opacity}" 
                    stroke-width="{self.stroke_width}" 
                    stroke="{self.stroke_color}" 
                    fill="{self.fill}" 
                    d="$d"
                />
            """
        )


class SVGCell(SVG):
    def __init__(
        self,
        col_id: int,
        row_id: int,
        cell_type: str,
        stroke_opacity: float = 1,
        stroke_width: float = 2,
        stroke_color: str = "black",
        fill: str = "none",
    ) -> None:
        super().__init__(stroke_opacity, stroke_width, stroke_color, fill)

        self.coor = COOR(x=col_id, y=row_id)
        self.type = cell_type

        # left upper corner coordinate
        self.luc = COOR(x=col_id * CELL_SIZE, y=row_id * CELL_SIZE)

    def d_m(self, x_shift: float, y_shift: float):
        self.d += f"M {self.luc.x + x_shift},{self.luc.y + y_shift} \n"

    def d_l(self, x_shift: float, y_shift: float):
        self.d += f"L {self.luc.x + x_shift},{self.luc.y + y_shift} \n"

    def d_c(
        self,
        x_start_curve_shift: float,
        y_start_curve_shift: float,
        x_end_curve_shift: float,
        y_end_curve_shift: float,
        x_end_shift: float,
        y_end_shift: float,
    ):
        self.d += (
            f"C {self.luc.x + x_start_curve_shift},{self.luc.y + y_start_curve_shift}"
            f" {self.luc.x + x_end_curve_shift},{self.luc.y + y_end_curve_shift}"
            f" {self.luc.x + x_end_shift},{self.luc.y + y_end_shift}\n"
        )

    def d_a(
        self,
        rx: float,
        ry: float,
        angle: float,
        large_arc_flag: int,
        sweep_flag: int,
        x_end_shift: float,
        y_end_shift: float,
    ):
        self.d += (
            f"A {rx} {ry}"
            f" {angle} {large_arc_flag} {sweep_flag}"
            f" {self.luc.x + x_end_shift},{self.luc.y + y_end_shift}\n"
        )


class SVGWall(SVGCell):
    def render(self):
        if self.type == "L":
            self.type_L()

        return self.svg_path.substitute(d=self.d)

    def type_L(self):
        """
        L: ──┐
           ──┘
        """

        self.d_m(x_shift=0, y_shift=QUARTER)
        self.d_c(
            x_start_curve_shift=QUARTER,
            y_start_curve_shift=QUARTER,
            x_end_curve_shift=THIRD,
            y_end_curve_shift=QUARTER / 2,
            x_end_shift=HALF,
            y_end_shift=QUARTER / 2,
        )
        self.d_a(
            rx=THREE_QUARTER / 2,
            ry=THREE_QUARTER / 2,
            angle=0,
            large_arc_flag=0,
            sweep_flag=1,
            x_end_shift=HALF,
            y_end_shift=QUARTER * 7 / 2,
        )

        self.d_m(x_shift=0, y_shift=THREE_QUARTER)
        self.d_c(
            x_start_curve_shift=QUARTER,
            y_start_curve_shift=THREE_QUARTER,
            x_end_curve_shift=THIRD,
            y_end_curve_shift=QUARTER * 7 / 2,
            x_end_shift=HALF,
            y_end_shift=QUARTER * 7 / 2,
        )


def SVGVisualize(maze_grid):
    BASE_SVG = Template(
        """
        <svg   
            viewBox="0 0 $view_box $view_box" 
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink" 
            height="$height" 
            width="$width"
        >
            $body
        </svg>
    """
    )

    svg_cells = ""

    for row in maze_grid:
        svg_cells += "".join(
            [
                SVGWall(
                    col_id=cell.x,
                    row_id=cell.y,
                    cell_type=cell.type or cell.cell_type(),
                ).render()
                for cell in row
            ]
        )

    PATH = os.path.join(
        os.path.realpath(os.path.dirname(__file__)),
        "svg_mazes",
    )

    os.makedirs(PATH, exist_ok=True)

    PATH = os.path.join(PATH, f"{len(maze_grid)}*{len(maze_grid[0])}.svg")

    with open(PATH, "w") as file:
        file.write(
            BASE_SVG.substitute(
                view_box=max(len(maze_grid), len(maze_grid[0])) * CELL_SIZE,
                height=len(maze_grid) * CELL_SIZE,
                width=len(maze_grid[0]) * CELL_SIZE,
                body=svg_cells,
            )
        )
