'''
Point Operations Module

The purpose of this module is to provide tools for computing poitn cluster distances and relations.
These allow for the identification and prediction of the positions of reference points on the model.

TODO:
-add 'lowest norm' mode to find closest and apply it to feature 20 - lo_mouth_node
-provide proper documentation to functions

AUTHOR & LICENSE DETAILS:

[Author]   Sergio Solé
[Email]    sergio.sole99@gmail.com
[Discord]  Steve from Customer Service#6001

License details can be found on license file of this repo at https://github.com/FalkenStein42/face-expressions


'''

import numpy as np
from math import atan as atan
from math import pi

    
def findCentralPoint(points):
    '''
    Implementation of the trimed algorithm for computing medioid of a collection of points
    '''
    low_bound = np.zeros(len(points))
    low_energy = 10**5
    #points.shuffle()
    for i in range(len(points)):
        if (low_bound[i]<low_energy):
            
            #Compute all distances to current point
            distance = np.array([])
            for j in range(len(points)):
                distance = np.append(distance,[np.linalg.norm(points[j]-points[i])])
                
            #Make energy of point its new bound
            low_bound[i] = (1/(len(points)-1)) * np.sum(distance)
            
            #If its lower than bound, make best candidate
            if (low_bound[i]<low_energy):
                best_i = i
                low_energy = low_bound[i]
            #Recalculate Bounds
            for j in range(len(points)):
                low_bound[j] = max(low_bound[j],abs(low_bound[i]-distance[j]))

    return points[best_i]


def findClosest(points, point, axis=-1, axis_mode='scope',axis_scope=90, orientation=0):
    '''
    axis 0 -> X
    axis 1 -> Y
    ...
    axis mode:
        scope     -  returns closest point within specified scope, that is, with an angle lower or equal to axis_mode/2
        weighted  -  returns point with lowest rating, with rating = norm(point) + (y**2/ymax)
    
    '''
    #print('---',point,'---')
    points = points-point #Shift origin to target
    points = np.delete(points, \
              np.where(points == [0,0])[0][0],axis=0) #Delete itself from the list (now transformed to [0,0]) if it exists
    #Check if axis orienrations are specified
    if(orientation):
        for i in range(len(orientation)): #Check orientation for each given axis
            if (orientation[i] == 1):
                points = points[np.where(points[:,i]>0)]
            elif (orientation[i] == -1):
                points = points[np.where(points[:,i]<0)]

    if(axis==-1):       #Check wether an axis was specified
        dist = np.linalg.norm(points,axis=1) #Make the vector norm array
        rating = dist   #Make the vector norm array the rating
        
    else:
        if axis_mode=='weighted':
            dist = np.linalg.norm(points,axis=1) #Make the vector norm array
            #Assign rating as a weighted sum of distance and axis coordinate
            weight = 0
            for i in range(points.shape[1]):  #calculate weights for al axes except target axis
                if i!= axis:
                    weight += abs(((points[:,i])**2)/np.amax(points[:,i]))
            rating = dist + weight                                       #Return elements wich correspond with the index of the

        elif axis_mode == 'scope':
            #print(points+point)
            angles = np.array([(abs(atan(p[int(not axis)]/p[axis])*180/pi)) for p in points]) #calculate angles of each point
            #print(angles)
            points = points[np.where(angles<(axis_scope/2))] #remove points outside of scope
            dist = np.linalg.norm(points,axis=1) #Make the vector norm array
            #print(dist)
            rating = dist #Make the vector norm array the rating

    return (points[np.where(rating == np.amin(rating))] + point) #normalized to global coordinates
            


            


