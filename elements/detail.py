from .column import RectangularColumn
from .rebar import Rebar

class Detail:
    def __init__(self, name: str, column: RectangularColumn, rebar_list: list[Rebar]):
        self.name = name
        self.column = column
        self.rebar_list = rebar_list