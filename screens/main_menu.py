import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpacerItem, QSizePolicy, QFileDialog,
    QTableWidget, QTableWidgetItem, QScrollArea, QFrame
    
)
from PyQt5.QtGui import QFont, QPixmap 
from PyQt5.QtCore import Qt, QSize, QT_VERSION_STR, PYQT_VERSION_STR

from core import create_column_table

# Import Screens
from screens.column_data import ColumnDataScreen
from screens.open_file import OpenFileWindow

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
        """Hides the main menu and shows the OpenFileWindow."""
        print("Action: Start New Game clicked!")
        if not self.new_game_window: # Create window only if it doesn't exist
            self.new_game_window = OpenFileWindow(main_menu_ref=self) # Pass self (main menu)
        
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
            self.sap_model_connected = sap_model
            self.show_message(message)
            
            # Get model Column data
            column_data = create_column_table.get_open_model_data(sap_model)
            
            
            # Crear y mostrar la ColumnDataScreen
            if not self.column_data_screen:
                self.column_data_screen = ColumnDataScreen(main_menu_ref=self, sap_model_object=self.sap_model_connected, column_data=column_data)
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
