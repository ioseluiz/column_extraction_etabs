import ezdxf
from math import sqrt

# 📐 Parámetros
ancho = 1300                # mm
alto = 1400                 # mm
rec = 50                   # mm
d_barra = 38             # Ø#8 mm
d_estribo = 16             # Ø estribo mm
barras_superior = 10        # por cara larga
barras_lateral = 10         # por cara corta

# 📏 Radios mínimos de doblado 90° (mm) según diámetro de estribo
radios_doblado_90 = {
    6: 25, 8: 35, 10: 40, 12: 50, 16: 65, 20: 115, 25: 135
}
radio_interior = radios_doblado_90[d_estribo]
radio_exterior = radio_interior + d_estribo

# 📄 Crear archivo DXF
doc = ezdxf.new()
msp = doc.modelspace()

# 🟥 Dibujar contorno general de la columna
msp.add_lwpolyline([(0, 0), (ancho, 0), (ancho, alto), (0, alto), (0, 0)],
                   close=True, dxfattribs={"color": 1})

# 🔁 Función para dibujar estribos redondeados
def dibujar_estribo(msp, x1, y1, x2, y2, radio):
    msp.add_line((x1 + radio, y1), (x2 - radio, y1))
    msp.add_line((x2, y1 + radio), (x2, y2 - radio))
    msp.add_line((x2 - radio, y2), (x1 + radio, y2))
    msp.add_line((x1, y2 - radio), (x1, y1 + radio))
    msp.add_arc((x2 - radio, y1 + radio), radio, 270, 360)
    msp.add_arc((x2 - radio, y2 - radio), radio, 0, 90)
    msp.add_arc((x1 + radio, y2 - radio), radio, 90, 180)
    msp.add_arc((x1 + radio, y1 + radio), radio, 180, 270)

# Área útil
x1 = rec
y1 = rec
x2 = ancho - rec
y2 = alto - rec

# Estribos exterior e interior
dibujar_estribo(msp, x1, y1, x2, y2, radio_exterior)
dibujar_estribo(
    msp,
    x1 + d_estribo,
    y1 + d_estribo,
    x2 - d_estribo,
    y2 - d_estribo,
    radio_interior
)

# Zona disponible para barras longitudinales intermedias
x_ini = x1 + d_estribo + d_barra / 2
x_fin = x2 - d_estribo - d_barra / 2
y_ini = y1 + d_estribo + d_barra / 2
y_fin = y2 - d_estribo - d_barra / 2

# Barras intermedias horizontales
if barras_superior > 2:
    sep_x = (x_fin - x_ini) / (barras_superior - 1)
    for i in range(barras_superior):
        x = x_ini + i * sep_x
        if i in [0, barras_superior - 1]: continue
        msp.add_circle((x, y_ini), d_barra / 2)
        msp.add_circle((x, y_fin), d_barra / 2)

# Barras intermedias verticales
if barras_lateral > 2:
    sep_y = (y_fin - y_ini) / (barras_lateral - 1)
    for i in range(barras_lateral):
        y = y_ini + i * sep_y
        if i in [0, barras_lateral - 1]: continue
        msp.add_circle((x_ini, y), d_barra / 2)
        msp.add_circle((x_fin, y), d_barra / 2)

# 🔘 Barras de ESQUINA con fórmula ajustada
# BX = REC + DE + R - (R - DB/2)/√2
delta = (radio_interior - d_barra / 2) / sqrt(2)
bx = rec + d_estribo + radio_interior - delta
by = rec + d_estribo + radio_interior - delta

# Esquinas (en orden: inf. izq., inf. der., sup. izq., sup. der.)
esquinas = [
    (bx, by),
    (ancho - bx, by),
    (bx, alto - by),
    (ancho - bx, alto - by)
]

for cx, cy in esquinas:
    msp.add_circle((cx, cy), d_barra / 2)

# Texto descriptivo
total_barras = barras_superior * 2 + barras_lateral * 2 - 4
msp.add_text(f"Rectangular {ancho/100:.2f}x{alto/100:.2f}",
             dxfattribs={'height': 50, 'color': 2}).set_placement((ancho/4, alto + 100))
msp.add_text(f"{total_barras} Ø#8", dxfattribs={'height': 50, 'color': 2}).set_placement((ancho/3, alto + 50))

# Guardar DXF
doc.saveas("columna_redonda_esquinas_CORREGIDO.dxf")
print("✅ Archivo generado correctamente con fórmula de esquinas ajustada.")
