import ezdxf
import math

# 📐 Parámetros
diametro_columna = 600     # mm
diam_estr = 12             # mm (DE)
diam_barra = 25.4          # mm (DB)
num_barras = 12            # número de barras longitudinales

# 📏 Cálculo de radios según TU fórmula
# r_barra = (D/2) - DE - (DB/2)
r_barra = (diametro_columna / 2) - diam_estr - (diam_barra / 2)

# Visual (opcional): radios de estribo para trazo
recubrimiento = 40
r_ext_estribo = (diametro_columna / 2) - recubrimiento
r_int_estribo = r_ext_estribo - diam_estr

# 🗂️ Crear DXF
doc = ezdxf.new()
msp = doc.modelspace()

# 🟥 Columna externa
msp.add_circle((0, 0), radius=diametro_columna / 2, dxfattribs={"color": 1})

# 🌀 Estribos circular visuales
msp.add_circle((0, 0), radius=r_ext_estribo, dxfattribs={"color": 3})
msp.add_circle((0, 0), radius=r_int_estribo, dxfattribs={"color": 3})

# 🔘 Barras tangentes al estribo interno
for i in range(num_barras):
    angulo = 2 * math.pi * i / num_barras
    x = r_barra * math.cos(angulo)
    y = r_barra * math.sin(angulo)
    msp.add_circle((x, y), radius=diam_barra / 2, dxfattribs={"color": 5})

# 🏷️ Texto informativo
msp.add_text(f"Columna Ø{diametro_columna} mm, {num_barras} Ø{int(diam_barra)}",
             dxfattribs={'height': 40, 'color': 2}).set_placement((-diametro_columna / 2, diametro_columna / 2 + 50))

# 💾 Guardar
doc.saveas("columna_circular_tangente_CORREGIDA.dxf")
print("✅ DXF generado como 'columna_circular_tangente_CORREGIDA.dxf'")
