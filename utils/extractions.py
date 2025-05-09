
def get_story_data(sap_model):
    stories_data = []
    print(sap_model.Story.GetNameList())
    try:
        num_stories, story_names_tuple, ret = sap_model.Story.GetNameList()
        if ret != 0 or not story_names_tuple:
            print("Error: Could not retrieve story names or no stories found.")
            return []
        
        story_names = list(story_names_tuple) # Convert tuple to list
        for story_name in story_names:
            elevation, ret_elev = sap_model.Story.GetElevation(story_name)
            print(sap_model.Story.GetElevation(story_name))
            if ret_elev == 0:
                stories_data.append({"name": story_name, "elevation": elevation})
            else:
                print(f"Warning: Could not retrieve elevation for story '{story_name}'.")
        
        # Sort stories by elevation in ascending order
        stories_data.sort(key=lambda s: s["elevation"])
        print(f"Successfully retrieved {len(stories_data)} stories.")
        return stories_data  
            
    except Exception as e:
        print(f"An error occured while getting story data: {e}")
        return []
    
def extract_columns_by_level(sap_model, stories_data):
    if not stories_data:
        print("No story data provided to extract columns by level")
        return []
    
    columns_by_level = {story["name"]: [] for story in stories_data}
    all_frames_count = 0
    identified_columns_count = 0
    
    try:
        # Get all frame objects name
        num_frames, frame_names_tuple, ret = sap_model.FrameObj.GetNameList()
        if ret !=0:
            print("Error: Could not retrieve frame object names.")
            return {}
        if not frame_names_tuple:
            print("No frame objects found in the model.")
            return columns_by_level # Return empty structure
        
        frame_names = list(frame_names_tuple)
        all_frames_count = len(frame_names)
        print(f"\nProcessing {all_frames_count} from objects to identify columns...")
        
        for frame_name in frame_names:
            is_column = False
            
            # Method 1: Check Design Orientation and Section Type
            # Get design orientation: 0 for Vertical, 1 for Horizontal, 2 for Inclined
            
    
    except Exception as e:
        print(f"An error occurred during column extraction: {e}")