import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpacerItem, QSizePolicy, QFileDialog,
    QTableWidget, QTableWidgetItem, QScrollArea, QFrame
    
)
from PyQt5.QtGui import QFont, QPixmap 
from PyQt5.QtCore import Qt, QSize, QT_VERSION_STR, PYQT_VERSION_STR

from core import create_column_table

class ColumnDataScreen(QWidget):
    """
    Pantalla para mostrar y gestionar datos de columnas después de conectar con ETABS.
    Inspirada en la imagen proporcionada.
    """
    def __init__(self, main_menu_ref, sap_model_object=None, parent=None):
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
        self.btn_exportar_planos = QPushButton("2. Exportar Planos")
        
        top_button_layout.addWidget(self.btn_identificar_columnas)
        top_button_layout.addWidget(self.btn_exportar_planos)
        
        self.main_layout.addLayout(top_button_layout)
        
        # -- Area de Tabs para Datos de Columnas
        self.tabs_layout = QHBoxLayout()
        
        # Placeholder para Rectangular
        group_rectangular_layout = QVBoxLayout()
        lbl_rectangular_armado = QLabel("[Rectangular] Armado transversal")
        lbl_rectangular_resultados = QLabel("[Rectangular] Resultados")
        self.table_rectangular_armado = QTableWidget(5, 3) # Filas, Columnas de ejemplo
        self.table_rectangular_armado.setHorizontalHeaderLabels(["Piso", "Columna", "Sección"])
        self.table_rectangular_resultados = QTableWidget(5, 4)
        self.table_rectangular_resultados.setHorizontalHeaderLabels(["CONF...", "ID Ramas vert.", "CONF...", "ID Ramas horiz."])
        
        group_rectangular_layout.addWidget(lbl_rectangular_armado)
        group_rectangular_layout.addWidget(self.table_rectangular_armado)
        group_rectangular_layout.addWidget(lbl_rectangular_resultados)
        group_rectangular_layout.addWidget(self.table_rectangular_resultados)
        
        # Placeholder par Circular
        group_circular_layout = QVBoxLayout()
        lbl_circular_armado = QLabel("[Circular] Armado transversal")
        lbl_circular_resultados = QLabel("[Circular] Resultados")
        self.table_circular_armado = QTableWidget(5, 3)
        self.table_circular_armado.setHorizontalHeaderLabels(["Piso", "Columna", "Sección"])
        self.table_circular_resultados = QTableWidget(5, 4)
        self.table_circular_resultados.setHorizontalHeaderLabels(["CONF...", "ID Ramas vert.", "CONF...", "ID Ramas horiz."])

        group_circular_layout.addWidget(lbl_circular_armado)
        group_circular_layout.addWidget(self.table_circular_armado)
        group_circular_layout.addWidget(lbl_circular_resultados)
        group_circular_layout.addWidget(self.table_circular_resultados)

        self.tabs_layout.addLayout(group_rectangular_layout)
        self.tabs_layout.addLayout(group_circular_layout)

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
        
        
    

