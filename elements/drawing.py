from .detail import Detail
import ezdxf

class Drawing:
    def __init__(self, filename, list_details: list[Detail]):
        self.filename = filename
        self.list_details = list_details
        
    def create_drawing(self):
        doc = ezdxf.new("R2010")
        msp = doc.modelspace()
        doc.saveas(self.filename)