import threading
from tkinter import IntVar
import ttkbootstrap as tkb
from YOLOBot import YOLOBot

yolo = YOLOBot()

def on_help_heal_chk_toggle():
    help_heal_thread = threading.Thread(target=yolo.help_heal_bot)
    print(type(help_heal_thread))

    print(f'run_help_heal: {run_help_heal.get()}')   
    if run_help_heal.get() == 1:
        print('Starting Help/Heal Bot Thread')
        yolo.start_help_heal_bot()
        print('Help/Heal Bot Started!')
    elif run_help_heal.get() == 0:
        print('Stopping Help/Heal Bot Thread')
        yolo.stop_help_heal_bot()
        print('Help/Heal Bot Stopped!')

root = tkb.Window('WosClickBot', 'solar', size=(400,300), position=(900,50))

run_help_heal = IntVar()

frame1 = tkb.Frame(root, padding=10).pack()

help_heal_chk = tkb.Checkbutton(frame1, 
                                text='Help/Heal Bot',
                                bootstyle='toolbutton', 
                                variable=run_help_heal,
                                command=on_help_heal_chk_toggle)

label1 = tkb.Label(frame1, text=f'run_help_heal: {run_help_heal.get()}')

def on_help_heal_chk_toggle():
    print(f'run_help_heal: {run_help_heal.get()}')
    label1.config(text=f'run_help_heal: {run_help_heal.get()}')

help_heal_chk.pack(pady=30, padx=40)
label1.pack()

root.mainloop()

yolo.stop_run_model()