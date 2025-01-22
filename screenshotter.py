import pygetwindow as gw
import pyautogui
import cv2 as cv
import numpy as np
import time

try:
    window_title = "Bluestacks App Player"
except Exception as e:
    print(f'Error finding window: {e}')

# Screenshot offsets
offset_x = 0
offset_y = 50
offset_w = -50
offset_h = -50

# Capture window location and save to 4 variables
window = gw.getWindowsWithTitle(window_title)[0]
x, y, w, h = window.left, window.top, window.width, window.height

# Apply Offsets
x += offset_x
y += offset_y
w += offset_w
h += offset_h

i = 0
while True:
    now = time.strftime('%y%m%d%H%M%S')
    file = f'screenshots\\screen-{now}.jpg'
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv.cvtColor(screenshot_np, cv.COLOR_RGB2BGR)
    cv.imshow('result', screenshot_bgr)
    cv.imwrite(file, screenshot_bgr)
    i += 1
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows
        break