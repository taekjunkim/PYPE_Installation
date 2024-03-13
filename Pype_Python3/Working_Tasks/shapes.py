import sys,types, math, pdb
from pype import *
from events import *
from tkinter import *
#bar
def createBar(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG):
    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    s.fill(myColor)
    
    s.rotate(myRot, 0, 1)
    s.myColor = myColor
    s.myH = round(s.h)
    s.myW = round(s.w)
    return s

#ellipse
def createEllipse(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG):

    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    s.fill(myBG)
    s.ellipse(myColor, myWidth, myLength)
    s.rotate(myRot, 0, 1)
    s.myColor = myColor
    s.myH = round(s.h)
    s.myW = round(s.w)
    return s

def createDiamond(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG):
#diamond
    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    s.fill(myBG)
    
    verts0 = [[0,-myLength/2.0],[myWidth/2.0,0],[0,myLength/2.0],[-myWidth/2.0,0]]
    s.polygon(myColor, verts0, 0)
    s.rotate(myRot, 0, 1)
    s.myColor = myColor
    s.myH = round(s.h)
    s.myW = round(s.w)
    return s

def createStar(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG):
#star
    l = round(myLength)
    w = round(myWidth)
    s = Sprite(round(myWidth)*4, round(myLength)*4, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    s.fill(myBG)
    #Computing vertices
    pixres = 1 #computed every pixel                
    def yvertcalc1 (x,):
            return (w/2.0)-(w/2.0)*sqrt(1-pow((x-(l/2.0))/(l/2.0),2))
    #segment 1 - this is the x>0y>0 quadrant
    xs1 = arange(l/2,-1,-pixres,Float)#so that both ends are included
    ys = fromfunction(yvertcalc1,(int(round((l/2)+1)),)) 
    ys1 = ys[::-pixres]
    #segment 4 is just the same with negative y in reverse order
    xs4 = arange(0,(l/2)+1,pixres,Float)
    ys4 =-ys[::pixres]
    #segment 2 - this is same as segment 1 in reverse order 
    xs2 = -arange(0,(l/2)+1,pixres,Float)
    ys2 = ys[::pixres]
    #segment 3 is the same with negative y in reverse order
    xs3 = -xs1
    ys3 = -ys[::-pixres]
    xs = concatenate((xs1,xs2,xs3,xs4),1)
    ys = concatenate((ys1,ys2,ys3,ys4),1)
    pointslist = transpose(array([xs,ys]))
    s.polygon(myColor, pointslist, 0)
    s.rotate(myRot, 0, 1)
    s.myColor = myColor
    s.myH = s.h/4
    s.myW = s.w/4
    return s

def createSinusoid(myWidth, myLength, myFB, myRot, myX, myY,myBG,color1, color2, frequency,phase=90,isCircle=1):

    #phase is not currently working

    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    s.fill(myBG)

    #offset = round((float(phase ) / 360)  *  size(s.array,0))
    offset = 0
    vals = range(size(s.array,0)+offset,0+offset,-1)
    xVals = sin(frequency * (array(vals, 'f') % size(s.array,0)) / size(vals,0) * (2*pi)-(pi*phase/180.0))
    rVals =  ((color2[0] - color1[0])/2) * xVals + (color1[0]+color2[0])/2
    gVals =  ((color2[1] - color1[1])/2) * xVals + (color1[1]+color2[1])/2
    bVals =  ((color2[2] - color1[2])/2) * xVals + (color1[2]+color2[2])/2
    s.array[:,:,0] = [list(rVals.astype(UnsignedInt8)) for row in range(size(s.array,1))]
    s.array[:,:,1] = [list(gVals.astype(UnsignedInt8)) for row in range(size(s.array,1))]
    s.array[:,:,2] = [list(bVals.astype(UnsignedInt8)) for row in range(size(s.array,1))]
    #print s.array[:,:,0]
    #s.array[:,:,1] = list(gVals.astype(UnsignedInt8))) * size(s.array,1)
    #s.array[:,:,2] = list(bVals.astype(UnsignedInt8))) * size(s.array,1)
    #xVals = range(0+offset,size(s.array,0)+offset,1)
    #for i in range(0,size(s.array,0)):
        #print xVals[i],frequency/xVals[i],sin(frequency/xVals[i]) size(xVals,0)
        #print color1, color2

        #rVal = (color2[0] - color1[0])/2 * sin(frequency * (float(xVals[i]) % size(xVals,0))/size(xVals,0) * (2*pi)-(pi*phase/180.0)) + (color1[0]+color2[0])/2
        #gVal = (color2[1] - color1[1])/2 * sin(frequency * (float(xVals[i]) % size(xVals,0))/size(xVals,0) * (2*pi)-(pi*phase/180.0)) + (color1[1]+color2[1])/2
        #bVal = (color2[2] - color1[2])/2 * sin(frequency * (float(xVals[i]) % size(xVals,0))/size(xVals,0) * (2*pi)-(pi*phase/180.0)) + (color1[2]+color2[2])/2
        #print xVals[i],(float(xVals[i]) % size(xVals,0))/size(xVals,0)
        #for j in range(0, size(s.array,1)):
        #s.array[i,:,0] = rVal
        #s.array[i,:,1] = gVal
        #s.array[i,:,2] = bVal
    #s.array[i,:,0] = rVals
    #s.array[i,:,1] = gVals
    #s.array[i,:,2] = bVals
    s.rotate(myRot, 1, 1)
    if(isCircle):
        s.circmask(0, 0, myWidth/2)
    #print s.array[0]
    #print s.array[1]
    #print s.array[2]
    return s

def addEllipse(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG,s):

#    s.fill(myBG)
    s.ellipse(myColor, myWidth, myLength, myX, myY)
#    s.rotate(myRot, 0, 1)
    s.myColor = myColor
    s.myH = round(s.h)
    s.myW = round(s.w)
    return s

def addBar(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG,s):
    s.rect(myX, myY, myWidth, myLength, myColor)
    #s.rectangle(myX, myY, myWidth, myLength, myColor)
#    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    #s.fill(myColor)
    
#    s.rotate(myRot, 0, 1)
    s.myColor = myColor
    s.myH = round(s.h)
    s.myW = round(s.w)
    return s

def addPacman(s, color, x, y):
    s.pacman(color, x, y)
    return s

def addDiamond(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG,s):
#diamond
    #s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    #s.fill(myBG)
    
    verts0 = [[0+myX,-myLength/2.0+myY],[myWidth/2.0+myX,0+myY],[0+myX,myLength/2.0+myY],[-myWidth/2.0+myX,0+myY]]
    s.polygon(myColor, verts0, 0)
    #s.rotate(myRot, 0, 1)
    #s.myColor = myColor
    s.myH = round(s.h)
    s.myW = round(s.w)
    return s

def addStar(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG,s):
#star
    l = round(myLength)
    w = round(myWidth)
    #s = Sprite(round(myWidth)*4, round(myLength)*4, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    #s.fill(myBG)
    #Computing vertices
    pixres = 1 #computed every pixel                
    def yvertcalc1 (x,):
            return (w/2.0)-(w/2.0)*sqrt(1-pow((x-(l/2.0))/(l/2.0),2))
    #segment 1 - this is the x>0y>0 quadrant
    xs1 = arange(l/2,-1,-pixres,Float)#so that both ends are included
    ys = fromfunction(yvertcalc1,(int(round((l/2)+1)),)) 
    ys1 = ys[::-pixres]
    #segment 4 is just the same with negative y in reverse order
    xs4 = arange(0,(l/2)+1,pixres,Float)
    ys4 =-ys[::pixres]
    #segment 2 - this is same as segment 1 in reverse order 
    xs2 = -arange(0,(l/2)+1,pixres,Float)
    ys2 = ys[::pixres]
    #segment 3 is the same with negative y in reverse order
    xs3 = -xs1
    ys3 = -ys[::-pixres]
    xs = concatenate((xs1+myX,xs2+myX,xs3+myX,xs4+myX),1)
    ys = concatenate((ys1+myY,ys2+myY,ys3+myY,ys4+myY),1)
    pointslist = transpose(array([xs,ys]))
    s.polygon(myColor, pointslist, 0)
    #s.rotate(myRot, 0, 1)
    #s.myColor = myColor
    s.myH = s.h/4
    s.myW = s.w/4
    return s

#            s3 = shapeDict.get(13,0)(app.fb, (200,20,20), 360-orientation, ((200-i,20+100),(300-i,20+100),(250-i,20+150)), myBG,s2)

def addCircleFill(myRadius, myFB, myColor, myRot, myX, myY, myBG, s):

#    s.fill(myBG)
    s.circlefill(myColor, myRadius, myX, myY)
#    s.rotate(myRot, 0, 1)
    s.myColor = myColor
    s.myH = round(s.h)
    s.myW = round(s.w)
    return s

def addPolygon(myFB, myColor, myRot, myVerts, myBG, s):

#    s.fill(myBG)
    s.polygon(myColor, myVerts, width=0)
#    s.rotate(myRot, 0, 1)
    s.myColor = myColor
#    s.myH = round(s.h)
#    s.myW = round(s.w)
    return s


shapeDict = {
    0:createBar,
    #1:createCart,
    #2:createHyper,
    #3:createPolar,
    4:createEllipse,
    5:createDiamond,
    6:createStar,
    7:createSinusoid,
    8:addBar,
    9:addEllipse,
    10:addDiamond,
    11:addStar,

    12:addCircleFill,
    13:addPolygon,
    14:addPacman
}


def isSymmetricAroundHorizontal(shapeCode,width, length):
    if(shapeCode == 0):
        return 1

    if(shapeCode == 4):
        return 1
        
    if(shapeCode == 5):
        return 1

    if(shapeCode == 6):
        if(length == width):
            return 1
        else:
            return 0
            

def isSymmetricAroundVertical(shapeCode, myWidth, myLength):

    if(shapeCode == 0):
        if(length == width):
            return 1
        else:
            return 0

    if(shapeCode == 4):
        if(length == width):
            return 1
        else:
            return 0
        
    if(shapeCode == 5):
        if(length == width):
            return 1
        else:
            return 0

    if(shapeCode == 6):
        if(length == width):
            return 1
        else:
            return 0


def hasPerfectSymmetry(shapeCode, myWidth, myLength):

    if(shapeCode == 4):
        if(length == width):
           return 1

    return 0
    