class NewGameWindow(QWidget):
    """
    A new window that appears when 'Start New Game' is clicked.
    It contains a button to open a QFileDialog for .edb files,
    a button to process the file, and a button to go back to the main menu.
    """
    def __init__(self, main_menu_ref, parent=None): # Added main_menu_ref
        super().__init__(parent)
        self.main_menu_ref = main_menu_ref # Store reference to main menu
        self.selected_file_path = None # To store the path of the selected .edb file

        self.setWindowTitle("Extraccion de Datos ETABS")
        self.setMinimumSize(450, 250) # Adjusted minimum size
        self.setGeometry(200, 200, 450, 250) # x, y, width, height

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        self.info_label = QLabel("Seleccione una opcion.", self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)

        self.btn_select_file = QPushButton("Select .edb File", self)
        self.btn_select_file.clicked.connect(self.open_file_dialog)
        
        # Style the select file button
        self.btn_select_file.setStyleSheet(f"""
            QPushButton {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
                font-weight: bold;
                color: #FFFFFF;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #00AEC4, stop:1 #00868B); /* Teal */
                border: 2px solid #006063;
                padding: 10px 20px;
                border-radius: 6px;
                min-width: 150px;
                outline: none;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #00868B, stop:1 #00AEC4);
                border: 2px solid #00868B;
            }}
            QPushButton:pressed {{
                background-color: #006063;
                border: 2px solid #006063;
            }}
        """)

        self.selected_file_label = QLabel("No selecciono ningun archivo.", self)
        self.selected_file_label.setAlignment(Qt.AlignCenter)
        self.selected_file_label.setStyleSheet("font-style: italic; color: #7f8c8d;")

        # --- New Buttons ---
        self.btn_process_file = QPushButton("Aceptar", self)
        self.btn_process_file.clicked.connect(self.process_selected_file)
        self.btn_process_file.setEnabled(False) # Initially disabled

        self.btn_back_to_menu = QPushButton("Volver al Menu Principal", self)
        self.btn_back_to_menu.clicked.connect(self.go_back_to_main_menu)

        # Styling for new buttons
        button_style_sheet_process = f"""
            QPushButton {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                font-weight: bold;
                color: #FFFFFF;
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #00AEC4, stop:1 #00868B); /* Teal for process */
                border: 2px solid #006063;
                padding: 8px 15px;
                border-radius: 6px;
                outline: none;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #00868B, stop:1 #00AEC4);
                border: 2px solid #00868B;
            }}
            QPushButton:pressed {{
                background-color: #006063;
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
                border-color: #7f8c8d;
                color: #7f8c8d;
            }}
        """
        button_style_sheet_back = f"""
            QPushButton {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                color: #2c3e50; /* Dark text for back button */
                background-color: #ecf0f1; /* Light gray */
                border: 1px solid #bdc3c7; /* Subtler border */
                padding: 8px 15px;
                border-radius: 6px;
                outline: none;
            }}
            QPushButton:hover {{
                background-color: #d5d9db;
                border-color: #95a5a6;
            }}
            QPushButton:pressed {{
                background-color: #bdc3c7;
            }}
        """
        self.btn_process_file.setStyleSheet(button_style_sheet_process)
        self.btn_back_to_menu.setStyleSheet(button_style_sheet_back)

        # Layout for the bottom buttons
        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_button_layout.addWidget(self.btn_back_to_menu)
        bottom_button_layout.addWidget(self.btn_process_file)
        bottom_button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))


        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.btn_select_file, 0, Qt.AlignHCenter)
        self.layout.addWidget(self.selected_file_label)
        self.layout.addStretch(1) # Add stretchable space
        self.layout.addLayout(bottom_button_layout) # Add the new button layout

        # Fallback background color if no specific styling is inherited
        self.setStyleSheet("QWidget { background-color: #f0f3f4; } " + self.styleSheet()) # Ensure QWidget is targeted

    def open_file_dialog(self):
        """
        Opens a QFileDialog to select files with the .edb extension.
        """
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog # Uncomment if native dialog causes issues
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo EDB",  # Dialog Title
            "",                 # Default directory (empty means current or last used)
            "EDB Files (*.edb);;All Files (*)",  # File filter
            options=options
        )

        if file_name:
            print(f"Selected file: {file_name}")
            self.selected_file_path = file_name # Store the full path
            self.selected_file_label.setText(f"Selected: {file_name.split('/')[-1]}")
            self.selected_file_label.setStyleSheet("color: #2c3e50; font-weight: bold;") # Darker text for selected file
            self.btn_process_file.setEnabled(True) # Enable process button
        else:
            print("File selection cancelled.")
            self.selected_file_path = None # Reset path
            self.selected_file_label.setText("File selection cancelled.")
            self.selected_file_label.setStyleSheet("font-style: italic; color: #c0392b;") # Reddish for cancelled
            self.btn_process_file.setEnabled(False) # Disable process button

    def process_selected_file(self):
        """
        Placeholder function to process the selected .edb file.
        This function will be implemented later.
        """
        if self.selected_file_path:
            print(f"Processing file: {self.selected_file_path}")
            # TODO: Implement file processing logic here
            self.info_label.setText(f"Processing: {self.selected_file_path.split('/')[-1]}...")
            # For now, just show a message
            # Call function to open etabs and extract the column data
            create_column_table.get_model_data(self.selected_file_path)
            
            
        else:
            print("No file selected to process.")
            self.info_label.setText("No file selected. Please select an .edb file first.")

    def go_back_to_main_menu(self):
        """Hides this window and shows the main menu."""
        self.hide()
        if self.main_menu_ref:
            self.main_menu_ref.show()

    def closeEvent(self, event):
        """Handle the case where this window is closed directly."""
        if self.main_menu_ref:
            # Option 1: Show main menu if this window is closed (unless app is exiting)
            # self.main_menu_ref.show()
            # Option 2: Or, if this window closing means exiting this part of the flow,
            # the main menu's visibility is handled by its own logic or app exit.
            # For now, we assume closing this window means returning to the main menu's control.
            # If the main menu is not visible and this is closed, it might be good to show it.
            if not self.main_menu_ref.isVisible():
                 self.main_menu_ref.show() # Show main menu if it was hidden
        super().closeEvent(event)


class MainMenuScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu Principal")
        self.setGeometry(100, 100, 800, 600) # x, y, width, height
        self.new_game_window = None # Attribute to hold the new game window instance
        self.column_data_screen = None # Atributo para la nueva pantalla
        self.sap_model_connected = None # Para almacenar el objeto SapModel

        # --- Central Widget and Layout ---
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Main vertical layout for the central widget
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(50, 50, 50, 50) 
        self.main_layout.setSpacing(20) 

        # --- Background Image Placeholder ---
        self.background_image_path = "path/to/your/background_image.jpg"


        # --- Title Label ---
        self.title_label = QLabel("ETABS - Cuadro de Columnas", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # --- Menu Buttons ---
        self.btn_start_game = QPushButton("Crear cuadro de cols")
        self.btn_connect_etabs = QPushButton("Conectar con archivo de ETABS abierto")
        self.btn_exit = QPushButton("Salir del Programa")

        # Set object names for specific styling
        self.btn_start_game.setObjectName("StdButton")
        self.btn_connect_etabs.setObjectName("StdButton")
        self.btn_exit.setObjectName("ExitButton")


        # --- Layout Management ---
        self.main_layout.addWidget(self.title_label, 0, Qt.AlignTop | Qt.AlignHCenter)
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addWidget(self.btn_start_game)
        button_layout.addWidget(self.btn_connect_etabs)
        button_layout.addWidget(self.btn_exit)

        self.main_layout.addLayout(button_layout)
        self.main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


        # --- Connect Signals to Slots (Button Actions) ---
        self.btn_start_game.clicked.connect(self.start_game)
        self.btn_connect_etabs.clicked.connect(self.connect_to_etabs_instance)
        self.btn_exit.clicked.connect(self.exit_application)

        # --- Apply Stylesheet ---
        self.apply_styles()

    def apply_styles(self):
        """Applies QSS styles to the main menu using the new color palette."""
        pixmap = QPixmap(self.background_image_path)
        qss_compatible_path = self.background_image_path.replace("\\", "/")
        
        color_teal_base = "#00868B" 
        color_teal_light = "#00AEC4" 
        color_teal_dark = "#006063"  

        color_red_base = "#E40E2D"   
        color_red_light = "#F71F3F"  
        color_red_dark = "#B80B24"   

        color_blue_base = "#0147BA"  
        color_text_light = "#FFFFFF" 
        color_title_shadow = "#00235C" 

        final_background_style = ""
        if not pixmap.isNull():
            final_background_style = f"""
                background-image: url({qss_compatible_path});
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-size: cover; 
            """
        else:
            print(f"Warning: Background image not found at '{self.background_image_path}'. Using fallback color: {color_blue_base}.")
            final_background_style = f"background-color: {color_blue_base};" 

        self.setStyleSheet(f"""
            QMainWindow {{
                {final_background_style}
            }}
            QWidget#MainMenuScreenCentralWidget {{
                /* background-color: transparent; */ 
            }}
            QLabel#TitleLabel {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 48px;
                font-weight: bold;
                color: {color_text_light}; 
                padding: 20px;
                text-shadow: 2px 2px 4px {color_title_shadow};
            }}
            QPushButton#StdButton {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                color: {color_text_light};
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 {color_teal_light}, stop:1 {color_teal_base});
                border: 2px solid {color_teal_dark};
                padding: 12px 25px;
                border-radius: 8px;
                min-width: 200px;
                outline: none;
            }}
            QPushButton#StdButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 {color_teal_base}, stop:1 {color_teal_light}); 
                border: 2px solid {color_teal_base};
            }}
            QPushButton#StdButton:pressed {{
                background-color: {color_teal_dark}; 
                border: 2px solid {color_teal_dark};
            }}
            QPushButton#ExitButton {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 18px;
                font-weight: bold;
                color: {color_text_light};
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 {color_red_light}, stop:1 {color_red_base});
                border: 2px solid {color_red_dark};
                padding: 12px 25px;
                border-radius: 8px;
                min-width: 200px;
                outline: none;
            }}
            QPushButton#ExitButton:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 {color_red_base}, stop:1 {color_red_light}); 
                border: 2px solid {color_red_base};
            }}
            QPushButton#ExitButton:pressed {{
                background-color: {color_red_dark};
                border: 2px solid {color_red_dark};
            }}
        """)
        self.central_widget.setObjectName("MainMenuScreenCentralWidget")
        self.title_label.setObjectName("TitleLabel")

    def start_game(self):
        """Hides the main menu and shows the NewGameWindow."""
        print("Action: Start New Game clicked!")
        if not self.new_game_window: # Create window only if it doesn't exist
            self.new_game_window = NewGameWindow(main_menu_ref=self) # Pass self (main menu)
        
        self.new_game_window.show()
        self.hide() # Hide the main menu

    def load_game(self):
        print("Action: Crear cuadro de columnas!")
        self.show_message("Cargando Cuadro de Columnas ...") # Placeholder

    def open_options(self):
        print("Action: Options clicked!")
        self.show_message("Opening Options...") # Placeholder
        
    def connect_to_etabs_instance(self):
        print("Action: Conectar con archivo de ETABS abierto clicked!")
        self.show_message("Intentando conectar con ETABS...")
        success, message, sap_model = create_column_table.connect_to_active_etabs_instance()
        if success and sap_model:
            self.spa_model_connected = sap_model
            self.show_message(message)
            
            # Crear y mostrar la ColumnDataScreen
            if not self.column_data_screen:
                self.column_data_screen = ColumnDataScreen(main_menu_ref=self, sap_model_object=self.spa_model_connected)
            else:
                # Si ya existe, actualiza la referencia al sap_model por si acaso
                self.column_data_screen.sap_model = self.sap_model_connected
                # Aquí podrías llamar a una función en column_data_screen para refrescar datos si es necesario
                # self.column_data_screen.refresh_display_with_new_model()

            self.column_data_screen.show()
            self.hide() # Ocultar el menú principal
                
                
            # create_column_table.get_open_model_data(sap_model)
            
        elif success and not sap_model:
             # ETABS conectado pero sin modelo abierto
            self.show_message(message + " Se requiere un modelo abierto para ver los datos de columnas.")
            self.sap_model_connected = None
        else:
            self.show_message(message) # Muestra el mensaje de error
            self.sap_model_connected = None

    def exit_application(self):
        print("Action: Salir del Programa clicked!")
        # Before quitting, ensure child windows are also closed if necessary
        if self.new_game_window and self.new_game_window.isVisible():
            self.new_game_window.close()
        QApplication.instance().quit()

    def show_message(self, message):
        """Helper to show a temporary message label (used for Load Game/Options)."""
        existing_labels = self.central_widget.findChildren(QLabel, "temp_message_label")
        for label in existing_labels:
            label.deleteLater()

        msg_label = QLabel(message, self.central_widget)
        msg_label.setObjectName("temp_message_label")
        msg_label.setAlignment(Qt.AlignCenter)
        
        defined_color_text_light = getattr(self, 'color_text_light', '#FFFFFF')

        msg_label.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(0, 0, 0, 0.75);
                color: {defined_color_text_light}; 
                font-size: 16px;
                padding: 10px 15px;
                border-radius: 5px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
        """)
        
        msg_label.adjustSize()
        msg_label.move(
            int((self.central_widget.width() - msg_label.width()) / 2),
            int(self.central_widget.height() - msg_label.height() - 20)
        )
        msg_label.show()
        msg_label.raise_()
        # from PyQt5.QtCore import QTimer # Uncomment for auto-hide
        # QTimer.singleShot(3000, msg_label.deleteLater) # Uncomment for auto-hide
    
    # Sobrescribir closeEvent para cerrar también ColumnDataScreen si está abierta
    def closeEvent(self, event):
        if self.new_game_window:
            self.new_game_window.close()
        if self.column_data_screen: # Añadido
            self.column_data_screen.close()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    print(f"Using Qt Version: {QT_VERSION_STR}")
    print(f"Using PyQt Version: {PYQT_VERSION_STR}")

    main_menu = MainMenuScreen()
    main_menu.show()
    sys.exit(app.exec_())
