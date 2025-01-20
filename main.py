### TODO: Create debug flag to stop imshow abd terminal for production run.

from bot import Bot
import cv2 as cv
import time
from windowCapture import WindowCapture
from imageDetection import Vision

wincap = WindowCapture('BlueStacks App Player')
helpAllBot = Bot((wincap.offset_x, wincap.cropped_y),(wincap.w, wincap.h))
reconnectBot = Bot((wincap.offset_x, wincap.cropped_y),(wincap.w, wincap.h))

originalssheight = 1475
scale = wincap.h / originalssheight

# vision_allianceBtn = Vision('images\\AllianceBtn.png')
# vision_allianceHelpBtn = Vision('images\\AllianceHelp.png')
# vision_backArrow = Vision('images\\BackArrow.png')
vision_helpAllBtn = Vision('images\\HelpAllBtn.png', scale)
vision_reconnectBtn = Vision('images\\reconnectBtn.png', scale)
#vision_back = Vision('BackButtonUnscaled.png')

while(True):
    # Capture screen
    screenshot = wincap.get_screenshot()

    # Detect Objects
    helpAllBtnRect = vision_helpAllBtn.find(screenshot, 0.8)
    reconnectBtnRect = vision_reconnectBtn.find(screenshot, 0.8)

    # Get click points from detection
    helpAllBtnPoints = vision_helpAllBtn.get_click_points(helpAllBtnRect)
    reconnectBtnPoints = vision_reconnectBtn.get_click_points(reconnectBtnRect)

    # Draw detection results
    output_image = vision_helpAllBtn.draw_rectangles(screenshot, helpAllBtnRect)

    # Display image with markers
    cv.imshow('Matches', output_image)

    # If Help All button is available, click it with Bot.click()
    if len(helpAllBtnPoints) > 0:
        helpAllBot.click(helpAllBtnPoints[0])
        time.sleep(0.5)

    if len(reconnectBtnPoints) > 0:
        reconnectBot.click(reconnectBtnPoints[0])
        time.sleep(0.5)

    # loop_time = time()
    # print('FPS {}'.format(1 / (time() - loop_time)))
                          
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')