import cv2 as cv
import numpy as np

def filterByArea(contours,minArea):
    cnt = []
    for cont in contours:
        if cv.contourArea(cont)>minArea:
            cnt.append(cont)
    return cnt


def findCenter(contours):
    centers = np.int16([[0,0]])
    # loop over the contours
    for c in contours:
            # compute the center of the contour
        M = cv.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centers = np.append(centers,[[cX,cY]],axis=0)
    #delete initializer element
    return np.delete(centers,0,axis=0)

#######

src = cv.VideoCapture('C:\\Workspace\\Python\\CV2\\output.avi')
first = 1
#cv.namedWindow('point', flags=cv.WINDOW_NORMAL)
while(1):
    _, frame = src.read()
    if not _:
        break
    contours, hierarchy = cv.findContours(cv.cvtColor(frame, cv.COLOR_BGR2GRAY), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    f_cont = filterByArea(contours,25)
    centers = findCenter(f_cont)
    if first:
        first_c = centers[0]
        first = 0
    movement = (centers[0]-first_c)[1]/500
    print(movement)
    #cv.circle(frame,(centers[0][0],centers[0][1]),5,[255,0,0],10)
    #cv.imshow('point',frame)
    #k = cv.waitKey(1) & 0xFF
    #if k == 27:
    #    break












##OLD FILE##
'''
img1 = cv.imread('face1.png',0)
img2 = cv.imread('face2.png',0)

contours1, hierarchy1 = cv.findContours(img1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cnt1 = contours1[4]
cv.drawContours(img1, [cnt1], 0, (0,255,0), 3)

contours2, hierarchy2 = cv.findContours(img1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cnt2 = contours2[4]
cv.drawContours(img2, [cnt2], 0, (0,255,0), 3)

cv.imshow('A',img1)
cv.imshow('B',img2)
cv.waitKey(0)
cv.destroyAllWindows()


def nothing(x):
    pass

#cv.createTrackbar('area_min','Params',0,255,nothing)
im = cv.imread('face1.png')
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
#ret, thresh = cv.threshold(im, 127, 255, 0)
contours, hierarchy = cv.findContours(imgray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
a = np.zeros(im.shape)

cnt = []
for cont in contours:
    if cv.contourArea(cont)>16:
        cnt.append(cont)
cv.drawContours(im, cnt, -1, (0,255,0), 1)

cv.imshow('A',im)
cv.waitKey(0)
cv.destroyAllWindows()
'''
