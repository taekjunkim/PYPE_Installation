## This is a factory class for the generation of b8 stims and associated controls

## It generates sprite objects according to function parameters





import sys, types

from pype import *

import numpy as np; 
from math import *

class b8StimFactory:



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
        vertX = self.myVerts[i][0]*self.myRFRadius/2/.75 #these were initially made for a spritesize of 4 so multiply
        vertY = self.myVerts[i][1]*self.myRFRadius/2/.75 #them by spritesize/4
        newVertX = list()
        newVertX.extend(vertX)
        newVertX.extend(vertX[0:3])
        newVertY = list()
        newVertY.extend(vertY)
        newVertY.extend(vertY[0:3])

        numVerts = len(vertX)
        ip = np.arange(0,sampling)/float(sampling) 
        incr = np.zeros((4,sampling), float)
        incr[0,:] = -ip*ip*ip+3*ip*ip-3*ip+1
        incr[1,:] = 3*ip*ip*ip-6*ip*ip+4
        incr[2,:] = -3*ip*ip*ip+3*ip*ip+3*ip+1
        incr[3,:] = ip*ip*ip

        xVertID = np.zeros((4,sampling), float)
        yVertID = np.zeros((4,sampling), float)
        myCoords = list()
        for j in np.arange(0,numVerts):
            for k in np.arange(0, size(incr,0)):
                xVertID[k,:] = newVertX[j+k]
                yVertID[k,:] = newVertY[j+k]
            xb = sum(xVertID*incr, axis=0)/6.0
            yb = sum(yVertID*incr, axis=0)/6.0   
            coords = np.zeros((len(xb),2),float)
            coords[0:len(xb),0] = xb*sp_scaling+sp_h_offset
            coords[0:len(yb),1] = yb*sp_scaling+sp_v_offset

            if(sp_rotation != 0):
    #                pdb.set_trace()
                rotx = coords[0,0]*np.cos(sp_rotation*np.pi/180)-coords[0,1]*np.sin(sp_rotation*np.pi/180)
                roty = coords[0,0]*np.sin(sp_rotation*np.pi/180)+coords[0,1]*np.cos(sp_rotation*np.pi/180)
                coords[0,0]=rotx
                coords[0,1]=roty
            myCoords.append(coords[0])

            for xy in range(1,len(xb)):
                if(sp_rotation != 0):		# COMMENT 8/3/11 do rotation on floating point contour
                    rotx = coords[xy,0]*np.cos(sp_rotation*np.pi/180)-coords[xy,1]*np.sin(sp_rotation*np.pi/180)
                    roty = coords[xy,0]*np.sin(sp_rotation*np.pi/180)+coords[xy,1]*np.cos(sp_rotation*np.pi/180)
                    coords[xy,0]=rotx
                    coords[xy,1]=roty
    #                    pdb.set_trace()
                if ((coords[xy,0] != coords[xy-1,0]) or (coords[xy,1] != coords[xy-1,1])):
                    myCoords.append(coords[xy])
	#DVP 2/15/13
	#to use a background image, switch the s= line to the one with fname=''
	#comment out s.fill
	#switch from aapolygon to regular polygon

        #needed depth=depth to present stimulus behind fixation spot DVP 8/2/13

        s = Sprite(spriteSize, spriteSize, rfX, rfY,fb=fb, depth=depth, on=0,centerorigin=1)

        # ORIGINAL LINE
        #s = Sprite(spriteSize, spriteSize, rfX, rfY,fb=fb, depth=1, on=0,centerorigin=1)

	#s = Sprite(spriteSize, spriteSize, rfX, rfY,fb=fb, depth=1, on=0,centerorigin=1, fname = 'NoiseSurround-bmp.jpg')

        s.fill(bg_color)
        #s.aapolygon(sp_color,myCoords,0) #9/3/12 changed this to implement AA polygon -- AP
        s.polygon(sp_color,myCoords,0) #9/3/12 changed this to implement AA polygon -- AP

        return s



    #Similar to getB8Stim except that the stimulus is first rotated about its center so that its prominent feature is at 180 degrees.

    def getB8StimAsOccluder(self,i, sampling,fb,sp_color,sp_rotation,rfX,rfY,bg_color, sp_h_offset=0, sp_v_offset=0,sp_scaling=1,depth=1):

        spriteSize = self.mySpriteSize

        vertX = self.myVerts[i][0]*self.myRFRadius/2.0/.75 #these were initially made for a spritesize of 4 so multiply

        vertY = self.myVerts[i][1]*self.myRFRadius/2.0/.75 #them by spritesize/4



        newVertX = list()

        newVertX.extend(vertX)

        newVertX.extend(vertX[0:3])

        newVertY = list()

        newVertY.extend(vertY)

        newVertY.extend(vertY[0:3])



        numVerts = len(vertX)

        ip = np.arange(0,sampling)/float(sampling) ### sampling

        incr = np.zeros((4,sampling), float)

        incr[0,:] = -ip*ip*ip+3*ip*ip-3*ip+1

        incr[1,:] = 3*ip*ip*ip-6*ip*ip+4

        incr[2,:] = -3*ip*ip*ip+3*ip*ip+3*ip+1

        incr[3,:] = ip*ip*ip

        xVertID = np.zeros((4,sampling), float)

        yVertID = np.zeros((4,sampling), float)

        myCoords = list()
        myCoords1 = list()

        for j in np.arange(0,numVerts):

            for k in np.arange(0, size(incr,0)):

                xVertID[k,:] = newVertX[j+k]

                yVertID[k,:] = newVertY[j+k]

            xb = sum(xVertID*incr, axis=0)/6.0

            yb = sum(yVertID*incr, axis=0)/6.0   

            coords = np.zeros((len(xb),2),float)

            coords[0:len(xb),0] = xb 

            coords[0:len(yb),1] = yb

            myCoords.extend(around(coords.tolist()))

            



        #rotate b8stim so that its prominent feature is at 180 degrees

        arCoords = array(myCoords)

        #print arCoords[:,1]

        theta = np.zeros((size(arCoords,0),1),float)

        rads = np.zeros((size(arCoords,0),1),float)

        newCoords = np.zeros((size(arCoords,0),2),int)

        myRot = self.myB8OccluderRots[i]
        

        for j in np.arange(0,size(arCoords,0)):

            theta[j] = atan2(arCoords[j,1],arCoords[j,0])

            rads[j] = sqrt(arCoords[j,1]**2 + arCoords[j,0]**2)

            newTVal = theta[j]+radians(myRot)

            newCoords[j,0] = round(rads[j]*cos(newTVal)*sp_scaling+sp_h_offset)

            newCoords[j,1] = round(rads[j]*sin(newTVal)*sp_scaling+sp_v_offset)
        

        #Added static vertical offsets for some accidental convex occluders because they were not overlapping the percept correctly.

        #This is only for stims 52-65 for new added convex occluders, everything else is just a rotation of previous occluders presented for complexstim

            if(i >= 52 and i <=59):

                newCoords[j,1] = newCoords[j,1] - 0.2*self.myRFRadius

            elif(i >= 60 and i <= 65 and i != 62):

                newCoords[j,1] = newCoords[j,1] - 0.2*self.myRFRadius

            elif(i == 62):

                newCoords[j,1] = newCoords[j,1] - 0.1*self.myRFRadius

        if(sp_rotation != 0):
            rotx = newCoords[0,0]*cos(sp_rotation*np.pi/180)-newCoords[0,1]*sin(sp_rotation*np.pi/180)
            roty = newCoords[0,0]*sin(sp_rotation*np.pi/180)+newCoords[0,1]*cos(sp_rotation*np.pi/180)
            newCoords[0,0]=rotx
            newCoords[0,1]=roty
        myCoords1.append(newCoords[0])

        for xy in range(1,size(newCoords,0)):
            if(sp_rotation != 0):		# COMMENT 8/3/11 do rotation on floating point contour
                 rotx = newCoords[xy,0]*cos(sp_rotation*np.pi/180)-newCoords[xy,1]*sin(sp_rotation*np.pi/180)
                 roty = newCoords[xy,0]*sin(sp_rotation*np.pi/180)+newCoords[xy,1]*cos(sp_rotation*np.pi/180)
                 newCoords[xy,0]=rotx
                 newCoords[xy,1]=roty
            if ((newCoords[xy,0] != newCoords[xy-1,0]) or (newCoords[xy,1] != newCoords[xy-1,1])):
            	 myCoords1.append(newCoords[xy])
            
        s = Sprite(spriteSize, spriteSize, rfX, rfY,fb=fb, depth=depth, on=0,centerorigin=1)
        s.fill(bg_color)
        #s.aapolygon(sp_color,myCoords1,0) #9/3/2012 changed this to implement aa polygon-AP
        s.polygon(sp_color,myCoords1,0) 
        return s


