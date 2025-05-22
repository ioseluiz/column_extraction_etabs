import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpacerItem, QSizePolicy, QFileDialog,
    QTableWidget, QTableWidgetItem, QScrollArea, QFrame
    
)
from PyQt5.QtGui import QFont, QPixmap 
from PyQt5.QtCore import Qt, QSize, QT_VERSION_STR, PYQT_VERSION_STR

import pandas as pd

from core import create_column_table


class ColumnDataScreen(QWidget):
    """
    Pantalla para mostrar y gestionar datos de columnas después de conectar con ETABS.
    Inspirada en la imagen proporcionada.
    """
    def __init__(self, main_menu_ref, sap_model_object=None, parent=None, column_data=None):
        super().__init__(parent)
        self.main_menu_ref = main_menu_ref
        self.sap_model = sap_model_object
        
        self.setWindowTitle("Detalle y Gestión de Columnas - ETABS")
        self.setGeometry(50, 50, 1200, 700) # Size based on complexity
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10,10,10,10)
        self.main_layout.setSpacing(10)
        
        # -- Seccion de Botones Superiores
        top_button_layout = QHBoxLayout()
        top_button_layout.setSpacing(5) # Menor espaciado para botones de accion
        
        self.btn_identificar_columnas = QPushButton("1. Reasignar Columnas")
        self.btn_exportar_excel = QPushButton("2. Exportar a Excel")
        self.btn_exportar_planos = QPushButton("3. Exportar Planos")
        
        top_button_layout.addWidget(self.btn_identificar_columnas)
        top_button_layout.addWidget(self.btn_exportar_excel)
        top_button_layout.addWidget(self.btn_exportar_planos)
        
        self.main_layout.addLayout(top_button_layout)
        
        # -- Area de Tabs para Datos de Columnas
        self.tabs_layout = QHBoxLayout()
        
        # Placeholder para Rectangular
        group_rectangular_layout = QVBoxLayout()
        lbl_rectangular_armado = QLabel("[Rectangular] Armado transversal")
        lbl_rectangular_resultados = QLabel("[Rectangular] Resultados")
        self.table_rectangular_armado = QTableWidget(len(column_data), 13) # Filas, Columnas de ejemplo
        self.table_rectangular_armado.setHorizontalHeaderLabels(["Piso","GridLine","Frame_id", "Sección", "depth","width", "Material", "Long. R2 Bars", "Long. R3 Bars","Rebar", "Rebar Est.","Cover","Detalle No."])
        
        print(column_data[0].keys())
        print(column_data[0])
        
        
        # Configure QTable
        for col_idx, col in enumerate(column_data):
            
            # Col 0: Piso
            item_piso = QTableWidgetItem(col['story'])
            self.table_rectangular_armado.setItem(col_idx, 0, item_piso)
            
            # Col 1: GridLine
            item_gridline = QTableWidgetItem(str(col['GridLine']))
            self.table_rectangular_armado.setItem(col_idx, 1, item_gridline)
            
            # Col 2: Frame id
            item_frame_id = QTableWidgetItem(col['col_id'])
            self.table_rectangular_armado.setItem(col_idx, 2, item_frame_id)
            
            # Col 3: Section
            # combo_section = QComboBox()
            # combo_section.addItems(defined_concrete_sections)
            item_section = QTableWidgetItem(col['section'])
            self.table_rectangular_armado.setItem(col_idx, 3, item_section)
            
            # Optional: Conectar signal para saber cuando cambia la seleccion
            # Usamos lambda para pasar la fila y el combobox a la funcion
            
            
            # Col 4: depthssss
            item_depth = QTableWidgetItem(str(col['depth']))
            self.table_rectangular_armado.setItem(col_idx, 4, item_depth)
            
            # Col 5: width
            item_width = QTableWidgetItem(str(col['width']))
            self.table_rectangular_armado.setItem(col_idx, 5, item_width)
            
            # Col 6: Material
            item_material = QTableWidgetItem(col['material'])
            self.table_rectangular_armado.setItem(col_idx, 6, item_material)
            
            # Col 7: Long. R2 Bars
            item_r2_bars = QTableWidgetItem(str(col['number_r2_bars']))
            self.table_rectangular_armado.setItem(col_idx, 7, item_r2_bars)
            
            # Col 8: Long. R3 Bars
            item_r3_bars = QTableWidgetItem(str(col['number_r3_bars']))
            self.table_rectangular_armado.setItem(col_idx, 8, item_r3_bars)
            
            # Col 9: Rebar #
            item_rebar = QTableWidgetItem(col['Rebar'])
            self.table_rectangular_armado.setItem(col_idx, 9, item_rebar)
            
            # Col 10: Mat. Est
            item_mat_est = QTableWidgetItem(col['Mat. Estribo'])
            self.table_rectangular_armado.setItem(col_idx, 10, item_mat_est)
            
            # Col 10: Cover
            item_cover = QTableWidgetItem(str(col['cover']))
            self.table_rectangular_armado.setItem(col_idx, 11,item_cover)
            
            # Col 11: Detalle #
            item_detalle = QTableWidgetItem(col['detail'])
            self.table_rectangular_armado.setItem(col_idx, 12,item_detalle)
            
            
        self.table_rectangular_armado.resizeColumnsToContents()
        # self.table_rectangular_armado.resizeRowToContents()
        
        
        # self.table_rectangular_resultados = QTableWidget(5, 4)
        # self.table_rectangular_resultados.setHorizontalHeaderLabels(["CONF...", "ID Ramas vert.", "CONF...", "ID Ramas horiz."])
        
        group_rectangular_layout.addWidget(lbl_rectangular_armado)
        group_rectangular_layout.addWidget(self.table_rectangular_armado)
        group_rectangular_layout.addWidget(lbl_rectangular_resultados)
        # group_rectangular_layout.addWidget(self.table_rectangular_resultados)
        
        # Placeholder par Circular
        # group_circular_layout = QVBoxLayout()
        # lbl_circular_armado = QLabel("[Circular] Armado transversal")
        # lbl_circular_resultados = QLabel("[Circular] Resultados")
        # self.table_circular_armado = QTableWidget(5, 3)
        # self.table_circular_armado.setHorizontalHeaderLabels(["Piso", "Columna", "Sección"])
        # self.table_circular_resultados = QTableWidget(5, 4)
        # self.table_circular_resultados.setHorizontalHeaderLabels(["CONF...", "ID Ramas vert.", "CONF...", "ID Ramas horiz."])

        # group_circular_layout.addWidget(lbl_circular_armado)
        # group_circular_layout.addWidget(self.table_circular_armado)
        # group_circular_layout.addWidget(lbl_circular_resultados)
        # group_circular_layout.addWidget(self.table_circular_resultados)

        self.tabs_layout.addLayout(group_rectangular_layout)
        # self.tabs_layout.addLayout(group_circular_layout)

        # Para hacer scrollable el contenido principal si excede el tamaño
        scroll_content_widget = QWidget()
        scroll_content_widget.setLayout(self.tabs_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content_widget)
        scroll_area.setFrameShape(QFrame.NoFrame) # Sin borde para el área de scroll

        self.main_layout.addWidget(scroll_area) # Añadir el área de scroll al layout principal
        
        # -- Boton de Volver
        bottom_layout = QHBoxLayout()
        self.btn_back_to_menu = QPushButton("Volver al Menú Principal")
        self.btn_back_to_menu.clicked.connect(self.go_back_to_main_menu)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.btn_back_to_menu)
        bottom_layout.addStretch(1)

        self.main_layout.addLayout(bottom_layout)
        
         # Conectar acciones (placeholders por ahora)
        self.btn_identificar_columnas.clicked.connect(self.load_column_data_action)

        self.apply_styles() # Aplicar algunos estilos básicos
        
    def apply_styles(self):
        # Estilo básico para los botones de acción
        action_button_style = """
            QPushButton {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11px;
                color: #FFFFFF;
                background-color: #0078D7; /* Azul similar al de Office/Windows */
                border: 1px solid #005A9E;
                padding: 6px 10px;
                border-radius: 3px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QPushButton:pressed {
                background-color: #003C6A;
            }
        """
        
        
        self.btn_identificar_columnas.setStyleSheet(action_button_style)
        self.btn_exportar_excel.setStyleSheet(action_button_style)
        self.btn_exportar_planos.setStyleSheet(action_button_style)

        # Estilo para el botón de volver (más grande y centrado)
        self.btn_back_to_menu.setStyleSheet("""
            QPushButton {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #2c3e50;
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 8px 20px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #d5d9db; }
            QPushButton:pressed { background-color: #bdc3c7; }
        """)
        self.setStyleSheet("QWidget { background-color: #E1E1E1; } QLabel { font-size: 12px; font-weight: bold; }")
        
    def load_column_data_action(self):
        """
        Placeholder para la acción de cargar/identificar datos de columnas.
        Aquí es donde interactuarías con self.sap_model para obtener los datos.
        """
        if self.sap_model:
            # Ejemplo: Obtener nombres de todas las columnas
            # try:
            #     _ret, number_names, column_names = self.sap_model.FrameObj.GetNameList(2) # Tipo 2 para columnas
            #     if _ret == 0 and number_names > 0:
            #         self.table_rectangular_armado.setRowCount(number_names)
            #         for i, name in enumerate(column_names):
            #             self.table_rectangular_armado.setItem(i, 1, QTableWidgetItem(name))
            #             # ... popular más datos ...
            #         self.main_menu_ref.show_message(f"{number_names} columnas identificadas (ejemplo).")
            #     else:
            #         self.main_menu_ref.show_message("No se encontraron columnas o hubo un error.")
            # except Exception as e:
            #     self.main_menu_ref.show_message(f"Error al obtener datos de columnas: {e}")
            self.main_menu_ref.show_message("Acción 'Identificar Columnas' activada. Conectado a ETABS.")
            # Simular llenado de tabla
            for r in range(5):
                self.table_rectangular_armado.setItem(r,0, QTableWidgetItem(f"Piso {r+1}"))
                self.table_rectangular_armado.setItem(r,1, QTableWidgetItem(f"C{r+1}-L{r*10}"))
                self.table_rectangular_armado.setItem(r,2, QTableWidgetItem(f"40x60"))

        else:
            self.main_menu_ref.show_message("No hay conexión activa con SapModel para cargar datos.")


    def go_back_to_main_menu(self):
        """Oculta esta pantalla y muestra el menú principal."""
        self.hide()
        if self.main_menu_ref:
            self.main_menu_ref.show()
            self.main_menu_ref.sap_model_connected = None # Limpiar referencia en el menú principal

    def closeEvent(self, event):
        """Maneja el cierre de la ventana."""
        self.go_back_to_main_menu() # Asegura que el menú principal se muestre
        super().closeEvent(event)
      