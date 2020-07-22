'''
Render module

The purpose of this module is to aid with the rendering of the frames, masks and other recuring elements used on the other scripts

KNOWN BUGS:
-renderVideo() may sometimes render a black video or nothing at all [may have to do with color flag?]
-trusting the user too much

TODO:
-generalize renderVideo() to admit other formats besides .avi
-provide proper documentation to functions

AUTHOR & LICENSE DETAILS:

[Author]   Sergio Solé
[Email]    sergio.sole99@gmail.com
[Discord]  Steve from Customer Service#6001

License details can be found on license file of this repo at https://github.com/FalkenStein42/face-expressions


'''

import cv2 as cv
import numpy as np
import math
import os
from python_settings import settings as s



def renderFrames(frame_o,BLUR,HSV,THRESH=1):
    '''
    !Docstring!
    Function takes as input the original frame [frame_o] and a list of parameters for rendering
    each sub-frame [BLUR,HSV] and a flag for wether to aply a threshold to the end result [THRESH]
    
    *[BLUR] = [BLUR_KERNEL, BLUR_SIGMA]
    *[HSV]  = [ [H_LOW,S_LOW,V_LOW] , [H_HIGH,S_HIGH,V_HIGH] ]
    *[THRESH] --> 1 - True  ; 0 - False
    **Threshold to apply is 0,255 on a grayscale of the frame

    ##RETURN
    [frame_blur,frame_masked,frame_threshold]
    
    '''
    
    frames = []

    #Render Blur - [BLUR_KERNEL, BLUR_SIGMA]
    frame_blur = cv.GaussianBlur(frame_o,(BLUR[0],BLUR[0]),BLUR[1])
    frames.append(frame_blur)    
    #Render HSV Mask - [ [H_LOW,S_LOW,V_LOW] , [H_HIGH,S_HIGH,V_HIGH] ]
    mask = cv.inRange(cv.cvtColor(frame_blur,cv.COLOR_BGR2HSV),np.array([HSV[0][0],HSV[0][1],HSV[0][2]]),np.array([HSV[1][0],HSV[1][1],HSV[1][2]]))
    frame_masked = cv.bitwise_and(frame_blur,frame_blur,mask=mask)
    frames.append(frame_masked)
    #Render Gray
    frame_gray = cv.cvtColor(frame_masked,cv.COLOR_BGR2GRAY)
    #Render Threshold
    _,frame_threshold = cv.threshold(frame_gray,0,255,0)
    frames.append(frame_threshold)

    return frames


def renderVideo(settings_file = 'default_settings',output_file = 'output.avi'):

    os.environ["SETTINGS_MODULE"] = settings_file
    
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    renderer = cv.VideoWriter(output_file, fourcc, 20.0, (1920,  1080),isColor=False)

    vid = cv.VideoCapture(s.VIDEO)

    print('Rendering',s.VIDEO,'...')
    while vid.isOpened():
        
        ret, frame = vid.read()
        if not ret:
            break
        
        frame_out = renderFrames(frame,[s.BLUR_KERNEL,s.BLUR_SIGMA],[[s.H_LOW,s.S_LOW,s.V_LOW],[s.H_HIGH,s.S_HIGH,s.V_HIGH]],1)[2]
        
        renderer.write(frame_out)
        
        if cv.waitKey(1) == ord('q'):
            break
        
    print('Done!')
    cam.release()
    out.release()











    
