# Class that handles bot functions using YOLO model predictions and PyAutoGUI

import time
import pyautogui
import threading
from ultralytics import YOLO
from windowCapture import WindowCapture

class YOLOBot:
    # Properties
    wincap = WindowCapture('BlueStacks App Player')
    model = YOLO(r'res\bestV4.pt')
    offset_x = 0
    offset_y = 0
    model_output = []
    help_clicks = 0
    # Thread variables
    lock = None
    run_model_stop = 0
    help_heal_bot_stop = 0

    # __init__ class, runs on class instantiation
    def __init__(self):
        self.offset_x = self.wincap.offset_x    # Gather window offset to calculate click points
        self.offset_y = self.wincap.offset_y
        self.lock = threading.Lock()            # Create a threading lock
        self.start_run_model()                  # Start the run_model thread

    def get_click_position(self, x, y):
        return((x + self.offset_x, y + self.offset_y)) # Returns calculated click positions with offsets
    
    def click(self, x, y):          # Function that handles click functions
        pyautogui.moveTo(x=x, y=y)  # Move cursor to x/y coordinate
        pyautogui.click()           # Click left mouse button
        time.sleep(0.25)            # Sleep for 0.25s to give the model a chance to update
    
    def start_run_model(self):      # Thread wrapper for run_model function
        self.run_model_stop = 0                                         # Set stop variable to run
        self.run_model_thread = threading.Thread(target=self.run_model) # Create thread for run_model
        self.run_model_thread.start()                                   # Start the thread

    def stop_run_model(self):           # Ends thread for run_model function
        self.run_model_stop = 1         # Set stop code to 1 to break loop
        self.run_model_thread.join()    # Wait for thread to close
    
    def run_model(self):                # Function responsible for gathering model data from screenshots
        while self.run_model_stop == 0: # Loop while stop code == 0
            # print('Updating Model')     
            screenshot = self.wincap.get_screenshot() # Get a screenshot

            results = self.model([screenshot], conf=0.80, save=False, verbose=False) # Run the screenshot through the YOLO model

            boxes = results[0].boxes.xyxy.tolist()  # List the xy coordinates of found items
            classes = results[0].boxes.cls.tolist() # List the classes of found items
            names = results[0].names                # List the class-name index

            newlist = []                            # Create a placeholder list
            for box, cls in zip(boxes, classes):    # Zip the rectangles and classes together and loop through
                x1, y1, x2, y2 = box                # Break rectangle points tuple to individual variables              
                center_x = (x1+x2) / 2              # Calculate center of rectangles
                center_y = (y1+y2) / 2

                name = names[int(cls)]              # Match the class from boxes to a 'friendly' name

                click_x, click_y = self.get_click_position( # Get click postions with proper offsets
                    center_x, center_y)

                output = (name, (click_x, click_y)) # Build the output list tuple
                newlist.append(output)              # Append the output tuple to the placeholder list

            self.lock.acquire()                     # Aquire thread lock to prevent data corruption
            self.model_output = newlist             # Overwrite class property with placeholder data
            self.lock.release()                     # Release the thread lock

    def start_help_heal_bot(self):                  # Thread wrapper for help_heal_bot function
        self.help_heal_bot_stop = 0
        self.help_heal_bot_thread = threading.Thread(target=self.help_heal_bot)
        self.help_heal_bot_thread.start()

    def stop_help_heal_bot(self):
        self.help_heal_bot_stop = 1
        self.help_heal_bot_thread.join()

    def help_heal_bot(self):                        # Help/Heal bot, looks for the Heal Button, Request Help Button,
                                                    # Alliance "Help Hands", then Heal All button in that order
        while self.help_heal_bot_stop == 0:         # Loop while stop code == 0

            # print('Obtaining model data')
            self.lock.acquire()                     # Aquire thread lock
            model_data = self.model_output          # Assign data from Class Property to local variable
            self.lock.release()                     # Release thread lock
            # print(model_data)
            for i in model_data:                    # Iterate through data
                name = i[0]                         # Break tuple in to variables
                x = i[1][0]
                y = i[1][1]

                # print(f'name: {name} x: {x} y: {y}')
                
                if name == 'healButton':                # Act on data based on name
                    print('Clicking healButton')
                    self.click(x, y)

                elif name == 'requestHelpBtn':
                    print('Clicking requestHelpBtn')
                    self.click(x, y)

                elif name == 'helpHand':
                    print('Clicking helpHand')
                    self.click(x, y)
                    self.help_clicks += 1
                    print(f'Helped {self.help_clicks} times')

                elif name == 'helpAllBtn':
                    print('Clicking Help All Button')
                    self.click(x, y)
                    self.help_clicks += 1
                    print(f'Helped {self.help_clicks} times')

            time.sleep(0.1)                         # Sleep for 0.1 seconds to give other threads a chance to run