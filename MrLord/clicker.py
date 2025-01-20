import cv2
import numpy as np
import pyautogui
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

symbol_path = "handschlag.png"
template = cv2.imread(symbol_path, cv2.IMREAD_COLOR)

if template is None:
    logging.error("Das Symbol konnte nicht geladen werden. Bitte prüfen Sie den Pfad.")
    exit(1)

threshold = 0.7

# Vergrößerte Region
REGION_X, REGION_Y = 130, 870
REGION_W, REGION_H = 300, 100

while True:
    # Screenshot nur dieser Region
    screenshot_region = pyautogui.screenshot(region=(REGION_X, REGION_Y, REGION_W, REGION_H))
    
    # In BGR-Format
    screenshot_bgr = cv2.cvtColor(np.array(screenshot_region), cv2.COLOR_RGB2BGR)
    
    # In Graustufen
    screenshot_gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # Template Matching
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    
    if max_val >= threshold:
        h, w, _ = template.shape
        # Offset in globalen Bildschirmkoordinaten
        click_x = REGION_X + max_loc[0] + w // 2
        click_y = REGION_Y + max_loc[1] + h // 2
        
        logging.info(f"Symbol gefunden (max_val={max_val:.2f}). Klicke auf ({click_x}, {click_y}).")
        pyautogui.click(click_x, click_y)
        
        time.sleep(1)
    else:
        logging.info(f"Symbol nicht gefunden (max_val={max_val:.2f}).")
        time.sleep(0.5)
