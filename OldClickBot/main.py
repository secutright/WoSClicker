### File List:
### main.py: Main loop, checks screenshots through each loop for certain items, then respond as needed
### imageDetection.py: Exposes a Vision class, essentially a wrapper for all opencv functions
### windowCapture.py: Exposes WindowCapture class, is responsible for communicating with windows gui to take screenshots
### bot.py: Handles click events, will eventually move more of the response logic in to here
### screenshotter.py: Just there to capture screenshots and save to file on a timer for future use with machine learning

import cv2 as cv
import time
from OldClickBot.bot import Bot
from windowCapture import WindowCapture
from OldClickBot.imageDetection import Vision

# DEBUG = True will show computer vision output to see what opencv is seeing and will output FPS each loop
DEBUG = False

wincap = WindowCapture('BlueStacks App Player')
helpAllBot = Bot((wincap.offset_x, wincap.cropped_y),(wincap.w, wincap.h))
reconnectBot = Bot((wincap.offset_x, wincap.cropped_y),(wincap.w, wincap.h))
loopTime = time.time()

originalssheight = 1475
scale = wincap.h / originalssheight

vision_allianceBtn = Vision('images\\AllianceBtn.png', scale)
vision_allianceHelpBtn = Vision('images\\AllianceHelp.png', scale)
vision_helpAllBtn = Vision('images\\HelpAllBtn.png', scale)
vision_reconnectBtn = Vision('images\\reconnectBtn.png', scale)
vision_exitBtn = Vision('images\\Exit.png', scale)
# vision_backArrow = Vision('images\\BackArrow.png')

while(True):
    # Capture screen
    screenshot = wincap.get_screenshot()

    # Detect Objects
    helpAllBtnRect = vision_helpAllBtn.find(screenshot, 0.8)
    reconnectBtnRect = vision_reconnectBtn.find(screenshot, 0.8)


    # Get click points from detection
    helpAllBtnPoints = vision_helpAllBtn.get_click_points(helpAllBtnRect)
    reconnectBtnPoints = vision_reconnectBtn.get_click_points(reconnectBtnRect)

    # If Help All button is available, click it with Bot.click()
    if len(helpAllBtnPoints) > 0:
        helpAllBot.click(helpAllBtnPoints[0])
        time.sleep(0.5)

    if len(reconnectBtnPoints) > 0:
        # Waiting 5 minutes to reconnect
        initialReconnectSleep = 1200
        print(f'Waiting {initialReconnectSleep/60} minutes to reconnect')
        time.sleep(initialReconnectSleep)

        # Click reconnect Button
        print('Clicking reconnect button')
        reconnectBot.click(reconnectBtnPoints[0])
        time.sleep(1)

        # Take Screenshot, look for exit button, and click
        screenshot = wincap.get_screenshot()
        exitBtnRects = vision_exitBtn.find(screenshot, 0.9)
        exitBtnPoints = vision_exitBtn.get_click_points(exitBtnRects)

        if DEBUG:
            output_image = vision_exitBtn.draw_rectangles(screenshot, exitBtnRects)
            cv.imshow('Matches', output_image)

        if len(exitBtnRects) > 0:
            reconnectBot.click(exitBtnPoints[0])
        else:
            print('Exit Button not found!')
        time.sleep(1)

        # Take a new capture and find alliance button
        screenshot = wincap.get_screenshot()
        allianceBtnRects = vision_allianceBtn.find(screenshot, 0.8)
        allianceBtnPoints = vision_allianceBtn.get_click_points(allianceBtnRects)

        if DEBUG:
            output_image = vision_allianceBtn.draw_rectangles(screenshot, allianceBtnRects)
            cv.imshow('Matches', output_image)

        if len(allianceBtnPoints) > 0:
            reconnectBot.click(allianceBtnPoints[0])
        else:
            print('Alliance Button not found!')
        time.sleep(1)

        # Find and click Help button
        screenshot = wincap.get_screenshot()
        allianceHelpBtnRects = vision_allianceHelpBtn.find(screenshot, 0.8)
        allianceHelpBtnPoints = vision_allianceHelpBtn.get_click_points(allianceHelpBtnRects)

        if DEBUG:
            output_image = vision_allianceHelpBtn.draw_rectangles(screenshot, allianceHelpBtnRects)
            cv.imshow('Matches', output_image)

        if len(allianceHelpBtnPoints) > 0:
            reconnectBot.click(allianceHelpBtnPoints[0])
        else:
            print('Alliance Help Button not found!')
        time.sleep(1)


    if DEBUG:
        # Draw detection results and display them
        output_image = vision_helpAllBtn.draw_rectangles(screenshot, helpAllBtnRect)
        cv.imshow('Matches', output_image)
        output_image = vision_reconnectBtn.draw_rectangles(screenshot, reconnectBtnRect)
        cv.imshow('Matches', output_image)
        print(f'FPS: {1/(time.time()-loopTime)}')
        loopTime = time.time()
        #print(f'Scale: {scale}')
                          
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')