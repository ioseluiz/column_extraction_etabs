REBAR_PROPERTIES_MM = [
    {'rebar': '#3', 'diameter': 9.525, 'area': 71},
    {'rebar': '#4', 'diameter': 12.7, 'area': 129},
    {'rebar': '#5', 'diameter': 15.875, 'area': 200},
    {'rebar': '#6', 'diameter': 19.05, 'area': 284},
    {'rebar': '#7', 'diameter': 22.225, 'area': 387},
    {'rebar': '#8', 'diameter': 25.4, 'area': 509},
    {'rebar': '#9', 'diameter': 28.65, 'area': 645},
    {'rebar': '#10', 'diameter': 32.26, 'area': 819},
    {'rebar': '#11', 'diameter': 35.81, 'area': 1006},
    {'rebar': '#14', 'diameter': 43, 'area': 1452},
    
]

class Rebar:
    def __init__(self, rebar_type: str, pos_x: float, pos_y: float):
        self.rebar_type = rebar_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.diameter = self.get_rebar_diameter()
        
    def get_rebar_diameter(self):
        for bar in REBAR_PROPERTIES_MM:
            if bar['rebar'] == self.rebar_type:
                return bar['diameter']
            
        return None