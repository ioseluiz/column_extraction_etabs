import comtypes.client
import os
import sys
from pathlib import Path
from utils import extractions
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,QMainWindow, QWidget, QPushButton, QVBoxLayout, QFileDialog, QTextEdit, QLabel
)
from PyQt5.QtGui import QColor, QPalette

qss = """
        #widget
             {
              border-image: url(self.image_path) 0 0 0 0 stretch stretch;
            }
            """
            
class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Second Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

class AppGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.w = None
        self.initUI()
        
    def initUI(self):
        ROOT_FOLDER = os.getcwd()
        IMG_FOLDER = Path(ROOT_FOLDER) / "img"
        self.image_path = str(Path(IMG_FOLDER / "skyline.png"))
        print(self.image_path)
        self.setGeometry(300,300, 1000,1000)
        self.setFixedSize(1000,1000)
        self.setWindowTitle("ETABS Concrete Column Table")
        
        self.widget = QWidget(self)
        self.widget.setObjectName("widget")
        
        self.image()
        
        self.lblTitle = QLabel()
        self.lblTitle.setText("Selec ETABS EDB File")
        self.lblTitle.setAlignment(Qt.AlignCenter)
        
        self.button = QPushButton("Go to next window")
        self.button.clicked.connect(self.show_new_window)
        
       
        
        
        
        layout = QVBoxLayout()
        layout.addWidget(self.lblTitle)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        
        self.show()
        
    def show_new_window(self):
        if self.w is None:
            self.w = SecondWindow()
            self.w.show()
        else:
            self.w = None # Discard reference, close window
        
        
    def image(self):
        self.image=QLabel(self)
        self.image.setPixmap(QPixmap(self.image_path))
        self.image.resize(1000,1000)
        
        


def get_model_data():
    ModelPath = r"C:\Users\User\Downloads\OneDrive_1_8-5-2025\POYECTO 01 CUADRO DE COLUMNAS\AURORA-11R (PAREDES LIVIANAS)(SOLO SW)-CABEZAL DESIGN.EDB"
    print(ModelPath)
        
    # Create API helper object
    helper = comtypes.client.CreateObject('ETABSv1.Helper')
    helper = helper.QueryInterface(comtypes.gen.ETABSv1.cHelper)

    EtabsObject = helper.CreateObjectProgID("CSI.ETABS.API.ETABSObject")

    # Start ETABS application
    EtabsObject.ApplicationStart()
    # Create SnapModel Object
    SapModel =EtabsObject.SapModel
    print(SapModel)
    SapModel.File.OpenFile(ModelPath)

    # Open and save the model
    print("ETABS model opened successfully!")

    # Get the model's name to verify the connection
    ModelName = EtabsObject.SapModel.GetModelFilename()

    print(f"Model loaded: {ModelName}")

    print("\nFetching story information...")
    stories = extractions.get_story_data(SapModel)

    if not stories:
        print("Could not retrieve story information. Exiting.")
                # Optional: Release COM objects
                # sap_model = None
                # if 'etabs_object' in locals() and etabs_object is not None:
                #     etabs_object = None
        sys.exit()
        
    for story in stories:
        print(f"  Story: {story['name']}, Elevation: {story['elevation']:.2f}")
        
    extractions.extract_columns_by_level(SapModel,stories)

    #Close Application
    EtabsObject.ApplicationExit(False)
    
def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    gui = AppGUI()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()




