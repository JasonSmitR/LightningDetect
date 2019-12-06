import sys #import the system
import os
import cv2 #openCV
import glob
import numpy as np
from PIL import Image, ImageTk
import datetime
import tkinter


SCALE = 0.5
NOISE_CUTOFF = 5
BLUR_size = 3
treshold = 38000

#taken from http://lukse.lt/uzrasai/2015-05-lightning-strikes-and-python/
def count_diff(img1, img2):
    small1 = cv2.resize(img1, (0,0), fx=SCALE, fy=SCALE)
    small2 = cv2.resize(img2, (0,0), fx=SCALE, fy=SCALE)
    #gray1 = cv2.cvtColor(small1, cv2.COLOR_BGR2GRAY)
    #gray2 = cv2.cvtColor(small2, cv2.COLOR_BGR2GRAY)
    #mask = cv2.compare(gray1, gray2, cv2.CMP_GT)
    diff = cv2.absdiff(small1,small2)
    diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    frame_delta1 = cv2.threshold(diff, NOISE_CUTOFF, 255, 3)[1]
    delta_count1 = cv2.countNonZero(frame_delta1)
    return delta_count1
##############################################################################

def waitFunc():
    for x in range(10):
        flag, image1 = video_source.read()
        image2 = image1
        return True
##############################################################################
def validDevice(source):
    ans = cv2.VideoCapture(source) 
    if ans is None or not ans.isOpened():
       return False
    else:
       return True
       
##############################################################################


totalStrikes = 0

f = open("outputLog.txt", "w")
if len(sys.argv) < 2:
    display = tkinter.Tk()
    for camera in range(len(glob.glob("/dev/video?"))):
        print(camera)
        if validDevice(camera):
            c = cv2.VideoCapture(camera)
            flag, image1 = c.read()
            b,g,r = cv2.split(image1)
            img = cv2.merge((r,g,b))
            im = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=im)
            tkinter.Label(display, image=imgtk).pack()
            c.release()
    display.mainloop() 
    #need to add click selection here
    video_source = cv2.VideoCapture(0) #use the default camera if no file specified, change as req
    #video_source = cv2.VideoCapture(path + '/' +filename) #for testing  purposes 
else:
    #video_source = cv2.VideoCapture(sys.argv[1]) 
    video_source = cv2.VideoCapture(path + '/' +filename)
    #Should run a for loop here over each file in dir    
checkForStrike = True
flag, image1 = video_source.read()
strikes = 'nan'
if flag:
    strikes = 0
    while checkForStrike:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        flag, image2 = video_source.read()
        if not flag:
           break
        diff1  = count_diff(image1, image2)
        if diff1 > treshold : #The frames are very different then'
            #action function called here
            strikeTime = datetime.datetime.now().strftime("%y-%m-%d %H_%M_%S_%f")
            os.mkdir(strikeTime)
            outputPath = os.getcwd() + '/' + strikeTime
            cv2.imwrite(outputPath+'/'+'img1.png',image1)
            cv2.imwrite(outputPath+'/'+'img2.png',image2)
            strikes = strikes + 1
            totalStrikes = totalStrikes + 1
            string = str(strikeTime)+'\n'
            f.write(string)
            image1=image2; #prepare for next round
            checkForStrike = False
            checkForStrike = waitFunc()
                    
video_source.release()
cv2.destroyAllWindows()
f.close()
exit()
