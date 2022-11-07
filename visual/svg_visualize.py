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

        if self.type == "R":
            self.type_R()

        if self.type == "U":
            self.type_U()

        if self.type == "D":
            self.type_D()

        if self.type == "LR":
            self.type_LR()

        if self.type == "LU":
            self.type_LU()

        if self.type == "LD":
            self.type_LD()

        if self.type == "RU":
            self.type_RU()

        if self.type == "RD":
            self.type_RD()

        if self.type == "UD":
            self.type_UD()

        if self.type == "LRU":
            self.type_LRU()

        if self.type == "LRD":
            self.type_LRD()

        if self.type == "LUD":
            self.type_LUD()

        if self.type == "RUD":
            self.type_RUD()

        if self.type == "LRUD":
            self.type_LRUD()

        return self.svg_path.substitute(d=self.d)

    def luc_wall(self):
        # making ┘ left upper corner
        self.d_m(x_shift=0, y_shift=QUARTER)
        self.d_a(
            rx=QUARTER,
            ry=QUARTER,
            angle=0,
            large_arc_flag=0,
            sweep_flag=0,
            x_end_shift=QUARTER,
            y_end_shift=0,
        )

    def ruc_wall(self):
        # making └ rigth upper corner
        self.d_m(x_shift=THREE_QUARTER, y_shift=0)
        self.d_a(
            rx=QUARTER,
            ry=QUARTER,
            angle=0,
            large_arc_flag=0,
            sweep_flag=0,
            x_end_shift=CELL_SIZE,
            y_end_shift=QUARTER,
        )

    def llc_wall(self):
        # making ┐ left lower corner
        self.d_m(x_shift=0, y_shift=THREE_QUARTER)
        self.d_a(
            rx=QUARTER,
            ry=QUARTER,
            angle=0,
            large_arc_flag=0,
            sweep_flag=1,
            x_end_shift=QUARTER,
            y_end_shift=CELL_SIZE,
        )

    def rlc_wall(self):
        # making ┌ rigth lower corner
        self.d_m(x_shift=THREE_QUARTER, y_shift=CELL_SIZE)
        self.d_a(
            rx=QUARTER,
            ry=QUARTER,
            angle=0,
            large_arc_flag=0,
            sweep_flag=1,
            x_end_shift=CELL_SIZE,
            y_end_shift=THREE_QUARTER,
        )

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

    def type_R(self):
        """
        R: ┌──
           └──
        """

        self.d_m(x_shift=CELL_SIZE, y_shift=QUARTER)
        self.d_c(
            x_start_curve_shift=THREE_QUARTER,
            y_start_curve_shift=QUARTER,
            x_end_curve_shift=THIRD * 2,
            y_end_curve_shift=QUARTER / 2,
            x_end_shift=HALF,
            y_end_shift=QUARTER / 2,
        )

        self.d_a(
            rx=THREE_QUARTER / 2,
            ry=THREE_QUARTER / 2,
            angle=0,
            large_arc_flag=0,
            sweep_flag=0,
            x_end_shift=HALF,
            y_end_shift=QUARTER * 7 / 2,
        )

        self.d_m(x_shift=CELL_SIZE, y_shift=THREE_QUARTER)
        self.d_c(
            x_start_curve_shift=THREE_QUARTER,
            y_start_curve_shift=THREE_QUARTER,
            x_end_curve_shift=THIRD * 2,
            y_end_curve_shift=QUARTER * 7 / 2,
            x_end_shift=HALF,
            y_end_shift=QUARTER * 7 / 2,
        )

    def type_U(self):
        """
        U: │ │
           └─┘
        """
        self.d_m(x_shift=QUARTER, y_shift=0)
        self.d_c(
            x_start_curve_shift=QUARTER,
            y_start_curve_shift=QUARTER,
            x_end_curve_shift=QUARTER / 2,
            y_end_curve_shift=THIRD,
            x_end_shift=QUARTER / 2,
            y_end_shift=HALF,
        )

        self.d_a(
            rx=THREE_QUARTER / 2,
            ry=THREE_QUARTER / 2,
            angle=0,
            large_arc_flag=0,
            sweep_flag=0,
            x_end_shift=QUARTER * 7 / 2,
            y_end_shift=HALF,
        )

        self.d_m(x_shift=THREE_QUARTER, y_shift=0)
        self.d_c(
            x_start_curve_shift=THREE_QUARTER,
            y_start_curve_shift=QUARTER,
            x_end_curve_shift=QUARTER * 7 / 2,
            y_end_curve_shift=THIRD,
            x_end_shift=QUARTER * 7 / 2,
            y_end_shift=HALF,
        )

    def type_D(self):
        """
        D: ┌─┐
           │ │
        """
        self.d_m(x_shift=QUARTER, y_shift=CELL_SIZE)
        self.d_c(
            x_start_curve_shift=QUARTER,
            y_start_curve_shift=THREE_QUARTER,
            x_end_curve_shift=QUARTER / 2,
            y_end_curve_shift=THIRD * 2,
            x_end_shift=QUARTER / 2,
            y_end_shift=HALF,
        )

        self.d_a(
            rx=THREE_QUARTER / 2,
            ry=THREE_QUARTER / 2,
            angle=0,
            large_arc_flag=0,
            sweep_flag=1,
            x_end_shift=QUARTER * 7 / 2,
            y_end_shift=HALF,
        )

        self.d_m(x_shift=THREE_QUARTER, y_shift=CELL_SIZE)
        self.d_c(
            x_start_curve_shift=THREE_QUARTER,
            y_start_curve_shift=THREE_QUARTER,
            x_end_curve_shift=QUARTER * 7 / 2,
            y_end_curve_shift=THIRD * 2,
            x_end_shift=QUARTER * 7 / 2,
            y_end_shift=HALF,
        )

    def type_LR(self):
        """
        LR: ───
            ───
        """
        # making horizontal upper line
        self.d_m(x_shift=0, y_shift=QUARTER)
        self.d_l(x_shift=CELL_SIZE, y_shift=QUARTER)

        # making horizontal lower line
        self.d_m(x_shift=0, y_shift=THREE_QUARTER)
        self.d_l(x_shift=CELL_SIZE, y_shift=THREE_QUARTER)

    def type_LU(self):
        """
        LU: ┘ │
            ──┘
        """

        self.luc_wall()

        # making    │
        #        ──┘
        self.d_m(x_shift=0, y_shift=THREE_QUARTER)
        self.d_a(
            rx=THREE_QUARTER,
            ry=THREE_QUARTER,
            angle=0,
            large_arc_flag=0,
            sweep_flag=0,
            x_end_shift=THREE_QUARTER,
            y_end_shift=0,
        )

    def type_LD(self):
        """
        LD: ──┐
            ┐ │
        """

        # making ┐ left lower corner
        self.llc_wall()

        # making   ──┐
        #           │
        self.d_m(x_shift=0, y_shift=QUARTER)
        self.d_a(
            rx=THREE_QUARTER,
            ry=THREE_QUARTER,
            angle=0,
            large_arc_flag=0,
            sweep_flag=1,
            x_end_shift=THREE_QUARTER,
            y_end_shift=CELL_SIZE,
        )

    def type_RU(self):
        """
        RU: │ └
            └──
        """

        # making └ rigth upper corner
        self.ruc_wall()

        # making │
        #       └──
        self.d_m(x_shift=QUARTER, y_shift=0)
        self.d_a(
            rx=THREE_QUARTER,
            ry=THREE_QUARTER,
            angle=0,
            large_arc_flag=0,
            sweep_flag=0,
            x_end_shift=CELL_SIZE,
            y_end_shift=THREE_QUARTER,
        )

    def type_RD(self):
        """
        RU: ┌──
            │ ┌
        """

        # making ┌ rigth lower corner
        self.rlc_wall()

        # making │
        #       └──
        self.d_m(x_shift=QUARTER, y_shift=CELL_SIZE)
        self.d_a(
            rx=THREE_QUARTER,
            ry=THREE_QUARTER,
            angle=0,
            large_arc_flag=0,
            sweep_flag=1,
            x_end_shift=CELL_SIZE,
            y_end_shift=QUARTER,
        )

    def type_UD(self):
        """
        UD: │ │
            │ │
        """

        # making vertical left line
        self.d_m(x_shift=QUARTER, y_shift=0)
        self.d_l(x_shift=QUARTER, y_shift=CELL_SIZE)

        # making vertical right line
        self.d_m(x_shift=THREE_QUARTER, y_shift=0)
        self.d_l(x_shift=THREE_QUARTER, y_shift=CELL_SIZE)

    def type_LRU(self):
        """
        LRU: ┘ └
             ───
        """
        # making ┘ left upper corner
        self.luc_wall()

        # making └ rigth upper corner
        self.ruc_wall()

        # making horizontal lower line
        self.d_m(x_shift=0, y_shift=THREE_QUARTER)
        self.d_l(x_shift=CELL_SIZE, y_shift=THREE_QUARTER)

    def type_LRD(self):
        """
        LRD: ───
             ┐ ┌
        """
        # making ┐ left lower corner
        self.llc_wall()

        # making ┌ rigth lower corner
        self.rlc_wall()

        # making horizontal upper line
        self.d_m(x_shift=0, y_shift=QUARTER)
        self.d_l(x_shift=CELL_SIZE, y_shift=QUARTER)

    def type_LUD(self):
        """
        LUD: ┘ │
             ┐ │
        """
        # making ┘ left upper corner
        self.luc_wall()

        # making ┐ left lower corner
        self.llc_wall()

        # making vertical right line
        self.d_m(x_shift=THREE_QUARTER, y_shift=0)
        self.d_l(x_shift=THREE_QUARTER, y_shift=CELL_SIZE)

    def type_RUD(self):
        """
        RUD: │ └
             │ ┌
        """
        # making └ rigth upper corner
        self.ruc_wall()

        # making ┌ rigth lower corner
        self.rlc_wall()

        # making vertical left line
        self.d_m(x_shift=QUARTER, y_shift=0)
        self.d_l(x_shift=QUARTER, y_shift=CELL_SIZE)

    def type_LRUD(self):
        """
        LRUD: ┘ └
              ┐ ┌
        """

        # making ┘ left upper corner
        self.luc_wall()

        # making └ rigth upper corner
        self.ruc_wall()

        # making ┐ left lower corner
        self.llc_wall()

        # making ┌ rigth lower corner
        self.rlc_wall()


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
