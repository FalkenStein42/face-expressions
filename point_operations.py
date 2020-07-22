'''
Point Operations Module

The purpose of this module is to provide tools for computing poitn cluster distances and relations.
These allow for the identification and prediction of the positions of reference points on the model.

TODO:
-implement trimmed median algorithm on findCentralPoint()
-generalize findClosest() to allow for specific axis and axis directions. Potentially separate this into a
    diferent version of the function
-implement an identification function for a set of points based on a fixed model
-provide proper documentation to functions

AUTHOR & LICENSE DETAILS:

[Author]   Sergio Solé
[Email]    sergio.sole99@gmail.com
[Discord]  Steve from Customer Service#6001

License details can be found on license file of this repo at https://github.com/FalkenStein42/face-expressions


'''

import numpy as np


def joinClosest(frame, points, connections = 2):
    pass
 
            
def findClosest(points, point):
    points = points-point #Shift origin to target
    points = np.delete(points, \
              np.where(np.all(np.equal(points,np.array([[0,0]])),axis=1)),\
              axis=0) #Delete itself from the list (now transformed to [0,0]) if it exists

    norm = np.linalg.norm(points,axis=1) #Make the vector norm array
    
    return (points[np.where(norm == np.amin(norm))] + point) #Return elements wich correspond with the index of the
                                                             # lowest norm, re-normalized to global coordinates
    
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
            





                
            
                
                
