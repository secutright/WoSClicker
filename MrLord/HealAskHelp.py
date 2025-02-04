import pyautogui
import time

def safe_locate_on_screen(image_path, region=None, confidence=0.8):
    """
    Calls pyautogui.locateOnScreen and catches the ImageNotFoundException if necessary.
    Returns None if the image is not found.
    """
    try:
        return pyautogui.locateOnScreen(image_path, region=region, confidence=confidence)
    except pyautogui.ImageNotFoundException:
        return None

def main():
    print("Searching for 'heal.png' or 'help.png' and clicking them if found.")
    print("Exit the script with CTRL + C.\n")
    
    # Paths to the buttons
    heal_image_path = r"C:\Users\norma\Documents\My Games\Whiteoutsurvival\heal.png"
    help_image_path = r"C:\Users\norma\Documents\My Games\Whiteoutsurvival\help.png"
    
    # Enlarged region or omit entirely
    region = (872, 671, 138, 72)  # Example: If you need a larger area
    
    while True:
        # 1) Search for 'heal.png'
        location_heal = safe_locate_on_screen(
            heal_image_path, 
            region=region, 
            confidence=0.8
        )
        if location_heal is not None:
            print("Heal symbol found!")
            center_heal = pyautogui.center(location_heal)
            
            # Double-click
            pyautogui.click(center_heal)
            time.sleep(0.1)
            pyautogui.click(center_heal)
            
            # Wait a bit to avoid immediate re-clicking
            time.sleep(0.3)
        
        # 2) Search for 'help.png'
        location_help = safe_locate_on_screen(
            help_image_path,
            region=region,
            confidence=0.8
        )
        if location_help is not None:
            print("Help symbol found!")
            center_help = pyautogui.center(location_help)
            
            # Double-click
            pyautogui.click(center_help)
            time.sleep(0.1)
            pyautogui.click(center_help)
            
            time.sleep(1)
        
        # Short break
        time.sleep(0.5)

if __name__ == "__main__":
    main()