##    #returns a new sprite that is a circle of a specified color occluded by a b8 stim of the chosen color

##    def getB8StimComplex(i, sampling,fb,fg_color,sp_rotation,rfX,rfY,mg_color, fg_h_offset=0, fg_v_offset=0,fg_scaling=1, mg_h_offset=0, mg_v_offset=0,mg_scaling=1):

##        #get cached b8 if exists        

##        s= getCachedB8(i, sampling,fb,fg_color,sp_rotation, fg_h_offset, fg_v_offset,fg_scaling)

##        s = s.clone()

##        s.moveto(rfX,rfY)

##        if(s is None):

##            s= getB8StimAsOccluder(i, sampling,fb,fg_color,sp_rotation,rfX,rfY, fg_h_offset, fg_v_offset,fg_scaling)

##

##        

##

##    def getCachedB8(i, sampling,fb,sp_color,sp_rotation,bg_color, sp_h_offset, sp_v_offset,sp_scaling)

##        foundSprite = 0

##        index = 0

##        while(not foundSprite and index < len(self.myCachedSpriteInfo)):

##            info = self.myCachedSpriteInfo[index]

##            if(info[0] == i and info[1]==sampling and info[2]==fb and info[3] == sp_color and info[4] == sp_rotation and info[7] == bg_color and info[8] ==  sp_h_offset and info[9] ==  sp_v_offset and info[10] == sp_scaling):

##                print "found cached sprite %d" % (i)

##                foundSprite = 1

##                return self.myCachedSprites[index]

##

