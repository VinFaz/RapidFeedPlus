import os
import tkinter
from tkinter import filedialog
from tkinter import *
from tkinter.font import Font
global RapidSpeed
Version = "0.5"
LineRead = []
NewWrite = []
RapidSections = ['']
HeightMap = []
# get file and add F(num) to all G0s


def getFileInfo(): #Open file, read its contnents and find the length of the file
    global filename
    filename = filedialog.askopenfilename()
    global file
    file = open(filename, "r")
    global LineRead
    LineRead = file.readlines()
    global MaxRead
    MaxRead = len(LineRead)
    print("File: " + filename)
    print("File Length: " + str(MaxRead))
    implabel.config(text=filename)


def selectExp(): #Get New File Path
    global newfilename
    newfilename = filename.split("/")
    newfilename = str(newfilename[len(newfilename) - 1])[:-3] + "(Rapid)" #make the new file name by splitting the origional and adding (Rapid) to the end
    global newfilepath
    newfilepath = filedialog.askdirectory()
    newfilepath =  newfilepath + "/" + newfilename #create new file location
    print(newfilepath)
    explabel.config(text=("File Exported to: " + newfilepath))
    zmap()


def zmap(): #A List of 0s and 1s to refer to when adding higher feedrates (if the value is 0, the cnc head is below Z=0)
    LastZ = 0
    HeightMap.append(0)
    for j in range(MaxRead):
        if LineRead[j].find("Z") != -1 & LineRead[j].find("(") == -1: #detecting whether there is a valid Z declaration in the line
            Zplace = LineRead[j].find("Z")
            if getZHeight(LineRead[j], LineRead[j].find("Z"), j) >= float(0):
                HeightMap.append(1)
                LastZ = 1
                print("List# " + str(j) + ": " + str(LastZ))
            else:
                HeightMap.append(0)
                LastZ = 0
                print("List# " + str(j) + ": " + str(LastZ))
        else:
            HeightMap.append(LastZ)
            print("List# " + str(j) + ": " + str(LastZ))
    print(HeightMap)
    print("Length: " + str(len(HeightMap)))
    file.close()
    createFile()


def getZHeight(rawZ, zPlace, row):
    rawZ = float(rawZ.strip()[(zPlace + 1):].split(" ")[0]) #quick function for tidiness
    return rawZ


def createFile(): #apply the zmap list and change G1 values to G0s
    print("Magically Creating New Gcode!")
    for i in range(MaxRead):
        if HeightMap[i + 1] == 0:
            NewWrite.append(LineRead[i].strip() + " ;Z < 0\n")
            print("List# " + str(i) + " (HeightMap: " + str(HeightMap[i]) + ") " + NewWrite[i].strip())
        if(HeightMap[i + 1] == 1):
            if (LineRead[i].find("X") == 0 or LineRead[i].find("Y") == 0) and (LineRead[i].find("Z") == -1 & LineRead[i].find("F") == -1):
                NewWrite.append("G0 " + LineRead[i].strip() + " ;Added G0\n")
                print("List# " + str(i) + " (HeightMap: " + str(HeightMap[i]) + ") " + NewWrite[i].strip())
            elif LineRead[i].find("G1 ") == 0 and LineRead[i].find("Z") == -1 and LineRead[i].find("F") == -1:
                NewWrite.append(LineRead[i].strip().replace("G1 ", "G0 ") + " ;Replaced G1\n")
                print("List# " + str(i) + " (HeightMap: " + str(HeightMap[i]) + ") " + NewWrite[i].strip())
            else:
                NewWrite.append(LineRead[i].strip() + " ;Else Category\n")
                print("List# " + str(i) + " (HeightMap: " + str(HeightMap[i]) + ") " + NewWrite[i].strip())
    print("New Gcode Length: " + str(len(NewWrite) + 1))
    NewWrite.insert(0, "G0 F" + str(RapidSpeed.get()) + " ;RapidFeedPlus Rapid Feed Value\n")
    exportFile()


def exportFile(): #check if file exists than create new file and write Gcode to it
    if os.path.exists(newfilepath) == False:
        print("Exporting!")
        global newfile
        newfile = open(newfilepath, "w")
        newfile.writelines(NewWrite)
        newfile.close()
    else:
        print("File Exists")
        explabel.config(text="File Exists!")


#Tkinter setup
app = tkinter.Tk()
text = tkinter.Text(app)
mainfont = Font(family="Exo", size=20, weight="bold")


#Var setup
var = tkinter.BooleanVar()


#Tkinter window
app.title("RapidFeedPlus")
app.configure(bg="#363636")
app.iconphoto(False, PhotoImage(file="RapidSpeedIcon.png"))
app.resizable(width=False, height=False)
RapidSpeed = Entry(app, bg="#8f8f8f", fg="#d9d9d9", font=mainfont)
impfile = Button(app, text="Import File", command=getFileInfo, bg="#616161", fg="#d9d9d9", font=mainfont)
SpeedLabel = Label(text="Rapid Speed (mm/min)", bg="#363636", fg="#d9d9d9", font=mainfont)
implabel = Label(text=getFileInfo, fg="#d9d9d9", bg="#363636")
expfile = Button(app, text="Export File", command=selectExp, bg="#414141", fg="#d9d9d9", font=mainfont)
explabel = Label(text=selectExp, fg="#d9d9d9", bg="#363636")


#Ordering of Buttons/Interactive modules
SpeedLabel.pack()
RapidSpeed.pack()
impfile.pack()
implabel.pack()
expfile.pack()
explabel.pack()
app.mainloop()

