import comtypes.client
import os
import sys
from pathlib import Path
from utils import extractions

def main():
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
    

if __name__ == "__main__":
    main()




