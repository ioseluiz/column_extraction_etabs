from dxf_drawer.drawing import Drawing
from dxf_drawer.detail import Detail
from dxf_drawer.column import RectangularColumn


def main():

    # 1. Create list of Detail
    list_details = []
    start_point = (100,100)
    counter = 0
    width_detail = 4000
    height_detail = 4000

    columns = [
        RectangularColumn(width=500, height=1500, fc=420, number_of_bars=24, rebar_type='#10', r2_bars=7, r3_bars=4, cover = 40.0, stirrup_type='#4'),
        RectangularColumn(width=300, height=700, fc=420, number_of_bars=16, rebar_type='#6', r2_bars=5, r3_bars=4, cover=40.0, stirrup_type='#4'),
        RectangularColumn(width=400, height=400, fc=420, number_of_bars=4, rebar_type="#5", r2_bars=2, r3_bars=4,cover=40.0, stirrup_type='#4'),
        RectangularColumn(width=300, height=1000, fc=420, number_of_bars=16, rebar_type="#7", r2_bars=6, r3_bars=4,cover=40.0, stirrup_type='#4'),
        RectangularColumn(width=500, height=800, fc=420, number_of_bars=12, rebar_type="#9", r2_bars=9, r3_bars=4, cover=40.0, stirrup_type='#4'),
        RectangularColumn(width=700, height=1200, fc=420, number_of_bars=12, rebar_type="#9", r2_bars=10, r3_bars=6, cover=40.0, stirrup_type='#4'),

    ]
    
    for i in range(1, len(columns)+1): #1 to 5
        actual_col = columns[i-1]
        origin_point = (start_point[0], start_point[1] - (height_detail*counter))
        detail = Detail(f"DC-{i}",origin_point, width_detail, height_detail)
        detail.set_column(actual_col)
        detail.set_origin_for_col(actual_col.width, actual_col.height)
        list_details.append( detail)
        counter += 1

    drawing = Drawing(filename='dibujo_prueba.dxf', list_details=list_details)
    drawing.create_dxf()

if __name__ == "__main__":
    main()