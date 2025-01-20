import pyautogui

class Bot:
    # Properties
    HelpClicks = 0

    def __init__(self, window_offset, window_size):
        self.window_offset = window_offset
        self.window_w = window_size[0]
        self.window_h = window_size[1]

    def get_screen_position(self, pos):
        return (pos[0] + self.window_offset[0], pos[1] + self.window_offset[1])
    
    def click(self, target):
        screen_x, screen_y = self.get_screen_position(target)
        print(f'Moving Mouse to X:{screen_x} Y:{screen_y}')
        pyautogui.moveTo(x=screen_x, y=screen_y)
        pyautogui.click()
        print('Clicked')