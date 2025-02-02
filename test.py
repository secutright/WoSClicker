# Just a simple launcher to test various bot functions
import time
from YOLOBot import YOLOBot

yolo = YOLOBot()
yolo.start_help_heal_bot()
time.sleep(5)
yolo.stop_help_heal_bot()
yolo.stop_run_model()