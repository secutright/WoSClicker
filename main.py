import shared
import cv2 as cv
from time import time
from windowCapture import WindowCapture
from imageDetection import Vision

wincap = WindowCapture('BlueStacks App Player')
print('ssheight: ' + str(shared.ssheight))
vision_allianceBtn = Vision('images\\AllianceBtn.png')
vision_allianceHelpBtn = Vision('images\\AllianceHelp.png')
vision_backArrow = Vision('images\\BackArrow.png')
vision_helpAllBtn = Vision('images\\HelpAllBtn.png')
#vision_back = Vision('BackButtonUnscaled.png')

while(True):
    # Capture screen
    screenshot = wincap.get_screenshot()

    # Detect Objects
    rectangles = vision_allianceBtn.find(screenshot, 0.8)
    # pointsAllianceHelpBtn = vision_allianceHelpBtn.find(screenshot, 0.8)
    # pointsBackArrow = vision_backArrow.find(screenshot, 0.8)
    # pointsHelpAllBtn = vision_helpAllBtn.find(screenshot, 0.8)
    # points = vision_back.find(screenshot, 0.7, 'points')

    # Draw detection results
    output_image = vision_allianceBtn.draw_rectangles(screenshot, rectangles)

    # Display image with markers
    cv.imshow('Matches', output_image)

    loop_time = time()

    print('FPS {}'.format(1 / (time() - loop_time)))
                          
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')