def featureIdentification(points):
    '''
    Feature IDs:
    0 -  nose
    1 -  cheek_left
    2 -  cheek_right
    3 -  lo_eye_node
    4 -  lo_eye_l1
    5 -  lo_eye_l2
    6 -  lo_eye_l3
    7 -  lo_eye_r1
    8 -  lo_eye_r2
    9 -  lo_eye_r3
    10 - eyebrow_node
    11 - eyebrow_l1
    12 - eyebrow_l2
    13 - eyebrow_l3
    14 - eyebrow_r1
    15 - eyebrow_r2
    16 - eyebrow_r3
    17 - hi_mouth_node
    18 - hi_mouth_l
    19 - hi_mouth_r
    20 - lo_mouth_node
    21 - lo_mouth_l1
    22 - lo_mouth_l2
    23 - lo_mouth_r1
    24 - lo_mouth_r2
    
    '''
     
    #find nose as central point of cluster
    features = np.array([findCentralPoint(points)])
        #find cheek points on each side
    features = np.append(features,findClosest(points,features[0],axis=0,orientation=[-1]),axis=0)
    features = np.append(features,findClosest(points,features[0],axis=0,orientation=[1]),axis=0)
    #find lower eye node
    features = np.append(features,findClosest(points,features[0],axis=1,orientation=[0,-1]),axis=0)
        #find lower eye left points
    features = np.append(features,findClosest(points,features[3],axis=0,orientation=[-1]),axis=0)
    features = np.append(features,findClosest(points,features[4],axis=0,axis_scope=120,orientation=[-1]),axis=0)
    features = np.append(features,findClosest(points,features[5],axis=0,axis_scope=160,orientation=[-1]),axis=0)
        #find lower eye right points
    features = np.append(features,findClosest(points,features[3],axis=0,orientation=[1]),axis=0)
    features = np.append(features,findClosest(points,features[7],axis=0,axis_scope=120,orientation=[1]),axis=0)
    features = np.append(features,findClosest(points,features[8],axis=0,axis_scope=160,orientation=[1]),axis=0)
    #find eyebrow node
    features = np.append(features,findClosest(points,features[3],axis=1,orientation=[0,-1]),axis=0)
        #find eyebrow left points
    features = np.append(features,findClosest(points,features[10],axis=0,axis_scope=170,orientation=[-1]),axis=0)
    features = np.append(features,findClosest(points,features[11],axis=0,axis_scope=170,orientation=[-1]),axis=0)
    features = np.append(features,findClosest(points,features[12],axis=0,axis_scope=170,orientation=[-1]),axis=0)
        #find eyebrow right points
    features = np.append(features,findClosest(points,features[10],axis_scope=170,axis=0,orientation=[1]),axis=0)
    features = np.append(features,findClosest(points,features[14],axis_scope=170,axis=0,orientation=[1]),axis=0)
    features = np.append(features,findClosest(points,features[15],axis_scope=170,axis=0,orientation=[1]),axis=0)
    #find mouth upper node
    features = np.append(features,findClosest(points,features[0],axis=1,orientation=[0,1]),axis=0)
        #find mouth higher left (note: scope set to the abs angle of cheek_left)
    features = np.append(features,findClosest(points,features[17],axis=0,axis_scope=abs(atan(features[1,1]/features[1,0])*180/pi)*2,orientation=[-1]),axis=0)  
        #find mouth higher right (note: scope set to the abs angle of cheek_right)
    features = np.append(features,findClosest(points,features[17],axis=0,axis_scope=abs(atan(features[1,1]/features[1,0])*180/pi)*2,orientation=[1]),axis=0)
    #find mouth lower node
    features = np.append(features,findClosest(points,features[17],axis=1,axis_scope=40,orientation=[0,1]),axis=0)
        #find mouth lower left
    features = np.append(features,findClosest(points,features[20],axis=0,orientation=[-1]),axis=0)
    features = np.append(features,findClosest(points,features[21],axis=0,axis_scope=160,orientation=[-1]),axis=0)
        #find mouth lower right
    features = np.append(features,findClosest(points,features[20],axis=0,orientation=[1]),axis=0)
    features = np.append(features,findClosest(points,features[23],axis=0,axis_scope=160,orientation=[1]),axis=0)
    

    return features
        
        
    

'''
face center point data for testing purposes
'''

face = np.array([[ 982,  913],
       [ 893,  875],
       [1087,  864],
       [ 821,  813],
       [1131,  803],
       [ 806,  744],
       [1131,  727],
       [ 962,  725],
       [ 807,  617],
       [1111,  597],
       [ 959,  558],
       [ 738,  446],
       [1172,  439],
       [ 805,  429],
       [ 689,  430],
       [1223,  410],
       [1087,  410],
       [ 957,  388],
       [ 947,  270],
       [ 996,  199],
       [ 884,  198],
       [ 806,  164],
       [ 721,  150],
       [1175,  129],
       [1089,  132]])
                