##        return None



    #return the control points for object i as a list of x,y pairs in alist

    def getControlPoints(self,i):

        ctPoints = self.myVerts[i]

        coords = np.zeros((len(ctPoints[0]),2),float)

        coords[0:len(ctPoints[0]),0] = ctPoints[0] 

        coords[0:len(ctPoints[1]),1] = ctPoints[1]

        return coords.tolist()

         





    def getB8OccluderRots(self):

        b8OccluderRots = np.zeros((len(self.myVerts)+1,1), float)

        b8OccluderRots[1] = 180

        b8OccluderRots[2] = 180

        b8OccluderRots[3] = 90

        b8OccluderRots[4] = 90

        b8OccluderRots[5] = 90

        b8OccluderRots[6] = 90

        b8OccluderRots[7] = 90

        b8OccluderRots[8] = 45

        b8OccluderRots[9] = 45

        b8OccluderRots[10] = 45

        b8OccluderRots[11] = 315

        b8OccluderRots[12] = 90

        b8OccluderRots[13] = 90

        b8OccluderRots[14] = 225

        b8OccluderRots[15] = 315

        b8OccluderRots[16] = 180

        b8OccluderRots[17] = 180

        b8OccluderRots[18] = 180

        b8OccluderRots[19] = 180

        b8OccluderRots[20] = 180

        b8OccluderRots[21] = 180

        b8OccluderRots[22] = 180

        b8OccluderRots[23] = 180

        b8OccluderRots[24] = 90

        b8OccluderRots[25] = 90

        b8OccluderRots[26] = 225

        b8OccluderRots[27] = 315

        b8OccluderRots[28] = 90

        b8OccluderRots[29] = 90

        b8OccluderRots[30] = 90

        b8OccluderRots[31] = 90

        b8OccluderRots[32] = 0

        b8OccluderRots[33] = 270

        b8OccluderRots[34] = 180

        b8OccluderRots[35] = 180

        b8OccluderRots[36] = 270

        b8OccluderRots[37] = 90

        b8OccluderRots[38] = 270

        b8OccluderRots[39] = 90

        b8OccluderRots[40] = 90

        b8OccluderRots[41] = 270

        b8OccluderRots[42] = 90

        b8OccluderRots[43] = 90

        b8OccluderRots[44] = 315

        b8OccluderRots[45] = 135

        b8OccluderRots[46] = 225

        b8OccluderRots[47] = 270

        b8OccluderRots[48] = 180

        b8OccluderRots[49] = 0

        b8OccluderRots[50] = 90

        b8OccluderRots[51] = 0

        b8OccluderRots[52] = 90

        b8OccluderRots[53] = 90

        b8OccluderRots[54] = 90

        b8OccluderRots[55] = 90

        b8OccluderRots[56] = 90

        b8OccluderRots[57] = 90

        b8OccluderRots[58] = 90

        b8OccluderRots[59] = 90

        b8OccluderRots[60] = 12

        b8OccluderRots[61] = 140

        b8OccluderRots[62] = 255

        b8OccluderRots[63] = 15

        b8OccluderRots[64] = 11

        b8OccluderRots[65] = 10

        b8OccluderRots[66] = 315

        b8OccluderRots[67] = 225

        b8OccluderRots[68] = 135

        b8OccluderRots[69] = 135

        b8OccluderRots[70] = 225

        b8OccluderRots[71] = 45

        b8OccluderRots[72] = 0

        b8OccluderRots[73] = 225

        b8OccluderRots[74] = 45

        b8OccluderRots[75] = 135

        b8OccluderRots[76] = 315

        return b8OccluderRots



    #internal method sets verts

    def getB8StimVerts(self):

        myVerts = list()

        temp = list()

        temp.append(None)

        temp.append(None)

        myVerts.append(list(temp))

        #Stim #1

        temp[0] = asarray([-0.400, -0.283, +0.000, +0.283, +0.400, +0.283, +0.000, -0.283])

        temp[1] = asarray([+0.000, +0.283, +0.400, +0.283, +0.000, -0.283, -0.400, -0.283])

        myVerts.append(list(temp))

        #Stim #2

        temp[0] = asarray([-1.600, -1.131, +0.000, +1.131, +1.600, +1.131, +0.000, -1.131])

        temp[1] = asarray([+0.000, +1.131, +1.600, +1.131, +0.000, -1.131, -1.600, -1.131])

        myVerts.append(list(temp))

        #Stim #3

        temp[0] = asarray([-0.400, -0.375, -0.300, -0.174, +0.000, +0.174, +0.300, +0.375, +0.400, +0.283, +0.000, -0.283])

        temp[1] = asarray([+0.000, +0.416, +0.825, +1.221, +1.600, +1.221, +0.825, +0.416, +0.000, -0.283, -0.400, -0.283])

        myVerts.append(list(temp))

        #Stim #4

        temp[0] = asarray([-0.481, -0.518, -0.481, -0.369, +0.000, +0.369, +0.481, +0.518, +0.481, +0.369, +0.000, -0.369])

        temp[1] = asarray([+0.215, +0.600, +0.983, +1.354, +1.600, +1.354, +0.983, +0.600, +0.215, -0.154, -0.400, -0.154])

        myVerts.append(list(temp))

        #Stim #5

        temp[0] = asarray([-0.373, -0.266, -0.069, +0.000, +0.069, +0.266, +0.373, +0.266, +0.069, +0.000, -0.069, -0.266])

        temp[1] = asarray([+0.000, +0.828, +1.370, +1.600, +1.370, +0.828, +0.000, -0.828, -1.370, -1.600, -1.370, -0.828])

        myVerts.append(list(temp))

        #Stim #6

        temp[0] = asarray([-0.438, -0.277, -0.182, -0.102, +0.000, +0.102, +0.182, +0.277, +0.438, +0.477, +0.393, +0.000, -0.393, -0.477])

        temp[1] = asarray([+0.195, +0.916, +1.190, +1.387, +1.600, +1.387, +1.190, +0.916, +0.195, -0.543, -1.278, -1.600, -1.278, -0.543])

        myVerts.append(list(temp))

        #Stim #7

        temp[0] = asarray([-0.640, -0.571, -0.369, +0.000, +0.369, +0.571, +0.640, +0.571, +0.369, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.000, +0.689, +1.354, +1.600, +1.354, +0.689, +0.000, -0.689, -1.354, -1.600, -1.354, -0.689])

        myVerts.append(list(temp))

        #Stim #8

        temp[0] = asarray([-0.266, +0.000, +0.122, +0.468, +0.988, +1.600, +0.820, +0.066])

        temp[1] = asarray([+0.820, +1.600, +0.988, +0.468, +0.122, +0.000, -0.266, +0.066])

        myVerts.append(list(temp))

        #Stim #9

        temp[0] = asarray([-0.386, -0.386, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.303, +0.589, -0.029])

        temp[1] = asarray([+0.589, +1.303, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.386, -0.386, -0.029])

        myVerts.append(list(temp))

        #Stim #10

        temp[0] = asarray([-0.082, -0.289, +0.000, +0.100, +0.351, +0.740, +1.200, +1.483, +1.600, +1.278, +0.467])

        temp[1] = asarray([+0.186, +0.884, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.393, -0.294])

        myVerts.append(list(temp))

        #Stim #11

        temp[0] = asarray([-1.600, -1.483, -1.200, -0.740, -0.351, -0.100, +0.000, +0.289, +0.082, -0.467, -1.278])

        temp[1] = asarray([+0.000, +0.283, +0.400, +0.500, +0.751, +1.140, +1.600, +0.884, +0.186, -0.294, -0.393])

        myVerts.append(list(temp))

        #Stim #12

        temp[0] = asarray([-0.245, +0.000, +0.075, +0.294, +0.651, +1.131, +0.385, -0.108])

        temp[1] = asarray([+0.781, +1.600, +0.846, +0.122, -0.546, -1.131, -0.733, -0.051])

        myVerts.append(list(temp))

        #Stim #13

        temp[0] = asarray([-0.427, -0.393, -0.283, +0.000, +0.283, +0.393, +0.373, +0.487, +0.727, +1.071, +1.248, +1.131, +0.850, +0.626, +0.106, -0.256])

        temp[1] = asarray([+0.573, +1.278, +1.483, +1.600, +1.483, +1.122, +0.652, +0.198, -0.203, -0.516, -0.848, -1.131, -1.250, -1.181, -0.713, -0.110])

        myVerts.append(list(temp))

        #Stim #14

        temp[0] = asarray([-0.123, -0.167, +0.000, +0.054, +0.257, +0.605, +1.071, +1.216, +1.131, +0.850, +0.570, +0.130])

        temp[1] = asarray([+0.149, +0.883, +1.600, +0.983, +0.401, -0.111, -0.516, -0.848, -1.131, -1.250, -1.131, -0.542])

        myVerts.append(list(temp))

        #Stim #15

        temp[0] = asarray([-0.605, -0.257, -0.054, +0.000, +0.167, +0.123, -0.130, -0.570, -0.850, -1.131, -1.216, -1.071])

        temp[1] = asarray([-0.111, +0.401, +0.983, +1.600, +0.883, +0.149, -0.542, -1.131, -1.250, -1.131, -0.848, -0.516])

        myVerts.append(list(temp))

        #Stim #16

        temp[0] = asarray([-0.533, -0.397, -0.176, +0.000, +0.122, +0.468, +0.988, +1.600, +0.988, +0.468, +0.122, +0.000, -0.176, -0.397])

        temp[1] = asarray([+0.000, +0.843, +1.333, +1.600, +0.988, +0.468, +0.122, +0.000, -0.122, -0.468, -0.988, -1.600, -1.333, -0.843])

        myVerts.append(list(temp))

        #Stim #17

        temp[0] = asarray([-0.533, -0.397, -0.176, +0.000, +0.100, +0.351, +0.740, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.176, -0.397])

        temp[1] = asarray([+0.000, +0.843, +1.333, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.333, -0.843])

        myVerts.append(list(temp))

        #Stim #18

        temp[0] = asarray([-0.575, -0.381, -0.212, +0.000, +0.122, +0.468, +0.988, +1.600, +1.140, +0.752, +0.492, +0.400, +0.283, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.172, +0.923, +1.273, +1.600, +0.988, +0.468, +0.122, +0.000, -0.092, -0.352, -0.740, -1.200, -1.483, -1.600, -1.354, -0.605])

        myVerts.append(list(temp))

        #Stim #19

        temp[0] = asarray([-0.571, -0.369, +0.000, +0.283, +0.400, +0.492, +0.752, +1.140, +1.600, +0.988, +0.468, +0.122, +0.000, -0.212, -0.381, -0.575])

        temp[1] = asarray([+0.605, +1.354, +1.600, +1.483, +1.200, +0.740, +0.352, +0.092, +0.000, -0.122, -0.468, -0.988, -1.600, -1.273, -0.923, -0.172])

        myVerts.append(list(temp))

        #Stim #20

        temp[0] = asarray([-0.575, -0.381, -0.212, +0.000, +0.100, +0.351, +0.740, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.172, +0.923, +1.273, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483, -1.600, -1.354, -0.605])

        myVerts.append(list(temp))

        #Stim #21

        temp[0] = asarray([-0.571, -0.369, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.212, -0.381, -0.575])

        temp[1] = asarray([+0.605, +1.354, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.273, -0.923, -0.172])

        myVerts.append(list(temp))

        #Stim #22

        temp[0] = asarray([-0.640, -0.571, -0.369, +0.000, +0.283, +0.400, +0.492, +0.752, +1.140, +1.600, +1.140, +0.752, +0.492, +0.400, +0.283, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.000, +0.689, +1.354, +1.600, +1.483, +1.200, +0.740, +0.352, +0.092, +0.000, -0.092, -0.352, -0.740, -1.200, -1.483, -1.600, -1.354, -0.689])

        myVerts.append(list(temp))

        #Stim #23

        temp[0] = asarray([-0.640, -0.571, -0.369, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.000, +0.689, +1.354, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483, -1.600, -1.354, -0.689])

        myVerts.append(list(temp))

        #Stim #24

        temp[0] = asarray([-0.294, -0.075, +0.000, +0.075, +0.294, +0.651, +1.131, +0.612, +0.000, -0.612, -1.131, -0.651])

        temp[1] = asarray([+0.122, +0.846, +1.600, +0.846, +0.122, -0.546, -1.131, -0.785, -0.663, -0.785, -1.131, -0.546])

        myVerts.append(list(temp))

        #Stim #25

        temp[0] = asarray([-0.467, -0.350, -0.393, -0.283, +0.000, +0.283, +0.393, +0.350, +0.467, +0.751, +1.131, +0.612, +0.000, -0.612, -1.131, -0.751])

        temp[1] = asarray([+0.102, +0.505, +1.122, +1.483, +1.600, +1.483, +1.122, +0.505, -0.102, -0.688, -1.131, -0.785, -0.663, -0.785, -1.131, -0.688])

        myVerts.append(list(temp))

        #Stim #26

        temp[0] = asarray([-0.294, -0.075, +0.000, +0.054, +0.257, +0.605, +1.071, +1.248, +1.131, +0.850, +0.570, +0.179, -0.282, -0.742, -1.131, -0.651])

        temp[1] = asarray([+0.122, +0.846, +1.600, +0.983, +0.401, -0.111, -0.516, -0.848, -1.131, -1.250, -1.131, -0.871, -0.780, -0.871, -1.131, -0.546])

        myVerts.append(list(temp))

        #Stim #27

        temp[0] = asarray([-0.257, -0.054, +0.000, +0.075, +0.294, +0.651, +1.131, +0.742, +0.282, -0.179, -0.571, -0.850, -1.131, -1.248, -1.071, -0.605])

        temp[1] = asarray([+0.401, +0.983, +1.600, +0.846, +0.122, -0.546, -1.131, -0.871, -0.780, -0.871, -1.131, -1.250, -1.131, -0.848, -0.516, -0.111])

        myVerts.append(list(temp))

        #Stim #28

        temp[0] = asarray([-0.257, -0.054, +0.000, +0.054, +0.257, +0.605, +1.071, +1.248, +1.131, +0.850, +0.570, +0.308, +0.000, -0.308, -0.570, -0.850, -1.131, -1.248, -1.071, -0.605])

        temp[1] = asarray([+0.401, +0.983, +1.600, +0.983, +0.401, -0.111, -0.516, -0.848, -1.131, -1.250, -1.131, -0.957, -0.896, -0.957, -1.131, -1.250, -1.131, -0.848, -0.516, -0.111])

        myVerts.append(list(temp))

        #Stim #29

        temp[0] = asarray([-0.487, -0.373, -0.393, -0.283, +0.000, +0.283, +0.393, +0.350, +0.467, +0.751, +1.131, +0.742, +0.282, -0.179, -0.571, -0.850, -1.131, -1.248, -1.071, -0.727])

        temp[1] = asarray([+0.198, +0.652, +1.122, +1.483, +1.600, +1.483, +1.122, +0.505, -0.102, -0.688, -1.131, -0.871, -0.780, -0.871, -1.131, -1.250, -1.131, -0.848, -0.516, -0.203])

        myVerts.append(list(temp))

        #Stim #30

        temp[0] = asarray([-0.467, -0.350, -0.393, -0.283, +0.000, +0.283, +0.393, +0.373, +0.487, +0.727, +1.071, +1.248, +1.131, +0.850, +0.570, +0.179, -0.282, -0.742, -1.131, -0.751])

        temp[1] = asarray([+0.102, +0.505, +1.122, +1.483, +1.600, +1.483, +1.122, +0.652, +0.198, -0.203, -0.516, -0.848, -1.131, -1.250, -1.131, -0.871, -0.780, -0.871, -1.131, -0.688])

        myVerts.append(list(temp))

        #Stim #31

        temp[0] = asarray([-0.487, -0.373, -0.393, -0.283, +0.000, +0.283, +0.393, +0.373, +0.487, +0.727, +1.071, +1.248, +1.131, +0.850, +0.570, +0.308, +0.000, -0.308, -0.570, -0.850, -1.131, -1.248, -1.071, -0.727])

        temp[1] = asarray([+0.198, +0.652, +1.122, +1.483, +1.600, +1.483, +1.122, +0.652, +0.198, -0.203, -0.516, -0.848, -1.131, -1.250, -1.131, -0.957, -0.896, -0.957, -1.131, -1.250, -1.131, -0.848, -0.516, -0.203])

        myVerts.append(list(temp))

        #Stim #32

        temp[0] = asarray([-1.600, -0.988, -0.468, -0.122, +0.000, +0.122, +0.468, +0.988, +1.600, +0.988, +0.468, +0.122, +0.000, -0.122, -0.468, -0.988])

        temp[1] = asarray([+0.000, +0.122, +0.468, +0.988, +1.600, +0.988, +0.468, +0.122, +0.000, -0.122, -0.468, -0.988, -1.600, -0.988, -0.468, -0.122])

        myVerts.append(list(temp))

        #Stim #33

        temp[0] = asarray([-1.600, -0.988, -0.468, -0.122, +0.000, +0.122, +0.468, +0.988, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140])

        temp[1] = asarray([+0.000, +0.122, +0.468, +0.988, +1.600, +0.988, +0.468, +0.122, +0.000, -0.100, -0.351, -0.740, -1.200, -1.483, -1.600, -1.483, -1.200, -0.740, -0.351, -0.100])

        myVerts.append(list(temp))

        #Stim #34

        temp[0] = asarray([-1.600, -1.483, -1.200, -0.740, -0.351, -0.100, +0.000, +0.100, +0.351, +0.740, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.100, -0.351, -0.740, -1.200, -1.483])

        temp[1] = asarray([+0.000, +0.283, +0.400, +0.500, +0.751, +1.140, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.140, -0.751, -0.500, -0.400, -0.283])

        myVerts.append(list(temp))

        #Stim #35

        temp[0] = asarray([-1.600, -0.988, -0.468, -0.122, +0.000, +0.100, +0.351, +0.740, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140])

        temp[1] = asarray([+0.000, +0.122, +0.468, +0.988, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483, -1.600, -1.483, -1.200, -0.740, -0.351, -0.100])

        myVerts.append(list(temp))

        #Stim #36

        temp[0] = asarray([-1.600, -1.483, -1.200, -0.894, -0.635, -0.461, -0.400, -0.283, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.100, -0.351, -0.740, -1.200, -1.483])

        temp[1] = asarray([+0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.140, -0.751, -0.500, -0.400, -0.283])

        myVerts.append(list(temp))

        #Stim #37

        temp[0] = asarray([-1.600, -1.483, -1.200, -0.894, -0.635, -0.461, -0.400, -0.283, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483])

        temp[1] = asarray([+0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483, -1.600, -1.483, -1.200, -0.894, -0.635, -0.461, -0.400, -0.283])

        myVerts.append(list(temp))

        #Stim #38

        temp[0] = asarray([-0.571, +0.000, +1.131, +1.600, +1.200, +0.740, +0.351, +0.100, +0.000, -0.212, -0.381, -0.575])

        temp[1] = asarray([+0.605, +1.600, +1.131, +0.000, -0.400, -0.500, -0.751, -1.140, -1.600, -1.273, -0.923, -0.172])

        myVerts.append(list(temp))

        #Stim #39

        temp[0] = asarray([-0.575, -0.381, -0.212, +0.000, +0.100, +0.351, +0.740, +1.200, +1.600, +1.131, +0.000, -0.571])

        temp[1] = asarray([+0.172, +0.923, +1.273, +1.600, +1.140, +0.751, +0.500, +0.400, +0.000, -1.131, -1.600, -0.605])

        myVerts.append(list(temp))

        #Stim #40

        temp[0] = asarray([-0.257, -0.054, +0.000, +0.054, +0.257, +0.605, +1.071, +1.131, +0.000, -1.131, -1.071, -0.605])

        temp[1] = asarray([+0.401, +0.983, +1.600, +0.983, +0.401, -0.111, -0.516, -1.131, -1.600, -1.131, -0.516, -0.111])

        myVerts.append(list(temp))

        #Stim #41

        temp[0] = asarray([-0.640, -0.571, +0.000, +1.131, +1.600, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.000, +0.689, +1.600, +1.131, +0.000, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483, -1.600, -1.354, -0.689])

        myVerts.append(list(temp))

        #Stim #42

        temp[0] = asarray([-0.640, -0.571, -0.369, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.600, +1.131, +0.000, -0.571])

        temp[1] = asarray([+0.000, +0.689, +1.354, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.000, -1.131, -1.600, -0.689])

        myVerts.append(list(temp))

        #Stim #43

        temp[0] = asarray([-0.487, -0.373, -0.393, -0.283, +0.000, +0.283, +0.393, +0.373, +0.487, +0.727, +1.071, +1.131, +0.000, -1.131, -1.071, -0.727])

        temp[1] = asarray([+0.198, +0.652, +1.122, +1.483, +1.600, +1.483, +1.122, +0.652, +0.198, -0.203, -0.516, -1.131, -1.600, -1.131, -0.516, -0.203])

        myVerts.append(list(temp))

        #Stim #44

        temp[0] = asarray([-1.600, -1.200, -0.894, -0.635, -0.461, -0.400, -0.283, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.000, -1.131])

        temp[1] = asarray([+0.000, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.600, -1.131])

        myVerts.append(list(temp))

        #Stim #45

        temp[0] = asarray([-1.600, -1.200, -0.894, -0.635, -0.461, -0.400, +0.000, +1.131, +1.600, +1.200, +0.894, +0.635, +0.461, +0.400, +0.000, -1.131])

        temp[1] = asarray([+0.000, +0.400, +0.461, +0.635, +0.894, +1.200, +1.600, +1.131, +0.000, -0.400, -0.461, -0.635, -0.894, -1.200, -1.600, -1.131])

        myVerts.append(list(temp))

        #Stim #46

        temp[0] = asarray([-1.600, -1.200, -0.894, -0.635, -0.461, -0.400, +0.000, +1.131, +1.600, +1.131, +0.000, -1.131])

        temp[1] = asarray([+0.000, +0.400, +0.461, +0.635, +0.894, +1.200, +1.600, +1.131, +0.000, -1.131, -1.600, -1.131])

        myVerts.append(list(temp))

        #Stim #47

        temp[0] = asarray([-1.600, -1.200, -0.894, -0.635, -0.461, -0.400, -0.283, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.600, +1.131, +0.000, -1.131])

        temp[1] = asarray([+0.000, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.000, -1.131, -1.600, -1.131])

        myVerts.append(list(temp))

        #Stim #48

        temp[0] = asarray([-1.600, -1.131, +0.000, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.100, -0.351, -0.740, -1.200])

        temp[1] = asarray([+0.000, +1.131, +1.600, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.140, -0.751, -0.500, -0.400])

        myVerts.append(list(temp))

        #Stim #49

        temp[0] = asarray([-1.600, -1.483, -1.200, -0.894, -0.635, -0.461, -0.400, +0.000, +1.131, +1.600, +1.200, +0.740, +0.351, +0.100, +0.000, -0.100, -0.351, -0.740, -1.200, -1.483])

        temp[1] = asarray([+0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.600, +1.131, +0.000, -0.400, -0.500, -0.751, -1.140, -1.600, -1.140, -0.751, -0.500, -0.400, -0.283])

        myVerts.append(list(temp))

        #Stim #50

        temp[0] = asarray([-1.600, -1.131, +0.000, +1.131, +1.600, +1.200, +0.740, +0.351, +0.100, +0.000, -0.100, -0.351, -0.740, -1.200])

        temp[1] = asarray([+0.000, +1.131, +1.600, +1.131, +0.000, -0.400, -0.500, -0.751, -1.140, -1.600, -1.140, -0.751, -0.500, -0.400])

        myVerts.append(list(temp))

        #Stim #51

        temp[0] = asarray([-1.600, -0.988, -0.468, -0.122, +0.000, +0.100, +0.351, +0.740, +1.200, +1.600, +1.131, +0.000, -0.400, -0.500, -0.751, -1.140])

        temp[1] = asarray([+0.000, +0.122, +0.468, +0.988, +1.600, +1.140, +0.751, +0.500, +0.400, +0.000, -1.131, -1.600, -1.200, -0.740, -0.351, -0.100])

        myVerts.append(list(temp))

        #Stim #52 - accidental convex version of 16

        temp[0] = asarray([-0.533, -0.397, -0.176, +0.000, +0.122, +0.468, +0.988, +1.600, +0.988, +0.468, +0.122, +0.000, -0.176, -0.397])

        temp[1] = asarray([+0.000, +0.843, +1.333, +1.600, +0.988, +0.468, +0.122, +0.000, -0.122, -0.468, -0.988, -1.600, -1.333, -0.843])

        myVerts.append(list(temp))

        #Stim #53   accidental convex version of 17

        temp[0] = asarray([-0.533, -0.397, -0.176, +0.000, +0.100, +0.351, +0.740, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.176, -0.397])

        temp[1] = asarray([+0.000, +0.843, +1.333, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.333, -0.843])

        myVerts.append(list(temp))

        #Stim #54   accidental convex version of 18

        temp[0] = asarray([-0.575, -0.381, -0.212, +0.000, +0.122, +0.468, +0.988, +1.600, +1.140, +0.752, +0.492, +0.400, +0.283, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.172, +0.923, +1.273, +1.600, +0.988, +0.468, +0.122, +0.000, -0.092, -0.352, -0.740, -1.200, -1.483, -1.600, -1.354, -0.605])

        myVerts.append(list(temp))

        #Stim #55   accidental convex version of 19

        temp[0] = asarray([-0.571, -0.369, +0.000, +0.283, +0.400, +0.492, +0.752, +1.140, +1.600, +0.988, +0.468, +0.122, +0.000, -0.212, -0.381, -0.575])

        temp[1] = asarray([+0.605, +1.354, +1.600, +1.483, +1.200, +0.740, +0.352, +0.092, +0.000, -0.122, -0.468, -0.988, -1.600, -1.273, -0.923, -0.172])

        myVerts.append(list(temp))

        #Stim #56   accidental convex version of 20

        temp[0] = asarray([-0.575, -0.381, -0.212, +0.000, +0.100, +0.351, +0.740, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.172, +0.923, +1.273, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483, -1.600, -1.354, -0.605])

        myVerts.append(list(temp))

        #Stim #57   accidental convex version of 21

        temp[0] = asarray([-0.571, -0.369, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.212, -0.381, -0.575])

        temp[1] = asarray([+0.605, +1.354, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.273, -0.923, -0.172])

        myVerts.append(list(temp))

        #Stim #58   accidental convex version of 22

        temp[0] = asarray([-0.640, -0.571, -0.369, +0.000, +0.283, +0.400, +0.492, +0.752, +1.140, +1.600, +1.140, +0.752, +0.492, +0.400, +0.283, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.000, +0.689, +1.354, +1.600, +1.483, +1.200, +0.740, +0.352, +0.092, +0.000, -0.092, -0.352, -0.740, -1.200, -1.483, -1.600, -1.354, -0.689])

        myVerts.append(list(temp))

        #Stim #59   accidental convex version of 23

        temp[0] = asarray([-0.640, -0.571, -0.369, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.369, -0.571])

        temp[1] = asarray([+0.000, +0.689, +1.354, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483, -1.600, -1.354, -0.689])

        myVerts.append(list(temp))

        #Stim #60   accidental convex version of 25

        temp[0] = asarray([-0.467, -0.350, -0.393, -0.283, +0.000, +0.283, +0.393, +0.350, +0.467, +0.751, +1.131, +0.612, +0.000, -0.612, -1.131, -0.751])

        temp[1] = asarray([+0.102, +0.505, +1.122, +1.483, +1.600, +1.483, +1.122, +0.505, -0.102, -0.688, -1.131, -0.785, -0.663, -0.785, -1.131, -0.688])

        myVerts.append(list(temp))

        #Stim #61   accidental convex version of 26

        temp[0] = asarray([-0.294, -0.075, +0.000, +0.054, +0.257, +0.605, +1.071, +1.248, +1.131, +0.850, +0.570, +0.179, -0.282, -0.742, -1.131, -0.651])

        temp[1] = asarray([+0.122, +0.846, +1.600, +0.983, +0.401, -0.111, -0.516, -0.848, -1.131, -1.250, -1.131, -0.871, -0.780, -0.871, -1.131, -0.546])

        myVerts.append(list(temp))

        #Stim #62   accidental convex version of 27

        temp[0] = asarray([-0.257, -0.054, +0.000, +0.075, +0.294, +0.651, +1.131, +0.742, +0.282, -0.179, -0.571, -0.850, -1.131, -1.248, -1.071, -0.605])

        temp[1] = asarray([+0.401, +0.983, +1.600, +0.846, +0.122, -0.546, -1.131, -0.871, -0.780, -0.871, -1.131, -1.250, -1.131, -0.848, -0.516, -0.111])

        myVerts.append(list(temp))

        #Stim #63   accidental convex version of 29

        temp[0] = asarray([-0.487, -0.373, -0.393, -0.283, +0.000, +0.283, +0.393, +0.350, +0.467, +0.751, +1.131, +0.742, +0.282, -0.179, -0.571, -0.850, -1.131, -1.248, -1.071, -0.727])

        temp[1] = asarray([+0.198, +0.652, +1.122, +1.483, +1.600, +1.483, +1.122, +0.505, -0.102, -0.688, -1.131, -0.871, -0.780, -0.871, -1.131, -1.250, -1.131, -0.848, -0.516, -0.203])

        myVerts.append(list(temp))

        #Stim #64   accidental convex version of 30

        temp[0] = asarray([-0.467, -0.350, -0.393, -0.283, +0.000, +0.283, +0.393, +0.373, +0.487, +0.727, +1.071, +1.248, +1.131, +0.850, +0.570, +0.179, -0.282, -0.742, -1.131, -0.751])

        temp[1] = asarray([+0.102, +0.505, +1.122, +1.483, +1.600, +1.483, +1.122, +0.652, +0.198, -0.203, -0.516, -0.848, -1.131, -1.250, -1.131, -0.871, -0.780, -0.871, -1.131, -0.688])

        myVerts.append(list(temp))

        #Stim #65   accidental convex version of 31

        temp[0] = asarray([-0.487, -0.373, -0.393, -0.283, +0.000, +0.283, +0.393, +0.373, +0.487, +0.727, +1.071, +1.248, +1.131, +0.850, +0.570, +0.308, +0.000, -0.308, -0.570, -0.850, -1.131, -1.248, -1.071, -0.727])

        temp[1] = asarray([+0.198, +0.652, +1.122, +1.483, +1.600, +1.483, +1.122, +0.652, +0.198, -0.203, -0.516, -0.848, -1.131, -1.250, -1.131, -0.957, -0.896, -0.957, -1.131, -1.250, -1.131, -0.848, -0.516, -0.203])

        myVerts.append(list(temp))

        #Stim #66   accidental convex version of 32

        temp[0] = asarray([-1.600, -0.988, -0.468, -0.122, +0.000, +0.122, +0.468, +0.988, +1.600, +0.988, +0.468, +0.122, +0.000, -0.122, -0.468, -0.988])

        temp[1] = asarray([+0.000, +0.122, +0.468, +0.988, +1.600, +0.988, +0.468, +0.122, +0.000, -0.122, -0.468, -0.988, -1.600, -0.988, -0.468, -0.122])

        myVerts.append(list(temp))

        #Stim #67   accidental convex version of 33

        temp[0] = asarray([-1.600, -0.988, -0.468, -0.122, +0.000, +0.122, +0.468, +0.988, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140])

        temp[1] = asarray([+0.000, +0.122, +0.468, +0.988, +1.600, +0.988, +0.468, +0.122, +0.000, -0.100, -0.351, -0.740, -1.200, -1.483, -1.600, -1.483, -1.200, -0.740, -0.351, -0.100])

        myVerts.append(list(temp))

        #Stim #68   accidental convex version of 34

        temp[0] = asarray([-1.600, -1.483, -1.200, -0.740, -0.351, -0.100, +0.000, +0.100, +0.351, +0.740, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.100, -0.351, -0.740, -1.200, -1.483])

        temp[1] = asarray([+0.000, +0.283, +0.400, +0.500, +0.751, +1.140, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.140, -0.751, -0.500, -0.400, -0.283])

        myVerts.append(list(temp))

        #Stim #69   accidental convex version of 35

        temp[0] = asarray([-1.600, -0.988, -0.468, -0.122, +0.000, +0.100, +0.351, +0.740, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140])

        temp[1] = asarray([+0.000, +0.122, +0.468, +0.988, +1.600, +1.140, +0.751, +0.500, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483, -1.600, -1.483, -1.200, -0.740, -0.351, -0.100])

        myVerts.append(list(temp))

        #Stim #70   accidental convex version of 36

        temp[0] = asarray([-1.600, -1.483, -1.200, -0.894, -0.635, -0.461, -0.400, -0.283, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.100, -0.351, -0.740, -1.200, -1.483])

        temp[1] = asarray([+0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.140, -0.751, -0.500, -0.400, -0.283])

        myVerts.append(list(temp))

        #Stim #71   accidental convex version of 37

        temp[0] = asarray([-1.600, -1.483, -1.200, -0.894, -0.635, -0.461, -0.400, -0.283, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483])

        temp[1] = asarray([+0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.483, -1.600, -1.483, -1.200, -0.894, -0.635, -0.461, -0.400, -0.283])

        myVerts.append(list(temp))

        #Stim #72   accidental convex version of 43

        temp[0] = asarray([-0.487, -0.373, -0.393, -0.283, +0.000, +0.283, +0.393, +0.373, +0.487, +0.727, +1.071, +1.131, +0.000, -1.131, -1.071, -0.727])

        temp[1] = asarray([+0.198, +0.652, +1.122, +1.483, +1.600, +1.483, +1.122, +0.652, +0.198, -0.203, -0.516, -1.131, -1.600, -1.131, -0.516, -0.203])

        myVerts.append(list(temp))

        #Stim #73   accidental convex version of 44

        temp[0] = asarray([-1.600, -1.200, -0.894, -0.635, -0.461, -0.400, -0.283, +0.000, +0.283, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.000, -1.131])

        temp[1] = asarray([+0.000, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.461, -0.635, -0.894, -1.200, -1.600, -1.131])

        myVerts.append(list(temp))

        #Stim #74   accidental convex version of 45

        temp[0] = asarray([-1.600, -1.200, -0.894, -0.635, -0.461, -0.400, +0.000, +1.131, +1.600, +1.200, +0.894, +0.635, +0.461, +0.400, +0.000, -1.131])

        temp[1] = asarray([+0.000, +0.400, +0.461, +0.635, +0.894, +1.200, +1.600, +1.131, +0.000, -0.400, -0.461, -0.635, -0.894, -1.200, -1.600, -1.131])

        myVerts.append(list(temp))

        #Stim #75   accidental convex version of 48

        temp[0] = asarray([-1.600, -1.131, +0.000, +0.400, +0.461, +0.635, +0.894, +1.200, +1.483, +1.600, +1.483, +1.200, +0.740, +0.351, +0.100, +0.000, -0.100, -0.351, -0.740, -1.200])

        temp[1] = asarray([+0.000, +1.131, +1.600, +1.200, +0.894, +0.635, +0.461, +0.400, +0.283, +0.000, -0.283, -0.400, -0.500, -0.751, -1.140, -1.600, -1.140, -0.751, -0.500, -0.400])

        myVerts.append(list(temp))

        #Stim #76   accidental convex version of 51

        temp[0] = asarray([-1.600, -0.988, -0.468, -0.122, +0.000, +0.100, +0.351, +0.740, +1.200, +1.600, +1.131, +0.000, -0.400, -0.500, -0.751, -1.140])

        temp[1] = asarray([+0.000, +0.122, +0.468, +0.988, +1.600, +1.140, +0.751, +0.500, +0.400, +0.000, -1.131, -1.600, -1.200, -0.740, -0.351, -0.100])

        myVerts.append(list(temp))

        #Stim #77   square DVP add from b8stim_new (shape 43) 8/2/13

        temp[0] = asarray([-1.6,-1.6,-1.6,-1.2,-0.8,-0.4,0.0,0.0,0.0,0.4,0.8,1.2,1.6,1.6,1.6,1.2,0.8,0.4,0.0,0.0,0.0,-0.4,-0.8,-1.2,-1.6,-1.6,-1.6])

        temp[1] = asarray([0.0,0.0,0.0,0.4,0.8,1.2,1.6,1.6,1.6,1.2,0.8,0.4,0.0,0.0,0.0,-0.4,-0.8,-1.2,-1.6,-1.6,-1.6,-1.2,-0.8,-0.4,0.0,0.0,0.0])
        myVerts.append(list(temp))

        return myVerts

