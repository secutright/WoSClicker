import cv2 as cv
import numpy as np


class Vision:

    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None
    originalssheight = 1475

    # constructor
    def __init__(self, needle_img_path, scale, method=cv.TM_CCOEFF_NORMED):
        # load the needle image
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_GRAYSCALE)
        self.needle_img = cv.resize(self.needle_img, None, fx=scale, fy=scale)
        # Save the dimensions of the needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, threshold=0.5):
        haystack_img = cv.cvtColor(haystack_img, cv.COLOR_BGR2GRAY)
        # Run matchTemplate
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # Return if no results
        if not locations:
            return np.array([], dtype=np.int32).reshape(0,4)

        # Create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        return rectangles
    
    def get_click_points(self, rectangles):

        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Save the points
            points.append((center_x, center_y))

        return points
    
    def draw_rectangles(self, haystack_img, rectangles):

        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # Break in to top left and bottom right
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # Draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                         lineType=line_type, thickness=2)
        
        return haystack_img
        
    def draw_crosshairs(self, haystack_img, points):
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            cv.drawMarker(haystack_img, (center_x, center_y), 
                        marker_color, marker_type, 
                        markerSize=40, thickness=2)
            
        return haystack_img