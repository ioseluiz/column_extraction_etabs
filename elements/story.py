class Story:
    def __init__(self, id, name, elevation):
        self.id = id
        self.name = name
        self.elevation = elevation
        
    def __str__(self):
        return f"Story: {self.name}, Elevation: {self.elevation}"