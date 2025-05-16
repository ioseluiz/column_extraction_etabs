from .rebar import Rebar
from .stirrup import Stirrup

class Arc:
    def __init__(self, center_point: tuple[int], radius: int, start_angle: int, end_angle: int):
        self.center_point = center_point
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

class RectangularColumn:
    def __init__(self, width: int, height: int, fc: str, number_of_bars: int, rebar_type: str, r2_bars: int, r3_bars: int, stirrup_type: str, cover: float):
        self.width = width # mm
        self.height = height # mm
        self.number_of_bars = number_of_bars
        self.rebar_type = rebar_type # Example: #3, #4...#14
        self.r2_bars = r2_bars # Long Direction (Height)
        self.r3_bars = r3_bars # Short Direction (Width)
        self.stirrup_type = stirrup_type
        self.cover = cover # cover in mm
        self.main_stirrup = self.set_stirrup()
        self.rebars = []
        
        


    def set_origin_point(self,  origin_point: tuple[int]):
        self.origin= origin_point # tuple (x,y)

    def get_column_coordinates(self):
        self.coordinates = self.set_column_coordinates() # list of tuples (x,y)

    def set_stirrup(self):
        return Stirrup(self.stirrup_type)
 

    def set_column_coordinates(self):
        coordinates = (
            (self.origin[0], self.origin[1]),
            (self.origin[0] + self.width, self.origin[1]),
            (self.origin[0] + self.width, self.origin[1] - self.height),
            (self.origin[0], self.origin[1] - self.height),
            (self.origin[0], self.origin[1])
        )

        return coordinates
    
    def set_rebar_r2_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        r2_spacing = (self.height - 2 * self.cover - 2 *self.main_stirrup.diameter - rebar.diameter )/(self.r2_bars-1)
        start_x = self.origin[0] + self.cover + self.main_stirrup.diameter + rebar.diameter/2
        start_y = self.origin[1] - self.cover - self.main_stirrup.diameter - rebar.diameter/2
        end_x = self.origin[0] + self.width - self.cover - self.main_stirrup.diameter - rebar.diameter/2
        # end_y = self.origin[1] - self.height + self.cover + self.main_stirrup + rebar.diameter/2
        counter = 0
        for x in range(self.r2_bars):
            rebar_1 = Rebar(type=self.rebar_type)
            rebar_1.set_coord_x(start_x)
            rebar_1.set_coord_y(start_y - counter * r2_spacing)
            self.rebars.append(rebar_1)
            rebar_2 = Rebar(type=self.rebar_type)
            rebar_2.set_coord_x(end_x)
            rebar_2.set_coord_y(start_y - counter * r2_spacing)
            self.rebars.append(rebar_2)
            counter += 1
    
    def set_rebar_r3_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        r3_spacing = (self.width - 2*self.cover - 2*self.main_stirrup.diameter - rebar.diameter)/(self.r3_bars-1)
        start_x = self.origin[0] + self.cover + self.main_stirrup.diameter + rebar.diameter/2
        start_y = self.origin[1] - self.cover - self.main_stirrup.diameter - rebar.diameter/2
        end_x = self.origin[0] + self.width - self.cover - self.main_stirrup.diameter - rebar.diameter/2
        end_y = self.origin[1] - self.height + self.cover + self.main_stirrup.diameter + rebar.diameter/2
        counter = 0
        for x in range(self.r3_bars):
            if counter !=0 and counter != (self.r3_bars-1):
                rebar_1 = Rebar(type=self.rebar_type)
                rebar_1.set_coord_x(start_x + counter * r3_spacing)
                rebar_1.set_coord_y(start_y)
                self.rebars.append(rebar_1)
                rebar_2 = Rebar(type=self.rebar_type)
                rebar_2.set_coord_x(start_x + counter * r3_spacing)
                rebar_2.set_coord_y(end_y)
                self.rebars.append(rebar_2)
            counter += 1

     # Outer Stirrup       
     # Vertical
    def set_main_stirrup_inner_vert_left_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        start_point = (
            self.origin[0] + self.cover + self.main_stirrup.diameter,
            self.origin[1] - self.cover - self.main_stirrup.diameter - rebar.diameter/2
        )
        end_point = (
            self.origin[0] + self.cover + self.main_stirrup.diameter,
            self.origin[1] - self.height + self.cover + self.main_stirrup.diameter  + rebar.diameter/2
        )
        self.vert_left_leg_inner_points = [start_point, end_point]

    def set_main_stirrup_outer_vert_left_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        start_point = (
            self.origin[0] + self.cover,
            self.origin[1] - self.cover - self.main_stirrup.diameter  - rebar.diameter/2
        )
        end_point = (
            self.origin[0] + self.cover,
            self.origin[1] - self.height + self.cover + self.main_stirrup.diameter  + rebar.diameter/2
        )
        self.vert_left_leg_outer_points = [start_point, end_point]


    def set_main_stirrup_inner_vert_right_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        start_point = (
            self.origin[0] + self.width - self.cover - self.main_stirrup.diameter,
            self.origin[1] - self.cover - self.main_stirrup.diameter  - rebar.diameter/2
        )
        end_point = (
            self.origin[0] + self.width - self.cover - self.main_stirrup.diameter,
            self.origin[1] - self.height + self.cover + self.main_stirrup.diameter  + rebar.diameter/2
        )
        self.vert_right_leg_inner_points = [start_point, end_point]

    def set_main_stirrup_outer_vert_right_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        start_point = (
            self.origin[0] + self.width - self.cover,
            self.origin[1] - self.cover - self.main_stirrup.diameter  - rebar.diameter/2
        )
        end_point = (
            self.origin[0] + self.width - self.cover,
            self.origin[1] - self.height + self.cover + self.main_stirrup.diameter  + rebar.diameter/2
        )
        self.vert_right_leg_outer_points = [start_point, end_point]

    # Horizontal
    def set_main_stirrup_inner_horizontal_top_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        start_point = (
            self.origin[0] + self.cover + self.main_stirrup.diameter + rebar.diameter/2,
            self.origin[1] - self.cover - self.main_stirrup.diameter
        )
        end_point = (
            self.origin[0] + self.width - self.cover - self.main_stirrup.diameter - rebar.diameter/2,
            self.origin[1] - self.cover - self.main_stirrup.diameter
        )
        self.top_leg_inner_points = [start_point, end_point]

    def set_main_stirrup_outer_horizontal_top_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        start_point = (
            self.origin[0] + self.cover + self.main_stirrup.diameter + rebar.diameter/2,
            self.origin[1] - self.cover
        )
        end_point = (
            self.origin[0] + self.width - self.cover - self.main_stirrup.diameter - rebar.diameter/2,
            self.origin[1] - self.cover
        )
        self.top_leg_outer_points = [start_point, end_point]

    def set_main_stirrup_inner_horizontal_bottom_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        start_point = (
            self.origin[0] + self.cover + self.main_stirrup.diameter + rebar.diameter/2,
            self.origin[1] - self.height + self.cover + self.main_stirrup.diameter
        )
        end_point = (
            self.origin[0] + self.width - self.cover - self.main_stirrup.diameter - rebar.diameter/2,
            self.origin[1] - self.height + self.cover + self.main_stirrup.diameter
        )
        self.bottom_leg_inner_points = [start_point, end_point]

    def set_main_stirrup_outer_horizontal_bottom_coordinates(self):
        rebar = Rebar(type=self.rebar_type)
        start_point = (
            self.origin[0] + self.cover + self.main_stirrup.diameter + rebar.diameter/2,
            self.origin[1] - self.height + self.cover
        )
        end_point = (
            self.origin[0] + self.width - self.cover - self.main_stirrup.diameter - rebar.diameter/2,
            self.origin[1] - self.height + self.cover
        )
        self.bottom_leg_outer_points = [start_point, end_point]

    def set_top_right_arc(self):
        rebar = Rebar(type=self.rebar_type)
        center_point = (
            self.origin[0] + self.cover + self.main_stirrup.diameter + rebar.diameter/2,
            self.origin[1] - self.cover - self.main_stirrup.diameter - rebar.diameter/2
        )
        self.arc_tr = Arc(
            center_point=center_point,
            radius = rebar.diameter/2 + self.main_stirrup.diameter,
            start_angle=90,
            end_angle=180
        )
        
    def set_top_left_arc(self):
        rebar = Rebar(type=self.rebar_type)
        center_point = (
            self.origin[0] +  self.width - self.cover - self.main_stirrup.diameter - rebar.diameter/2,
            self.origin[1] - self.cover - self.main_stirrup.diameter - rebar.diameter/2
        )
        self.arc_tl = Arc(
            center_point=center_point,
            radius = rebar.diameter/2 + self.main_stirrup.diameter,
            start_angle=0,
            end_angle=90,
        )
        
    def set_bottom_left_arc(self):
        rebar = Rebar(type=self.rebar_type)
        center_point = (
           self.origin[0] + self.cover + self.main_stirrup.diameter + rebar.diameter/2,
            self.origin[1] - self.height + self.cover + self.main_stirrup.diameter + rebar.diameter/2
        )
        self.arc_bl = Arc(
            center_point=center_point,
            radius = rebar.diameter/2 + self.main_stirrup.diameter,
            start_angle=180,
            end_angle=270
        )
        
    def set_bottom_right_arc(self):
        rebar = Rebar(type=self.rebar_type)
        center_point = (
           self.origin[0] +  self.width - self.cover - self.main_stirrup.diameter - rebar.diameter/2,
            self.origin[1] - self.height + self.cover + self.main_stirrup.diameter + rebar.diameter/2
        )
        self.arc_br = Arc(
            center_point=center_point,
            radius = rebar.diameter/2 + self.main_stirrup.diameter,
            start_angle=270,
            end_angle=0
        )
        
    def set_corner_hook(self):
        pass


