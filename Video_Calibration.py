import numpy as np
import cv2 as cv
import render_helper
import os
from python_settings import settings

#SETTIINGS
    #READ SETTINGS
def readSettings(settings_file = 'default_settings'):
    
    os.environ["SETTINGS_MODULE"] = settings_file
    
    VIDEO = settings.VIDEO
    CROP_LEFT = settings.CROP_LEFT
    CROP_RIGHT = settings.CROP_RIGHT
    RESIZE = settings.RESIZE
    BLUR_KERNEL = settings.BLUR_KERNEL
    BLUR_SIGMA = settings.BLUR_SIGMA
    H_LOW = settings.H_LOW
    S_LOW = settings.S_LOW
    V_LOW = settings.V_LOW
    H_HIGH = settings.H_HIGH
    S_HIGH = settings.S_HIGH
    V_HIGH = settings.V_HIGH

    #WRITE SETTINGS
def writeSettings(settings_file='settings_1'):
    config = open(settings_file+'.py','w')
    
        #Write HSV
    cfg_line = ''
    for val in [H_LOW,S_LOW,V_LOW,H_HIGH,S_HIGH,V_HIGH]:
        cfg_line += '0'*(3-len(str(val))) + str(val) +','
    config.write(cfg_line+' #HSV LOW-HIGH\n')
    
        #Write Camera ID
    cfg_line = ''
    for val in [RESIZE]:
        cfg_line += '0'*(3-len(str(val))) + str(val) +'%'
    config.write(cfg_line+' #RESIZE %\n')
    
        #Write Crop
    cfg_line = ''
    for val in [CROP_LEFT, CROP_RIGHT]:
        cfg_line += '0'*(3-len(str(val))) + str(val) +','    
    config.write(cfg_line+' #CROP LEFT-RIGH\n')
    
        #Write Blur
    config.write(str(BLUR_KERNEL)+','+'0'*(2-len(str(val))) + str(val) +','' #BLUR KERNEL-SIGMA\n')
 



#TRACKBAR FUNCTIONS

def nothing(x):
    pass

#TRACKBAR CRATION FUNCTIONS

def createBlur():
    cv.namedWindow('Blur')
    cv.createTrackbar('Kernel Size','Blur',BLUR_KERNEL,5,nothing)
    cv.createTrackbar('Sigma','Blur',BLUR_SIGMA,50,nothing)

def createHSV():
    cv.namedWindow('HSV Mask adjustment')
    cv.createTrackbar('H-low','HSV Mask adjustment',H_LOW,180,nothing)
    cv.createTrackbar('S-low','HSV Mask adjustment',S_LOW,255,nothing)
    cv.createTrackbar('V-low','HSV Mask adjustment',V_LOW,255,nothing)
    cv.createTrackbar('H-high','HSV Mask adjustment',H_HIGH,180,nothing)
    cv.createTrackbar('S-high','HSV Mask adjustment',S_HIGH,255,nothing)
    cv.createTrackbar('V-high','HSV Mask adjustment',V_HIGH,255,nothing)

#--------------

#Start Video Capture Device
cam = cv.VideoCapture(VIDEO)
if type(cam):
    print('Video found')
else:
    exit()
    
frame_state, frame = cam.read()
vsize = frame.shape #get video size
#createCropFrame(vsize[1])

#Select frames
cam = cv.VideoCapture(VIDEO)
frames = []

print('Counting frames...')
i=0
while (frame_state): #get n of frames
    frame_state, frame = cam.read()
    i+=1
print('Video has',i,'frames')

print('Grabing 4 preview frames...')
cam = cv.VideoCapture(VIDEO)
for f in range(4): #get 4 preview frames
    for a in range(5+(int(i/4)*(f if (f==0) else 1))):#Salta hasta el fotograma a guardar
        cam.read()
    _, fr = cam.read()
    preview = cv.resize(fr,(int(vsize[1] * RESIZE/100),int(vsize[0] * RESIZE/100)))
    frames.append(preview)#Resize and add frame preview to list
del frame
vsize = frames[0].shape
print('Video Resized to: ',vsize[0],'x',vsize[1])

#PARAM SET LOOP
  #Create Filters
createBlur()
createHSV()

while(True):
        
  #Reads
   #Read Blur
    BLUR_KERNEL = 3+2*(cv.getTrackbarPos('Kernel Size','Blur'))
    BLUR_SIGMA = cv.getTrackbarPos('Gausian Sigma','Blur')
   #Read HSV trackbars
    H_LOW = cv.getTrackbarPos('H-low','HSV Mask adjustment')
    S_LOW = cv.getTrackbarPos('S-low','HSV Mask adjustment')
    V_LOW = cv.getTrackbarPos('V-low','HSV Mask adjustment')
    H_HIGH = cv.getTrackbarPos('H-high','HSV Mask adjustment')
    S_HIGH = cv.getTrackbarPos('S-high','HSV Mask adjustment')
    V_HIGH = cv.getTrackbarPos('V-high','HSV Mask adjustment')

    j=0
    for frame in frames:
        r_frame = render_helper.renderFrames(frame,[BLUR_KERNEL,BLUR_SIGMA],[[H_LOW,S_LOW,V_LOW],[H_HIGH,S_HIGH,V_HIGH]],1)    
    #Displays
        #(Comment out lines to disable a specific feed)
        cv.imshow('Frame'+str(j),frame)
        cv.imshow('Blur'+str(j),r_frame[0])
        cv.imshow('Mask'+str(j),r_frame[1])
        j+=1

   #Await kill key
    #
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

#Write settings & quit
cv.destroyAllWindows()
writeSettings()
