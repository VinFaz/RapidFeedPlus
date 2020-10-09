import time
import random
import math
import tkinter
from tkinter import Label, Button, Entry, PhotoImage
from tkinter import filedialog
from tkinter import *
from tkinter.font import Font
global RapidSpeed
global updateWindow
updateWindow = True

#get file and add F(num) to all G0s
def RapidFeedMod():
    print("Rapid Feed: " + RapidSpeed.get())
    if len(RapidSpeed.get()) != 0:
        RapidFeedSpeed = RapidSpeed.get()
        global file
        file = open(filename, "r+")
        global LineRead
        LineRead = file.readlines()
        print(LineRead[0])
        LineRead[0] = str(LineRead[0].strip())[:-2] + ' (Rapid)")' + "\n"
        LineRead[5] = "; WE WILL NEVER PAY FOR SERVICES THAT ARE PROBABLY WORTH THE MONEY! NEVER! SCREW YOU FUSION 360! \n"
        MaxRead = LineRead.__len__()
        print("File Length: " + str(MaxRead))
        for i in range(MaxRead - 1):
            currentLine = LineRead[i]
            if currentLine[:2] == "G0":
                print("G0 at line " + str(i + 1))
                LineRead[i] = LineRead[i].strip() + " F" + str(RapidFeedSpeed) + "\n"
    newFile()
def newFile():
    newfile = open(filename + " (Rapid)", "w+")
    global newfilename
    newfilename = newfile.name
    newfile.writelines(LineRead)
    explabel.config(text=newfilename)
    file.close()
    print("File Closed!")

def setFileName():
    global filename
    filename = filedialog.askopenfilename()
    print(filename)
    implabel.config(text=filename)

#Tkinter window
app = tkinter.Tk()
text = tkinter.Text(app)
mainfont = Font(family="Exo", size=20, weight="bold")
app.title("Rapid Feed-ifier")
app.configure(bg="#363636")
app.iconphoto(False, PhotoImage(file="D:\Pictures\Py Projects\Rapid Speed Restoration\Drill_bit-512.png"))
app.resizable(width=False, height=False)
RapidSpeed = Entry(app, bg="#8f8f8f", fg="#d9d9d9", font=mainfont)
impfile = Button(app, text="Import File", command=setFileName, bg="#616161", fg="#d9d9d9", font=mainfont)
SpeedLabel = Label(text="Rapid Speed (mm/min)", bg="#363636", fg="#d9d9d9", font=mainfont)
implabel = Label(text=setFileName, fg="#d9d9d9", bg="#363636")
expfile = Button(app, text="Export File", command=RapidFeedMod, bg="#414141", fg="#d9d9d9", font=mainfont)
explabel = Label(text=newFile, fg="#d9d9d9", bg="#363636")

#Ordering of Buttons/Interactive modules
SpeedLabel.pack()
RapidSpeed.pack()
impfile.pack()
implabel.pack()
expfile.pack()
explabel.pack()
app.mainloop()


