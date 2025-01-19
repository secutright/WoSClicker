import cv2 as cv
from time import time
from windowCapture import WindowCapture
from imageDetection import Vision

originalssheight = 1475

wincap = WindowCapture('BlueStacks App Player')
vision_allianceBtn = Vision('images\AllianceBtn.png')
vision_allianceHelpBtn = Vision('images\AllianceHelp.png')
vision_backArrow = Vision('images\BackArrow.png')
vision_helpAllBtn = Vision('images\HelpAllBtn.png')
#vision_back = Vision('BackButtonUnscaled.png')

while(True):
    screenshot, ssheight = wincap.get_screenshot()

    print(ssheight)
    scale = ssheight / originalssheight
    print('Scale = ' + str(scale))
    pointsAllianceBtn = vision_allianceBtn.find(screenshot, scale, 0.8, 'rectangles')
    pointsAllianceHelpBtn = vision_allianceHelpBtn.find(screenshot, scale, 0.8, 'rectangles')
    pointsBackArrow = vision_backArrow.find(screenshot, scale, 0.8, 'rectangles')
    pointsHelpAllBtn = vision_helpAllBtn.find(screenshot, scale, 0.8, 'rectangles')
    # points = vision_back.find(screenshot, 0.7, 'points')


    loop_time = time()

    print('FPS {}'.format(1 / (time() - loop_time)))

                          
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')