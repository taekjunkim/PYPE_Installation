## This is a factory class for the generation of b8 stims and associated controls
## It generates sprite objects according to function parameters

import sys, types
from pype import *
#from Numeric import *
from math import *
class b8StimFactory_mm:
    def __init__(self,spriteSize,rfRadius):
        self.myVerts = self.getB8StimVerts()
        self.mySpriteSize = spriteSize
        self.myRFRadius = rfRadius
        self.myB8OccluderRots = self.getB8OccluderRots()
        self.myCachedSprites = list()
        self.myCachedSpriteInfo = list()
    #returns a b8 stimlus drawn in sp_color on a sprite with background bg_color
    #the sprite is centered at rfY, rfX, the b8 stimulus is centered at rfX+sp_h_offset and rfY+sp_v_offset
    #i = the sprite number
    #sampling is the number of points in each b8 segment
    #the sprite is rotated by sp_rotation degrees counterclockwise
    def getB8Stim(self,i, sampling,fb,sp_color,sp_rotation,rfX,rfY,bg_color, sp_h_offset=0, sp_v_offset=0, sp_scaling=1,depth=1):
        spriteSize = self.mySpriteSize
        vertX = self.myVerts[i][0]*self.myRFRadius/2 #these were initially made for a spritesize of 4 so multiply
        vertY = self.myVerts[i][1]*self.myRFRadius/2 #them by spritesize/4 ***comment about making this the standard size
        newVertX = list()
        newVertX.extend(vertX)
        newVertX.extend(vertX[0:3])
        newVertY = list()
        newVertY.extend(vertY)
        newVertY.extend(vertY[0:3])
        numVerts = len(vertX)
        ip = arange(0,sampling)/float(sampling) 
        incr = zeros((4,sampling), Float)
        incr[0,:] = -ip*ip*ip+3*ip*ip-3*ip+1
        incr[1,:] = 3*ip*ip*ip-6*ip*ip+4
        incr[2,:] = -3*ip*ip*ip+3*ip*ip+3*ip+1
        incr[3,:] = ip*ip*ip
        xVertID = zeros((4,sampling), Float)
        yVertID = zeros((4,sampling), Float)
        myCoords = list()
        for j in arange(0,numVerts):
            for k in arange(0, size(incr,0)):
                xVertID[k,:] = newVertX[j+k]
                yVertID[k,:] = newVertY[j+k]
            xb = sum(xVertID*incr)/6.0
            yb = sum(yVertID*incr)/6.0   
            coords = zeros((len(xb),2),Float)
            coords[0:len(xb),0] = xb*sp_scaling+sp_h_offset
            coords[0:len(yb),1] = yb*sp_scaling+sp_v_offset
            myCoords.extend(around(coords.tolist()))
        s = Sprite(spriteSize, spriteSize, rfX, rfY,fb=fb, depth=1, on=0,centerorigin=1)
        s.fill(bg_color)

        if(sp_rotation != 0):
            s.rotate(sp_rotation, 0, 1)
        s.polygon(sp_color,myCoords,0)
        return s
    #Similar to getB8Stim except that the stimulus is first rotated about its center so that its prominent feature is at 180 degrees.

    def getB8StimAsOccluder(self,i, sampling,fb,sp_color,sp_rotation,rfX,rfY,bg_color, sp_h_offset=0, sp_v_offset=0,sp_scaling=1,depth=1):
        spriteSize = self.mySpriteSize
        if(i != 43):		
        	vertX = self.myVerts[i][0]*self.myRFRadius/2.0/.75 #these were initially made for a spritesize of 4 so multiply
        	vertY = self.myVerts[i][1]*self.myRFRadius/2.0/.75 #them by spritesize/4
        	newVertX = list()
        	newVertX.extend(vertX)
        	newVertX.extend(vertX[0:3])
        	newVertY = list()
        	newVertY.extend(vertY)
        	newVertY.extend(vertY[0:3])
        	numVerts = len(vertX)
        	ip = arange(0,sampling)/float(sampling) ### sampling
        	incr = zeros((4,sampling), Float)
        	incr[0,:] = -ip*ip*ip+3*ip*ip-3*ip+1
        	incr[1,:] = 3*ip*ip*ip-6*ip*ip+4
        	incr[2,:] = -3*ip*ip*ip+3*ip*ip+3*ip+1
        	incr[3,:] = ip*ip*ip
        	xVertID = zeros((4,sampling), Float)
        	yVertID = zeros((4,sampling), Float)
        	myCoords = list()
        	for j in arange(0,numVerts):
            		for k in arange(0, size(incr,0)):
                		xVertID[k,:] = newVertX[j+k]
                		yVertID[k,:] = newVertY[j+k]
            		xb = sum(xVertID*incr)/6.0
            		yb = sum(yVertID*incr)/6.0   
            		coords = zeros((len(xb),2),Float)
            		coords[0:len(xb),0] = xb 
            		coords[0:len(yb),1] = yb
            		myCoords.extend(around(coords.tolist()))
        #rotate b8stim so that its prominent feature is at 180 degrees
        #[theta,rad] = cart2pol(newShapeX, newShapeY);%find the polar coordinates
        #    [newX,newY] = pol2cart(theta+(j-1)*pi/4, rad);%rotate
        	arCoords = array(myCoords)
        #print arCoords[:,1]
        	theta = zeros((size(arCoords,0),1),Float)
        	rads = zeros((size(arCoords,0),1),Float)
        	newCoords = zeros((size(arCoords,0),2),Int)
        	myRot = self.myB8OccluderRots[i]
        	for j in arange(0,size(arCoords,0)):
            		theta[j] = atan2(arCoords[j,1],arCoords[j,0])
            		rads[j] = sqrt(arCoords[j,1]**2 + arCoords[j,0]**2)
            		newTVal = theta[j]+radians(myRot)
            		newCoords[j,0] = round(rads[j]*cos(newTVal)*sp_scaling+sp_h_offset)
            		newCoords[j,1] = round(rads[j]*sin(newTVal)*sp_scaling+sp_v_offset)
        	s = Sprite(spriteSize, spriteSize, rfX, rfY,fb=fb, depth=depth, on=0,centerorigin=1)
        	s.fill(bg_color)
        	s.rotate(sp_rotation, 0, 1)
        	s.polygon(sp_color,newCoords,0)
        else:
        	s = Sprite(spriteSize, spriteSize, rfX, rfY, fb=fb, depth=depth, on=0, centerorigin=1)
        	s.fill(bg_color)
        	s.rotate(sp_rotation, 0, 1)
        	s.rect(0,0,self.myRFRadius/.75, self.myRFRadius/.75, sp_color)
        return s
    #return the control points for object i as a list of x,y pairs in alist

    def getControlPoints(self,i):
        ctPoints = self.myVerts[i]
        coords = zeros((len(ctPoints[0]),2),Float)
        coords[0:len(ctPoints[0]),0] = ctPoints[0] 
        coords[0:len(ctPoints[1]),1] = ctPoints[1]
        return coords.tolist()

    def getB8OccluderRots(self):
        b8OccluderRots = zeros((len(self.myVerts)+1,1), Float)
        b8OccluderRots[1] = 0
        b8OccluderRots[2] = 0
        b8OccluderRots[3] = 0
        b8OccluderRots[4] = 0
        b8OccluderRots[5] = 0
        b8OccluderRots[6] = 0
        b8OccluderRots[7] = 0
        b8OccluderRots[8] = 0
        b8OccluderRots[9] = 0
        b8OccluderRots[10] = 0
        b8OccluderRots[11] = 0
        b8OccluderRots[12] = 0
        b8OccluderRots[13] = 0
        b8OccluderRots[14] = 0
        b8OccluderRots[15] = 0
        b8OccluderRots[16] = 0
        b8OccluderRots[17] = 0
        b8OccluderRots[18] = 0
        b8OccluderRots[19] = 0
        b8OccluderRots[20] = 0
        b8OccluderRots[21] = 0
        b8OccluderRots[22] = 0
        b8OccluderRots[23] = 0
        b8OccluderRots[24] = 0
        b8OccluderRots[25] = 0
        b8OccluderRots[26] = 0
        b8OccluderRots[27] = 0
        b8OccluderRots[28] = 0
        b8OccluderRots[29] = 0
        b8OccluderRots[30] = 0
        b8OccluderRots[31] = 0
        b8OccluderRots[32] = 0
        b8OccluderRots[33] = 0
        b8OccluderRots[34] = 0
        b8OccluderRots[35] = 0
        b8OccluderRots[36] = 0
        b8OccluderRots[37] = 0
        b8OccluderRots[38] = 0
        b8OccluderRots[39] = 0
        b8OccluderRots[40] = 0
        b8OccluderRots[41] = 0
        b8OccluderRots[42] = 0
        return b8OccluderRots
    #internal method sets verts

    def getB8StimVerts(self):
        myVerts = list()
        temp = list()
        temp.append(None)
        temp.append(None)
        myVerts.append(list(temp))
        #Stim #1
        temp[0] = asarray([-1.6,-0.988,-0.468,-0.122,0.0,0.122,0.468,0.988,1.6,0.988,0.468,0.122,0.0,-0.122,-0.468,-0.988])
        temp[1] = asarray([0.0,0.122,0.468,0.988,1.6,0.988,0.468,0.122,0.0,-0.122,-0.468,-0.988,-1.6,-0.988,-0.468,-0.122])
        myVerts.append(list(temp))
        #Stim #2
        temp[0] = asarray([-1.6,-0.988,-0.468,-0.122,0.0,0.122,0.468,0.988,1.6,1.14,0.751,0.5,0.4,0.283,0.0,-0.283,-0.4,-0.5,-0.751,-1.14])
        temp[1] = asarray([0.0,0.122,0.468,0.988,1.6,0.988,0.468,0.122,0.0,-0.1,-0.351,-0.74,-1.2,-1.483,-1.6,-1.483,-1.2,-0.74,-0.351,-0.1])
        myVerts.append(list(temp))
        #Stim #3
        temp[0] = asarray([-1.6,-1.483,-1.2,-0.74,-0.351,-0.1,0.0,0.1,0.351,0.74,1.2,1.483,1.6,1.483,1.2,0.74,0.351,0.1,0.0,-0.1,-0.351,-0.74,-1.2,-1.483])
        temp[1] = asarray([0.0,0.283,0.4,0.5,0.751,1.14,1.6,1.14,0.751,0.5,0.4,0.283,0.0,-0.283,-0.4,-0.5,-0.751,-1.14,-1.6,-1.14,-0.751,-0.5,-0.4,-0.283])
        myVerts.append(list(temp))
        #Stim #4
        temp[0] = asarray([-1.6,-0.988,-0.468,-0.122,0.0,0.1,0.351,0.74,1.2,1.483,1.6,1.483,1.2,0.894,0.635,0.461,0.4,0.283,0.0,-0.283,-0.4,-0.5,-0.751,-1.14])
        temp[1] = asarray([0.0,0.122,0.468,0.988,1.6,1.14,0.751,0.5,0.4,0.283,0.0,-0.283,-0.4,-0.461,-0.635,-0.894,-1.2,-1.483,-1.6,-1.483,-1.2,-0.74,-0.351,-0.1])
        myVerts.append(list(temp))
        #Stim #5
        temp[0] = asarray([-1.6,-1.483,-1.2,-0.894,-0.635,-0.461,-0.4,-0.283,0.0,0.283,0.4,0.461,0.635,0.894,1.2,1.483,1.6,1.483,1.2,0.74,0.351,0.1,0.0,-0.1,-0.351,-0.74,-1.2,-1.483])
        temp[1] = asarray([0.0,0.283,0.4,0.461,0.635,0.894,1.2,1.483,1.6,1.483,1.2,0.894,0.635,0.461,0.4,0.283,0.0,-0.283,-0.4,-0.5,-0.751,-1.14,-1.6,-1.14,-0.751,-0.5,-0.4,-0.283])
        myVerts.append(list(temp))
        #Stim #6
        temp[0] = asarray([-1.6,-0.988,-0.468,-0.122,0.0,0.1,0.351,0.74,1.2,1.483,1.6,1.131,0.0,-0.283,-0.4,-0.5,-0.751,-1.14])
        temp[1] = asarray([0.0,-0.122,-0.468,-0.988,-1.6,-1.14,-0.751,-0.5,-0.4,-0.283,0.0,1.131,1.6,1.483,1.2,0.74,0.351,0.1])
        myVerts.append(list(temp))
        #Stim #7
        temp[0] = asarray([-1.6,-0.988,-0.468,-0.122,0.0,1.131,1.6,1.483,1.2,0.894,0.635,0.461,0.4,0.283,0.0,-0.283,-0.4,-0.5,-0.751,-1.14])
        temp[1] = asarray([0.0,0.122,0.468,0.988,1.6,1.131,0.0,-0.283,-0.4,-0.461,-0.635,-0.894,-1.2,-1.483,-1.6,-1.483,-1.2,-0.74,-0.351,-0.1])
        myVerts.append(list(temp))
        #Stim #8
        temp[0] = asarray([-0.294,-0.075,0.0,0.075,0.294,0.651,1.131,0.612,0.0,-0.612,-1.131,-0.651])
        temp[1] = asarray([0.122,0.846,1.6,0.846,0.122,-0.546,-1.131,-0.785,-0.663,-0.785,-1.131,-0.546])
        myVerts.append(list(temp))
        #Stim #9
        temp[0] = asarray([-0.467,-0.35,-0.393,-0.283,0.0,0.283,0.393,0.35,0.467,0.751,1.131,0.612,0.0,-0.612,-1.131,-0.751])
        temp[1] = asarray([0.102,0.505,1.122,1.483,1.6,1.483,1.122,0.505,-0.102,-0.688,-1.131,-0.785,-0.663,-0.785,-1.131,-0.688])
        myVerts.append(list(temp))
        #Stim #10
        temp[0] = asarray([-0.294,-0.075,0.0,0.054,0.257,0.605,1.071,1.248,1.131,0.85,0.57,0.179,-0.282,-0.742,-1.131,-0.651])
        temp[1] = asarray([0.122,0.846,1.6,0.983,0.401,-0.111,-0.516,-0.848,-1.131,-1.25,-1.131,-0.871,-0.78,-0.871,-1.131,-0.546])
        myVerts.append(list(temp))
        #Stim #11
        temp[0] = asarray([-0.257,-0.054,0.0,0.075,0.294,0.651,1.131,0.742,0.282,-0.179,-0.571,-0.85,-1.131,-1.248,-1.071,-0.605])
        temp[1] = asarray([0.401,0.983,1.6,0.846,0.122,-0.546,-1.131,-0.871,-0.78,-0.871,-1.131,-1.25,-1.131,-0.848,-0.516,-0.111])
        myVerts.append(list(temp))
        #Stim #12
        temp[0] = asarray([-0.257,-0.054,0.0,0.054,0.257,0.605,1.071,1.248,1.131,0.85,0.57,0.308,0.0,-0.308,-0.57,-0.85,-1.131,-1.248,-1.071,-0.605])
        temp[1] = asarray([0.401,0.983,1.6,0.983,0.401,-0.111,-0.516,-0.848,-1.131,-1.25,-1.131,-0.957,-0.896,-0.957,-1.131,-1.25,-1.131,-0.848,-0.516,-0.111])
        myVerts.append(list(temp))
        #Stim #13
        temp[0] = asarray([-0.487,-0.373,-0.393,-0.283,0.0,0.283,0.393,0.35,0.467,0.751,1.131,0.742,0.282,-0.179,-0.571,-0.85,-1.131,-1.248,-1.071,-0.727])
        temp[1] = asarray([0.198,0.652,1.122,1.483,1.6,1.483,1.122,0.505,-0.102,-0.688,-1.131,-0.871,-0.78,-0.871,-1.131,-1.25,-1.131,-0.848,-0.516,-0.203])
        myVerts.append(list(temp))
        #Stim #14
        temp[0] = asarray([-0.467,-0.35,-0.393,-0.283,0.0,0.283,0.393,0.373,0.487,0.727,1.071,1.248,1.131,0.85,0.57,0.179,-0.282,-0.742,-1.131,-0.751])
        temp[1] = asarray([0.102,0.505,1.122,1.483,1.6,1.483,1.122,0.652,0.198,-0.203,-0.516,-0.848,-1.131,-1.25,-1.131,-0.871,-0.78,-0.871,-1.131,-0.688])
        myVerts.append(list(temp))
        #Stim #15
        temp[0] = asarray([-0.487,-0.373,-0.393,-0.283,0.0,0.283,0.393,0.373,0.487,0.727,1.071,1.248,1.131,0.85,0.57,0.308,0.0,-0.308,-0.57,-0.85,-1.131,-1.248,-1.071,-0.727])
        temp[1] = asarray([0.198,0.652,1.122,1.483,1.6,1.483,1.122,0.652,0.198,-0.203,-0.516,-0.848,-1.131,-1.25,-1.131,-0.957,-0.896,-0.957,-1.131,-1.25,-1.131,-0.848,-0.516,-0.203])
        myVerts.append(list(temp))
        #Stim #16
        temp[0] = asarray([-0.257,-0.054,0.0,0.054,0.257,0.605,1.071,1.248,1.131,0.85,0.0,-0.85,-1.131,-1.248,-1.071,-0.605])
        temp[1] = asarray([0.401,0.983,1.6,0.983,0.401,-0.111,-0.516,-0.848,-1.131,-1.25,-1.6,-1.25,-1.131,-0.848,-0.516,-0.111])
        myVerts.append(list(temp))
        #Stim #17
        temp[0] = asarray([-0.467,-0.35,-0.393,-0.283,0.0,0.283,1.031,1.248,1.131,0.85,0.57,0.179,-0.282,-0.742,-1.131,-0.751])
        temp[1] = asarray([0.102,0.505,1.122,1.483,1.6,1.483,0.298,-0.848,-1.131,-1.25,-1.131,-0.871,-0.78,-0.871,-1.131,-0.688])
        myVerts.append(list(temp))
        #Stim #18
        temp[0] = asarray([0.467,0.35,0.393,0.283,0.0,-0.283,-1.031,-1.248,-1.131,-0.85,-0.57,-0.179,0.282,0.742,1.131,0.751])
        temp[1] = asarray([0.102,0.505,1.122,1.483,1.6,1.483,0.298,-0.848,-1.131,-1.25,-1.131,-0.871,-0.78,-0.871,-1.131,-0.688])
        myVerts.append(list(temp))
        #Stim #19
        temp[0] = asarray([-0.487,-0.373,-0.393,-0.283,0.0,0.283,1.031,1.248,1.131,0.85,0.57,0.308,0.0,-0.308,-0.57,-0.85,-1.131,-1.248,-1.071,-0.727])
        temp[1] = asarray([0.198,0.652,1.122,1.483,1.6,1.483,0.298,-0.848,-1.131,-1.25,-1.131,-0.957,-0.896,-0.957,-1.131,-1.25,-1.131,-0.848,-0.516,-0.203])
        myVerts.append(list(temp))
        #Stim #20
        temp[0] = asarray([0.487,0.373,0.393,0.283,0.0,-0.283,-1.031,-1.248,-1.131,-0.85,-0.57,-0.308,0.0,0.308,0.57,0.85,1.131,1.248,1.071,0.727])
        temp[1] = asarray([0.198,0.652,1.122,1.483,1.6,1.483,0.298,-0.848,-1.131,-1.25,-1.131,-0.957,-0.896,-0.957,-1.131,-1.25,-1.131,-0.848,-0.516,-0.203])
        myVerts.append(list(temp))
        #Stim #21
        temp[0] = asarray([-0.487,-0.373,-0.393,-0.283,0.0,0.283,0.393,0.373,0.487,0.727,1.071,1.248,1.131,0.85,0.0,-0.85,-1.131,-1.248,-1.071,-0.727])
        temp[1] = asarray([0.198,0.652,1.122,1.483,1.6,1.483,1.122,0.652,0.198,-0.203,-0.516,-0.848,-1.131,-1.25,-1.6,-1.25,-1.131,-0.848,-0.516,-0.203])
        myVerts.append(list(temp))
        #Stim #22
        temp[0] = asarray([-0.571,-0.369,0.0,0.283,0.4,0.492,0.752,1.14,1.6,0.988,0.468,0.122,0.0,-0.212,-0.381,-0.575])
        temp[1] = asarray([0.605,1.354,1.6,1.483,1.2,0.74,0.352,0.092,0.0,-0.122,-0.468,-0.988,-1.6,-1.273,-0.923,-0.172])
        myVerts.append(list(temp))
        #Stim #23
        temp[0] = asarray([-0.533,-0.397,-0.176,0.0,0.122,0.468,0.988,1.6,0.988,0.468,0.122,0.0,-0.176,-0.397])
        temp[1] = asarray([0.0,0.843,1.333,1.6,0.988,0.468,0.122,0.0,-0.122,-0.468,-0.988,-1.6,-1.333,-0.843])
        myVerts.append(list(temp))
        #Stim #24
        temp[0] = asarray([-0.533,-0.397,-0.176,0.0,0.1,0.351,0.74,1.2,1.483,1.6,1.483,1.2,0.74,0.351,0.1,0.0,-0.176,-0.397])
        temp[1] = asarray([0.0,0.843,1.333,1.6,1.14,0.751,0.5,0.4,0.283,0.0,-0.283,-0.4,-0.5,-0.751,-1.14,-1.6,-1.333,-0.843])
        myVerts.append(list(temp))
        #Stim #25
        temp[0] = asarray([-0.575,-0.381,-0.212,0.0,0.122,0.468,0.988,1.6,1.14,0.752,0.492,0.4,0.283,0.0,-0.369,-0.571])
        temp[1] = asarray([0.172,0.923,1.273,1.6,0.988,0.468,0.122,0.0,-0.092,-0.352,-0.74,-1.2,-1.483,-1.6,-1.354,-0.605])
        myVerts.append(list(temp))
        #Stim #26
        temp[0] = asarray([-0.571,-0.369,0.0,0.283,0.4,0.461,0.635,0.894,1.2,1.483,1.6,1.483,1.2,0.74,0.351,0.1,0.0,-0.212,-0.381,-0.575])
        temp[1] = asarray([0.605,1.354,1.6,1.483,1.2,0.894,0.635,0.461,0.4,0.283,0.0,-0.283,-0.4,-0.5,-0.751,-1.14,-1.6,-1.273,-0.923,-0.172])
        myVerts.append(list(temp))
        #Stim #27
        temp[0] = asarray([-0.64,-0.571,-0.369,0.0,0.283,0.4,0.492,0.752,1.14,1.6,1.14,0.752,0.492,0.4,0.283,0.0,-0.369,-0.571])
        temp[1] = asarray([0.0,0.689,1.354,1.6,1.483,1.2,0.74,0.352,0.092,0.0,-0.092,-0.352,-0.74,-1.2,-1.483,-1.6,-1.354,-0.689])
        myVerts.append(list(temp))
        #Stim #28
        temp[0] = asarray([-0.64,-0.571,-0.369,0.0,0.283,0.4,0.461,0.635,0.894,1.2,1.483,1.6,1.483,1.2,0.894,0.635,0.461,0.4,0.283,0.0,-0.369,-0.571])
        temp[1] = asarray([0.0,0.689,1.354,1.6,1.483,1.2,0.894,0.635,0.461,0.4,0.283,0.0,-0.283,-0.4,-0.461,-0.635,-0.894,-1.2,-1.483,-1.6,-1.354,-0.689])
        myVerts.append(list(temp))
        #Stim #29
        temp[0] = asarray([-1.6,-1.131,0.0,1.131,1.6,1.2,0.74,0.351,0.1,0.0,-0.1,-0.351,-0.74,-1.2])
        temp[1] = asarray([0.0,1.131,1.6,1.131,0.0,-0.4,-0.5,-0.751,-1.14,-1.6,-1.14,-0.751,-0.5,-0.4])
        myVerts.append(list(temp))
        #Stim #30
        temp[0] = asarray([-0.571,0.0,1.131,1.6,1.2,0.74,0.351,0.1,0.0,-0.212,-0.381,-0.575])
        temp[1] = asarray([0.605,1.6,1.131,0.0,-0.4,-0.5,-0.751,-1.14,-1.6,-1.273,-0.923,-0.172])
        myVerts.append(list(temp))
        #Stim #31
        temp[0] = asarray([0.575,0.381,0.212,0.0,-0.1,-0.351,-0.74,-1.2,-1.6,-1.131,0.0,0.571])
        temp[1] = asarray([-0.172,-0.923,-1.273,-1.6,-1.14,-0.751,-0.5,-0.4,0.0,1.131,1.6,0.605])
        myVerts.append(list(temp))
        #Stim #32
        temp[0] = asarray([-0.64,-0.571,0.0,1.131,1.6,1.2,0.894,0.635,0.461,0.4,0.283,0.0,-0.369,-0.571])
        temp[1] = asarray([0.0,0.689,1.6,1.131,0.0,-0.4,-0.461,-0.635,-0.894,-1.2,-1.483,-1.6,-1.354,-0.689])
        myVerts.append(list(temp))
        #Stim #33
        temp[0] = asarray([0.64,0.571,0.369,0.0,-0.283,-0.4,-0.461,-0.635,-0.894,-1.2,-1.6,-1.131,0.0,0.571])
        temp[1] = asarray([0.0,-0.689,-1.354,-1.6,-1.483,-1.2,-0.894,-0.635,-0.461,-0.4,0.0,1.131,1.6,0.689])
        myVerts.append(list(temp))
        #Stim #34
        temp[0] = asarray([-1.6,-1.2,-0.894,-0.635,-0.461,-0.4,0.0,1.131,1.6,1.131,0.0,-1.131])
        temp[1] = asarray([0.0,-0.4,-0.461,-0.635,-0.894,-1.2,-1.6,-1.131,0.0,1.131,1.6,1.131])
        myVerts.append(list(temp))
        #Stim #35
        temp[0] = asarray([-1.6,-1.2,-0.894,-0.635,-0.461,-0.4,-0.283,0.0,0.283,0.4,0.461,0.635,0.894,1.2,1.6,1.131,0.0,-1.131])
        temp[1] = asarray([0.0,-0.4,-0.461,-0.635,-0.894,-1.2,-1.483,-1.6,-1.483,-1.2,-0.894,-0.635,-0.461,-0.4,0.0,1.131,1.6,1.131])
        myVerts.append(list(temp))
        #Stim #36
        temp[0] = asarray([-0.373,-0.266,-0.069,0.0,0.069,0.266,0.373,0.266,0.069,0.0,-0.069,-0.266])
        temp[1] = asarray([0.0,0.828,1.37,1.6,1.37,0.828,0.0,-0.828,-1.37,-1.6,-1.37,-0.828])
        myVerts.append(list(temp))
        #Stim #37
        temp[0] = asarray([-0.438,-0.277,-0.182,-0.102,0.0,0.102,0.182,0.277,0.438,0.477,0.393,0.0,-0.393,-0.477])
        temp[1] = asarray([0.195,0.916,1.19,1.387,1.6,1.387,1.19,0.916,0.195,-0.543,-1.278,-1.6,-1.278,-0.543])
        myVerts.append(list(temp))
        #Stim #38
        temp[0] = asarray([-0.64,-0.571,-0.369,0.0,0.369,0.571,0.64,0.571,0.369,0.0,-0.369,-0.571])
        temp[1] = asarray([0.0,0.689,1.354,1.6,1.354,0.689,0.0,-0.689,-1.354,-1.6,-1.354,-0.689])
        myVerts.append(list(temp))
        #Stim #39
        temp[0] = asarray([-0.082,-0.289,0.0,0.1,0.351,0.74,1.2,1.483,1.6,1.278,0.467])
        temp[1] = asarray([0.186,0.884,1.6,1.14,0.751,0.5,0.4,0.283,0.0,-0.393,-0.294])
        myVerts.append(list(temp))
        #Stim #40
        temp[0] = asarray([-1.6,-1.483,-1.2,-0.74,-0.351,-0.1,0.0,0.289,0.082,-0.467,-1.278])
        temp[1] = asarray([0.0,0.283,0.4,0.5,0.751,1.14,1.6,0.884,0.186,-0.294,-0.393])
        myVerts.append(list(temp))
        #Stim #41
        temp[0] = asarray([-0.123,-0.167,0.0,0.054,0.257,0.605,1.071,1.216,1.131,0.85,0.57,0.13])
        temp[1] = asarray([0.149,0.883,1.6,0.983,0.401,-0.111,-0.516,-0.848,-1.131,-1.25,-1.131,-0.542])
        myVerts.append(list(temp))
        #Stim #42
        temp[0] = asarray([-0.605,-0.257,-0.054,0.0,0.167,0.123,-0.13,-0.57,-0.85,-1.131,-1.216,-1.071])
        temp[1] = asarray([-0.111,0.401,0.983,1.6,0.883,0.149,-0.542,-1.131,-1.25,-1.131,-0.848,-0.516])
        myVerts.append(list(temp))
        return myVerts

