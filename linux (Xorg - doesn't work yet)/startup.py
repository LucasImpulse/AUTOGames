from tkinter import Tk, Label; import tkinter as tk; import time, time_lang, launch_connect
haha = "Hello."
print(Tk, Label)
print(time)
print(haha)





def StartUp():

#IF THIS PROGRAM HAS ALREADY BEEN SETUP, SKIP TO LINE 36 (change when necessary), the program checks this by looking for an existing and valid lock file.

    root = Tk()

#time_lang.firstTimeConfig()

#Add a window of defined size that could fit on any screen, even the smallest.
#STARTUP WINDOW 1

#WINDOW 1 PAGE 1

#Put on that window's left an image of what our program logo is.
#On the window's right a text that welcomes, summarises program, and asks press next to setup, back to go back or cancel to cancel.
#Bottom right, next-back-cancel button, in the order that the << leftOrRight bool variable from time-and-lang module >> defines.

#WINDOW 1 PAGE 2

#Tell the user that a launcher connector is about to launch.
#launch-connect.py >>> initLaunchConnect(int(0)) 0 is the integer that means this is first time.
#wait for return.

#WINDOW 1 CLOSE

#TELL main.py TO START MAIN WINDOW >>> resizable.

#END OF startup.StartUp()





print("Finished!")
time.sleep(3)