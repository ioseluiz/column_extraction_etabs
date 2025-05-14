

    
class Grid_Line:
    def __init__(self, id,name, pos_x, pos_y):
        self.id = id
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        
    def __str__(self):
        return f"Grid Line: {self.name}"


class Column:
    def __init__(self,id,center_x,center_y, b, h, fc, start_level, end_level, cant_rebar, rebar_type, detail):
        self.id = id
        self.center_x = center_x
        self.center_y
        self.b = b
        self.h = h
        self.fc = fc
        self.start_level = start_level
        self.end_level = end_level
        self.cant_rebar  = cant_rebar
        self.rebar_type = rebar_type
        self.detail = detail
        
        
    def __str__(self):
        return f"{self.b}x{self.h}"