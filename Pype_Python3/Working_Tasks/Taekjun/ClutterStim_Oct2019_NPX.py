# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 18:40:54 2017

SlitViewing.py is a Fixation task for Shape moving behind the slit

@author: taekjunkim
"""

#%%
import os, sys, types   ## os is needed to specify file location
from pype import *
from Numeric import *   ## Numeric is needed for array computation. Possible to upgrade?
import numpy as np
import h5py   ## to load mat file later than -v7.3
import math
from random import *
from shapes import *   ## because of create bar for blank stimuli
from colors import *
from b8StimFactory import *

#%%

def RunSet(app):
    app.taskObject.runSet(app)

def cleanup(app):
    app.taskObject.cleanup(app)

def main(app):
    app.taskObject = ClutterStim(app)
    app.globals = Holder()
    app.idlefb()
    app.startfn = RunSet

#%%
# This is also something that all tasks have, and it's a python thing.
# Don't touch it.
if not __name__ == '__main__':
        loadwarn(__name__)
else:
        dump(sys.argv[1])


class ClutterStim:

    def __init__(self, app):
        self.createParamTable(app)
        self.app = app
        # 54 unique conditons, 15 repetition
        # required sprites: center, surround1, surround3, surround6, 
        #                 : surround middle, surround far 
        self.StimInfoTable = np.array([],int);
        self.myEmptySprites = list();      
        self.myCenterSprites_Gray = list(); 
        self.myCenterSprites_Color = list();         
        self.mySurr1NearSprites_Gray = list();        
        self.mySurr3NearSprites_Gray = list();        
        self.mySurr6NearSprites_Gray = list();        
        self.mySurr6NearSprites_Color = list();                
        self.mySurrMiddleSprites_Gray = list();        
        self.mySurrFarSprites_Gray = list();                
        self.mySurr6NearCircleSprites_Gray = list();                        
        self.mySurr12NearSmallSprites_Gray = list();                                
        self.mySurr12NearSmallCircleSprites_Gray = list();                                        
        self.myGrayCenter6SurrPS_Sprites = list();                                
        self.myGrayCenter6CircleSurrPS_Sprites = list();                                
        self.myGrayCenter12SmallSurrPS_Sprites = list();                                     
        self.myGrayCenter12SmallCircleSurrPS_Sprites = list();                                                        
        self.myid = list();
        self.numStim = 138*10;
        self.taskparam = 0; # parameter for NeuroPixel


    def createStimuli(self,app):

        ## global parameters
        gParam = app.getcommon()

        ## parameters defined in this task
        self.params = self.myTaskParams.check()
        params = self.params

        randomize_stims = params['randomize_stimuli']
        myBG = params['bg_during']
        BGlist = list(myBG)

        myFB = app.fb  ## framebuffer

        ### Number of frames to show visual stimuli
        self.mon_Hz = 100;    
        self.Numframes = self.mon_Hz*params['stimon']/1000;

        ### Stimulus size based on RF eccentricity
        RF_X = params['RF_centerX']
        RF_Y = params['RF_centerY']
        RF_ecc = ((RF_X**2)+(RF_Y**2))**0.5
        self.RF_X = RF_X; 
        self.RF_Y = RF_Y;        
        # RF size in pixel
        # In pre-computed matlab file, RF size was assumed to be 100 pixel
        # Therefore, it needs to be scaled
        RFScaleFactor = 0.625;

        if params['V2orV4']==1:
            RF_dia = int(gParam['mon_ppd']+RFScaleFactor*RF_ecc); 
        elif params['V2orV4']==0:
            RF_dia = int((gParam['mon_ppd']+RFScaleFactor*RF_ecc)*0.5); 
        
        ### StimInfoTable
        # No stim (1)
        # Gray Center alone (2-9)
        # Gray 1 Surround alone (10)
        # Gray Center + Gray 1 Surround (11-18)
        # Gray 3 Surround alone (19)
        # Gray Center + Gray 3 Surround (20-27)
        # Gray 6 Surround alone (28)
        # Gray Center + Gray 6 Surround (Near) (29-36)
        # Gray 12 Surround alone (37)
        # Gray Center + Gray 12 Surround (Middle) (38-45)
        # Gary 18 Surround alone (46)
        # Gray Center + Gray 18 Surround (Far) (47-54)
        # Gray 6 Circle Surround alone (55)
        # Gray Center + Gray 6 Circle Surround (56-63)
        # Gray 12 Small Near Surround alone (64)
        # Gray Center + Gray 12 Small Near Surround (65-72)
        # Gray 12 Small Near Circle Surround alone (73)
        # Gray Center + Gray 12 Small Near Circle Surround (74-81)
        # Color center alone (82-89)
        # Color Center + Gray 6 Surround (Near) (90-97)
        # Color 6 Surround alone (98)
        # Gray Center + Color 6 Surround (Near) (99-106)
        # Gray Center + Gray 6 Surround (PS) (107-114)
        # Gray Center + Gray 6 Circle Surround (PS) (115-122)
        # Gray Center + Gray 12 Small Near Surround (PS) (123-130)
        # Gray Center + Gray 12 Small Near Circle Surround (PS) (131-138)
        
        repetitionIDs = np.arange(10); ### inter-block order    
        if(randomize_stims):
            np.random.shuffle(repetitionIDs);
        rOrder = np.arange(138); ### inner-block order
        StimInfoTable = np.empty((0,14),int);
        """
        col0: Stim condition number
        col1: gray center
        col2: color center
        col3: gray near surr 1
        col4: gray near surr 3        
        col5: gray near surr 6        
        col6: color near surr 6                
        col7: gray middle surr 12                        
        col8: gray far surr 18
        col9: gray near surr circle 6
        col10: gray near surr small 12
        col11: gray near surr small circle 12        
        col12: PS version
        col13: Shuffled order
        """
        for r in np.arange(10): # 10 repetition
            rNow = repetitionIDs[r];
            StimInfoTableNow = np.zeros((138,14),dtype=int);
            StimInfoTableNow[:,0] = rNow*138 + np.arange(1,138+1,1,dtype=int);
            
            # assign gray center
            StimInfoTableNow[1:9,1] = np.arange(1,9,1,dtype=int);           
            StimInfoTableNow[10:18,1] = np.arange(1,9,1,dtype=int);   
            StimInfoTableNow[19:27,1] = np.arange(1,9,1,dtype=int);     
            StimInfoTableNow[28:36,1] = np.arange(1,9,1,dtype=int);      
            StimInfoTableNow[37:45,1] = np.arange(1,9,1,dtype=int);    
            StimInfoTableNow[46:54,1] = np.arange(1,9,1,dtype=int);   
            StimInfoTableNow[55:63,1] = np.arange(1,9,1,dtype=int);               
            StimInfoTableNow[64:72,1] = np.arange(1,9,1,dtype=int);      
            StimInfoTableNow[73:81,1] = np.arange(1,9,1,dtype=int);                  
            StimInfoTableNow[98:106,1] = np.arange(1,9,1,dtype=int);               
            StimInfoTableNow[106:114,1] = np.arange(1,9,1,dtype=int);                                                   
            StimInfoTableNow[114:122,1] = np.arange(1,9,1,dtype=int);                                                               
            StimInfoTableNow[122:130,1] = np.arange(1,9,1,dtype=int);                                                               
            StimInfoTableNow[130:138,1] = np.arange(1,9,1,dtype=int);                                                               

            # assign color center
            StimInfoTableNow[81:89,2] = np.arange(1,9,1,dtype=int);           
            StimInfoTableNow[89:97,2] = np.arange(1,9,1,dtype=int);   
            
            # assign gray near surr1
            StimInfoTableNow[9:18,3] = rNow+1;     
            
            # assign gray near surr3            
            StimInfoTableNow[18:27,4] = rNow+1;     
            
            # assign gray near surr6            
            StimInfoTableNow[27:36,5] = rNow+1;     
            StimInfoTableNow[89:97,5] = rNow+1;             
            StimInfoTableNow[106:114,5] = rNow+1;                 
            
            # assign color near surr6               
            StimInfoTableNow[97:106,6] = rNow+1;                 
            
            # assign gray middle surr12            
            StimInfoTableNow[36:45,7] = rNow+1;     
            
            # assign gray far surr18            
            StimInfoTableNow[45:54,8] = rNow+1;    
            
            # assign gray near surr circle 6            
            StimInfoTableNow[54:63,9] = rNow+1;    
            StimInfoTableNow[114:122,9] = rNow+1;   
             
            # assign gray near surr small 12                        
            StimInfoTableNow[63:72,10] = rNow+1;    
            StimInfoTableNow[122:130,10] = rNow+1;                
            
            # assign gray near surr small circle 12                                    
            StimInfoTableNow[72:81,11] = rNow+1;    
            StimInfoTableNow[130:138,11] = rNow+1;                
            
            # assign PS verson
            StimInfoTableNow[106:138,12] = rNow+1;                            

            # assign random order
            if(randomize_stims):            
                np.random.shuffle(rOrder);
            StimInfoTableNow[:,13] = rOrder;
            StimInfoTableNow = StimInfoTableNow[
                    StimInfoTableNow[:,13].argsort()];
            # Accumulate multiple blocks
            StimInfoTable = np.append(StimInfoTable,
                                      StimInfoTableNow,axis=0);
        self.StimInfoTable = StimInfoTable;
        """
        ##### Loading json.gz file caused a memory error #####
        ### Clutter stimuli from ClutterStim4_0.5_cropped.json.gz file
        import json;
        import gzip;
        FileDirec = '/home/shapelab/.pyperc/Tasks/Taekjun';
        gzipFileName = os.path.join(FileDirec, 'ClutterStim4_0.5_cropped.json.gz');            
        f = gzip.GzipFile(gzipFileName,'r');
        import pdb; pdb.set_trace()                
        stimList = json.loads(f.read().decode('utf-8'));
        f.close();
        print('json.gz File was loaded');
        """
        MatFileBase = '/home/shapelab/.pyperc/Tasks/Taekjun/stimFiles/ClutterStim';
        MatFileName = os.path.join(MatFileBase, 'ClutterStim5_0.5_cropped_uint8.mat');            
        sData = h5py.File(MatFileName,'r');
        print('mat File was loaded');

        # Blank Stim
        s = createBar(10, 10, myFB,myBG, 0, RF_X, RF_Y, myBG);    
        s.depth = 3;
        self.myEmptySprites.append(s)        
        
        # Center Stim
        ShapeID = 16;
        RotationIDs = [1,2,3,4,5,6,7,8];
        myShapeScale = int(RF_dia*0.5)  ## .5 of RF size

        self.sampling = 100
        fg_color = (100,100,100)
        #import pdb; pdb.set_trace();
        salient_color = params['salient_color']
        myFactory = b8StimFactory(myShapeScale*2.0,myShapeScale/2.0)
        for j in range(0,len(RotationIDs)):
            rotation = 45*(RotationIDs[j]-1)
            s = myFactory.getB8Stim(
                                    ShapeID,self.sampling,myFB,fg_color,rotation,
                                    RF_X,RF_Y,myBG,sp_h_offset=0,sp_v_offset=0, sp_scaling=1,depth=1)   
            s2 = myFactory.getB8Stim(
                                     ShapeID,self.sampling,myFB,salient_color,rotation,
                                     RF_X,RF_Y,myBG,sp_h_offset=0,sp_v_offset=0, sp_scaling=1,depth=1)   
            ForAlpha = myFactory.getB8Stim(
                                    ShapeID,self.sampling,myFB,(255,255,255),rotation,
                                    RF_X,RF_Y,(0,0,0),sp_h_offset=0,sp_v_offset=0, sp_scaling=1,depth=1)
            s.alpha[:,:] = ForAlpha.array[:,:,0];
            self.myCenterSprites_Gray.append(s);                    
            s2.alpha[:,:] = ForAlpha.array[:,:,0];
            self.myCenterSprites_Color.append(s2);                    
        print('Center sprites were created');
        
        # Surr1Near
        for i in range(10):
            ref = sData['Surr1Near']['Img'][i,0];
            SpriteSize = np.shape(sData[ref].value)[1];
            
            s = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
            imageNow = np.zeros((SpriteSize,SpriteSize,3))
            imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref].value,(1,2,0))
            
            imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
            s.array[:] = imageNow
            myScale = int(RF_dia*SpriteSize/100)
            s.scale(myScale, myScale)    #Scales to size in pixels		   
            self.mySurr1NearSprites_Gray.append(s)
        print('Surr1Near sprites were created');        
        
        # Surr3Near
        for i in range(10):
            ref = sData['Surr3Near']['Img'][i,0];
            SpriteSize = np.shape(sData[ref].value)[1];
            
            s = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
            imageNow = np.zeros((SpriteSize,SpriteSize,3))
            imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref].value,(1,2,0))
            
            imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
            s.array[:] = imageNow
            myScale = int(RF_dia*SpriteSize/100)
            s.scale(myScale, myScale)    #Scales to size in pixels		   
            self.mySurr3NearSprites_Gray.append(s)
        print('Surr3Near sprites were created');               
        
        # Surr6Near
        for i in range(10):
            ref = sData['Surr6Near']['Img'][i,0];
            SpriteSize = np.shape(sData[ref].value)[1];
            
            s = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
            imageNow = np.zeros((SpriteSize,SpriteSize,3))
            imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref].value,(1,2,0))
            
            imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
            s.array[:] = imageNow
            myScale = int(RF_dia*SpriteSize/100)
            s.scale(myScale, myScale)    #Scales to size in pixels		   
            self.mySurr6NearSprites_Gray.append(s)
            
            ## color
            s2 = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
            imageNow = np.zeros((SpriteSize,SpriteSize,3))
            imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref].value,(1,2,0))
            aa,bb = np.where(imageNow[:,:,0]!=40);
            imageNow[aa,bb,0] = salient_color[0];
            imageNow[aa,bb,1] = salient_color[1];
            imageNow[aa,bb,2] = salient_color[2];
            imageNow= imageNow.tolist();
            s2.array[:] = imageNow;
            s2.scale(myScale, myScale)    #Scales to size in pixels		   
            self.mySurr6NearSprites_Color.append(s2);            
        print('Surr6Near sprites were created');                   

        # SurrMiddle
        for i in range(10):
            ref = sData['SurrMiddle']['Img'][i,0];
            SpriteSize = np.shape(sData[ref].value)[1];
            
            s = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
            imageNow = np.zeros((SpriteSize,SpriteSize,3))
            imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref].value,(1,2,0))
            
            imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
            s.array[:] = imageNow
            myScale = int(RF_dia*SpriteSize/100)
            s.scale(myScale, myScale)    #Scales to size in pixels		   
            self.mySurrMiddleSprites_Gray.append(s)
        print('SurrMiddle sprites were created');                   

        # SurrFar
        for i in range(10):
            ref = sData['SurrFar']['Img'][i,0];
            SpriteSize = np.shape(sData[ref].value)[1];
            
            s = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
            imageNow = np.zeros((SpriteSize,SpriteSize,3))
            imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref].value,(1,2,0))
            
            imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
            s.array[:] = imageNow
            myScale = int(RF_dia*SpriteSize/100)
            s.scale(myScale, myScale)    #Scales to size in pixels		   
            self.mySurrFarSprites_Gray.append(s)
        print('SurrFar sprites were created');       
        
        # Surr6NearCircle
        for i in range(10):
            ref = sData['Surr6NearCircle']['Img'][i,0];
            SpriteSize = np.shape(sData[ref].value)[1];
            
            s = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
            imageNow = np.zeros((SpriteSize,SpriteSize,3))
            imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref].value,(1,2,0))
            
            imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
            s.array[:] = imageNow
            myScale = int(RF_dia*SpriteSize/100)
            s.scale(myScale, myScale)    #Scales to size in pixels		   
            self.mySurr6NearCircleSprites_Gray.append(s)
        print('Surr6NearCircle sprites were created');       
		
        # Surr12NearSmall
        for i in range(10):
            ref = sData['Surr12NearSmall']['Img'][i,0];
            SpriteSize = np.shape(sData[ref].value)[1];
            
            s = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
            imageNow = np.zeros((SpriteSize,SpriteSize,3))
            imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref].value,(1,2,0))
            
            imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
            s.array[:] = imageNow
            myScale = int(RF_dia*SpriteSize/100)
            s.scale(myScale, myScale)    #Scales to size in pixels		   
            self.mySurr12NearSmallSprites_Gray.append(s)
        print('Surr12NearSmall sprites were created');       

        # Surr12NearSmallCircle
        for i in range(10):
            ref = sData['Surr12NearSmallCircle']['Img'][i,0];
            SpriteSize = np.shape(sData[ref].value)[1];
            
            s = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
            imageNow = np.zeros((SpriteSize,SpriteSize,3))
            imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref].value,(1,2,0))
            
            imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
            s.array[:] = imageNow
            myScale = int(RF_dia*SpriteSize/100)
            s.scale(myScale, myScale)    #Scales to size in pixels		   
            self.mySurr12NearSmallCircleSprites_Gray.append(s)
        print('Surr12NearSmallCircle sprites were created');       

        # GrayCenter6SurrPS
        for i in range(10):
            ref = sData['CenterSurr6Near']['shape'][i,0];									
            CS = [None]*8;	            
            for j in range(8):
                ref2 = sData[ref]['PS_Img'][j,0];
                SpriteSize = np.shape(sData[ref2].value)[1];
                CS[j] = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
                imageNow = np.zeros((SpriteSize,SpriteSize,3))
                imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref2].value,(1,2,0))
            
                imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
                CS[j].array[:] = imageNow
                myScale = int(RF_dia*SpriteSize/100)
                CS[j].scale(myScale, myScale)    #Scales to size in pixels	
            self.myGrayCenter6SurrPS_Sprites.append(CS)
            print('GrayCenter6SurrPS - repeat #: '+str(i));                        
        print('GrayCenter6SurrPS sprites were created');       

        # GrayCenter6CircleSurrPS
        for i in range(10):
            ref = sData['CenterSurr6NearCircle']['shape'][i,0];									
            CS = [None]*8;	            
            for j in range(8):
                ref2 = sData[ref]['PS_Img'][j,0];
                SpriteSize = np.shape(sData[ref2].value)[1];
                CS[j] = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
                imageNow = np.zeros((SpriteSize,SpriteSize,3))
                imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref2].value,(1,2,0))
            
                imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
                CS[j].array[:] = imageNow
                myScale = int(RF_dia*SpriteSize/100)
                CS[j].scale(myScale, myScale)    #Scales to size in pixels	
            self.myGrayCenter6CircleSurrPS_Sprites.append(CS)
            print('GrayCenter6CirclePS - repeat #: '+str(i));
        print('GrayCenter6CircleSurrPS sprites were created');       

        # GrayCenter12SmallSurrPS
        for i in range(10):
            ref = sData['CenterSurr12NearSmall']['shape'][i,0];									
            CS = [None]*8;	            
            for j in range(8):
                ref2 = sData[ref]['PS_Img'][j,0];
                SpriteSize = np.shape(sData[ref2].value)[1];
                CS[j] = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
                imageNow = np.zeros((SpriteSize,SpriteSize,3))
                imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref2].value,(1,2,0))
            
                imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
                CS[j].array[:] = imageNow
                myScale = int(RF_dia*SpriteSize/100)
                CS[j].scale(myScale, myScale)    #Scales to size in pixels	
            self.myGrayCenter12SmallSurrPS_Sprites.append(CS)
            print('GrayCenter12SmallSurrPS - repeat #: '+str(i));            
        print('GrayCenter12SmallSurrPS sprites were created');       

        # GrayCenter12SmallCircleSurrPS
        for i in range(10):
            ref = sData['CenterSurr12NearSmallCircle']['shape'][i,0];									
            CS = [None]*8;	            
            for j in range(8):
                ref2 = sData[ref]['PS_Img'][j,0];
                SpriteSize = np.shape(sData[ref2].value)[1];
                CS[j] = Sprite(SpriteSize, SpriteSize, RF_X, RF_Y, fb=myFB, depth=2, on=0, centerorigin=1)
                imageNow = np.zeros((SpriteSize,SpriteSize,3))
                imageNow[0:SpriteSize,0:SpriteSize,0:3] = np.transpose(sData[ref2].value,(1,2,0))
            
                imageNow = imageNow.tolist()   ### numpy.ndarray --> list (May not be needed)
                CS[j].array[:] = imageNow
                myScale = int(RF_dia*SpriteSize/100)
                CS[j].scale(myScale, myScale)    #Scales to size in pixels	
            self.myGrayCenter12SmallCircleSurrPS_Sprites.append(CS)
            print('GrayCenter12SmallCircleSurrPS - repeat #: '+str(i));            
        print('GrayCenter12SmallCircleSurrPS sprites were created');       


        ## these are the stim params that need to be encoded before start of task
        self.myFB = myFB
        self.myBG = myBG

 

    def createParamTable(self,app):
        #create parameter table and window to go along with it
        P = app.getcommon()
        self.myTaskButton = app.taskbutton(text=__name__, check = 1)
        self.myTaskNotebook = DockWindow(title=__name__, checkbutton=self.myTaskButton)
        parfile = "%s.%s" % (app.taskname(), P['subject'])
        # Look for an existing saved parameter file for this task
        if parfile:
                parfile = parfile + '.par'

        # Initialization and default values for the parameters.  Each row is
        # one parameter.  The first value is the name of the parameter, the
        # second is its default value, the third defines the type of
        # the value (more on that later) and the fourth is optional and
        # is a descriptive label that pops up when you hold the mouse over
        # that entry in the table.  There are numerous standard parameter
        # types, the most common are self-explanatory.  is_color needs to be
        # 3 or 4 numbers in tuple format, e.g. (255,1,1) for red; the 4th
        # number is optional and is an alpha value (if left off, assumed
        # to be 255).  (0,0,0) is a special code for transparent or for
        # white noise fill pattern, depending on the task, so use (1,1,1)
        # for black.  is_any just gets passed as a string, this is what
        # to use if you need a list of numbers.  is_iparam can take a
        # variance value as either a percentage or an actual number of
        # units, so you'd have "1000+-10%" or "150+-50".  There are a ton of
        # others defined in ptable.py.  Values of None for default value and
        # type make that row into a heading of sorts that can be helpful for
        # organizing a large number of parameters.

        self.myTaskParams = ParamTable(self.myTaskNotebook, (        
            ("Stim Presentation Params", None, None), 
            ("RF_centerX", "200", is_int,"X coordinate of the receptive field center in pixels"),
            ("RF_centerY", "-150", is_int,"Y coordinate of the receptive field center in pixels"),
            ("FixationShift", "[0,0]", is_any, "Entire screen coordinate shift"),                  
            ("V2orV4", "0", is_int, "Which visual area? - V2: 0, V4: 1"),                                    
            ("randomize_stimuli", 1, is_boolean, "Whether or not to randomize stimuli within repetitions."),
            #("Center_Scale", ".5", is_float, "Stimulus size compared to RF size. Choose in [0.3, 0.5, 0.7]"),
            ("salient_color", "(46, 95, 69)", is_color, "The background color before stimulus presentation"),                        
            ("bg_before", "(40, 40, 40)", is_color, "The background color before stimulus presentation"),            
            ("bg_during", "(40, 40, 40)", is_color, "The background color during stimulus presentation"),
            ("Task Params", None, None),
            ("iti", "2500", is_int, "Inter-trial interval"),
            ("IStime", "300", is_int, "Inter-stimulus interval"),
            ("stimon", "300", is_int, "Stimulus presentation"),
            ("nstim", "4", is_int, "Number of stimuli"),
            ("Fixation Params", None, None, "Fixation Parameters"),
            ("fixcolor1", "(255,255,255)",is_color, 'Color of the fixation dot'),
            ("min_err", "0", is_int),
            ("max_err", "100", is_int),
            ("fixwait", "100", is_int),
            ("Reward Params", None, None),
            ("numdrops", "15", is_int, "Number of juice drops"),
            ("rmult", "1.0", is_float),
            ("Record File Params", None, None, "Params for setting name of record file"),
            ("Use Special Name", "0", is_boolean, "If 1 then the record file name will be AnimalPrefixDate_TaskName_CellGroup_Iteration.rec"),
            ("RFDirectory", "/home/shapelab/recordFiles/", is_any, "Directory to use for Record Files"),               
            ("AnimalPrefix", "m", is_any, "Animal Prefix to use"),
            ("Date","080325", is_any, "Date to use "),
            ("TaskName","isolumcontrol", is_any, "TaskName"),
            ("CellGroup","01", is_int, "# of cell group encountered today"),
            ("Iteration","01", is_int, "# of times this task has been run on this cell group"),
            ("Misc Params", None, None, "Miscelaneous Parameters"),
            ("Recent Buffer Size", "50", is_int, "The number of trials to use to calculate recent performance"),
            ("pause_color", "(20,20,20)", is_color, "The screen will turn this color when the task is paused")
            ), file=parfile)


    def cleanup(self, app):
        #delete parameter table and anything else we created
        self.myTaskParams.save()
        self.myTaskButton.destroy()
        self.myTaskNotebook.destroy()
        del app.globals
        #self.myTaskParams.destroy()
#        if(len(self.mySprites) > 0):
#            for i in arange(1,len(self.mySprites)):
#                self.mySprites[i].__del__()


    def encodeISI(self,app,sIndex):
        myid = self.StimInfoTable[sIndex,0];
	
        app.encode_plex('stimid')
        app.encode_plex(int(myid+app.globals.plexStimIDOffset))

        app.encode('stimid')
        app.encode(int(myid+app.globals.plexStimIDOffset))


    def encodeTaskParameters(self,app):
        #encode task parameters
        params = self.myTaskParams.check()
        app.encode_plex('rfx')
        #import pdb; pdb.set_trace()
        app.encode_plex(params['RF_centerX']+ app.globals.yOffset)
        app.encode_plex('rfy')
        app.encode_plex(params['RF_centerY'] + app.globals.yOffset)
        #app.encode_plex('stimWidth')                         
        #app.encode_plex(params['Stim_Size'] + app.globals.yOffset)
        app.encode_plex('iti')
        app.encode_plex(int(params['V2orV4']))
        app.encode_plex('stim_time')
        app.encode_plex(int(params['stimon']))
        app.encode_plex('isi')
        app.encode_plex(int(params['IStime']))
        app.encode_plex('numstim')
        app.encode_plex(int(params['nstim']))

        app.encode('rfx')
        app.encode(params['RF_centerX']+ app.globals.yOffset)
        app.encode('rfy')
        app.encode(params['RF_centerY'] + app.globals.yOffset)
        #app.encode('stimWidth')                         
        #app.encode(params['Stim_Size'] + app.globals.yOffset)
        app.encode('iti')
        app.encode(int(params['iti']))
        app.encode('stim_time')
        app.encode(int(params['stimon']))
        app.encode('isi')
        app.encode(int(params['IStime']))
        app.encode('numstim')
        app.encode(int(params['nstim']))

     
    def encodeITI(self,app):
        pass


    def runSet(self,app):
        """
        This is what is run when you hit the 'start' button (set as such in
        the 'main' function, defined at the end of this file).
        """

        # tally collects the results of the last N trials and displays a
        # running tally at the bottom of the main pype control window
        app.tally(clear=1)
	
        # This erases any information printed to the console
        #app.console.clear()
	
        # Update the task's representation of all the parameters set in the
        # task parameter table, rig_params and monk_params - always called P
        #app.params = ParamTable(None, (), None)        
        P = self.myTaskParams.check(mergewith=app.getcommon())
        params = self.myTaskParams.check()

        # Save this version (in case you've made changes since the last time
        # the .par file was updated).

        #P.save()
        #params.save()

        self.createStimuli(app)
        print('Done creating Stimuli')
        
        if (self.warnNumStim()):
            if ask("pype", "%d stimuli, proceed?" % self.getNumStim(), ("yes", "no")) == 0:
               pass
            else:
               return

        #Set the record filename if the task wants to:
        rFileName = self.getRecordFileName()
        if (rFileName is not None):
            if (os.path.exists(rFileName)):
               if ask("pype", "overwrite file: %s ?" % (rFileName), ("yes", "no")) == 0:
                  app.record_selectfile(fname=rFileName)
               else:
                  return
            else:
               app.record_selectfile(fname=rFileName)

        app.record_note('task_is', __name__)

        # Basic setup stuff, you shouldn't want to change this.
        app.paused = 0
        app.running = 1
        # Makes a little green light/red light on the main pype window
        app.led(1) 

        # Set various counters and markers in app.globals.  globals is an
        # instance of the Holder class (initialized in function "main,"
        # below), which just lets you store a bunch of variables inside app
        # in a reasonably neat way. 
        # - repnum: number of reps completed, 
        # - ncorrect: number of trials correct
        # - ntrials: number of trials completed
        # - seqcorrect: count of how many trials in a row have been correct
        # - uicount: how many trials have been uninitiated (use with uimax)
        # - number of stimuli that have been seen for complete stim time

        app.globals.repnum = -1
        app.globals.ncorrect = 0
        app.globals.ntrials = 0
        app.globals.seqcorrect = 0
        app.globals.uicount = 0
        app.globals.stimCorrect = 0
        app.globals.yOffset = 600
        #app.globals.yOffset = pype_plex_code_dict('plexYOffset')
        app.globals.plexStimIDOffset = pype_plex_code_dict('plexStimIDOffset')
        app.globals.plexRotOffset = pype_plex_code_dict('plexRotOffset')

        self.encodeTaskParameters(app)

        
        #initialize ITI timer, we are now in the first ITI
        t = Timer()

        # This call intiates the first ITI before the first trial.
        # Calling encode will make a note in the data record
        # with the current timestamp and whatever comment you give it.

        app.encode_plex(START_ITI)
        app.encode(START_ITI)
        self.encodeITI(app)
        # Calls RunTrial, and calculates a running percentage correct.
        try:
           # I added this to keep a running "recent" percentage correct
           # because perfomance often changes during the task.
           pctbuffer = list()
		
           # Call Run trial only if there are still unshown stimuli in
           # the stimorder buffer
           while app.running and (app.globals.stimCorrect < self.getNumStim()):
                #This task implements pause (f5) at the trial level
                was_paused = 0
                while (app.paused):
                      if (was_paused == 0):
                         #app.encode_plex('pause')
                         #app.encode('pause')
                         app.globals.dlist.bg = params['pause_color']
                         # Update the dlist and flip the framebuffer
                         app.globals.dlist.update()
                         app.fb.flip()
                         was_paused = 1
                      app.idlefn()
                if (was_paused): #reset background color
                   #app.encode_plex('unpause')
                   #app.encode('unpause')
                   app.globals.dlist.bg = params['bg_during']
                   # Update the dlist and flip the framebuffer
                   app.globals.dlist.update()
                   app.fb.flip()
                
                P = self.myTaskParams.check(mergewith=app.getcommon())
                params = self.myTaskParams.check()

                try:
                   # RunTrial is a function defined below that runs a
                   # single trial.
                   result,t = self.RunTrial(app,t)
                except UserAbort:
                   # The escape key will abort a trial while it's running.
                   result=None
                   t.reset()
                   pass
               
                # This if statement avoids a divide-by-zero error if the
                # first trial is aborted before ntrials is incremented
                if (app.globals.ntrials > 0 and params['Recent Buffer Size'] > 0):
                   pctbuffer.append(result)
                   # Average the performance over the past X trials.
                   if (app.globals.ntrials < params['Recent Buffer Size']) :
                      recent=100*app.globals.ncorrect/app.globals.ntrials
                   else:
                      lastX = pctbuffer[len(pctbuffer) - params['Recent Buffer Size']::]
                      recent=100*lastX.count(CORRECT_RESPONSE)/len(lastX)
                   stimPerTrial =  float(app.globals.stimCorrect)/ float(app.globals.ntrials)
                else:
                   stimPerTrial = 0.0

                # This call prints the overall and recent perf % to console
                con(app, " %s:%d %d/%d %.0f%% (recent %.0f%%)\n %0.2f stims per trial" % \
                    (now(), app.nreps(),app.globals.ncorrect, app.globals.ntrials, 100.0 * app.globals.ncorrect / app.globals.ntrials, recent, stimPerTrial), 'black')
                   			                                                      
                #update the behavioral history and tally
                if (result is None):
                   app.tally(type=USER_ABORT)
                   app.history(USER_ABORT)
                elif (iscorrect(result)):
                   app.tally(type=CORRECT_RESPONSE)
                   app.history(CORRECT_RESPONSE)
                elif (result == BREAK_FIX):
                   app.tally(type=BREAK_FIX)
                   app.history(BREAK_FIX)
                elif(isui(result)):
                   app.tally(type=UNINITIATED_TRIAL)
                   app.history(UNINITIATED_TRIAL)
                else:
                   app.tally(NO_RESP)
                   app.history(NO_RESP)

        except:
           # If there's an error generated inside the try statement,
           # it drops to here - reporterror tries to exit cleanly instead
           # of crashing the machine.
           reporterror()

        # More housekeeping stuff, also shouldn't change.
        app.repinfo()
        app.running = 0
        app.led(0)
        # standard beep sequence when you hit the "stop" button.
        app.warn_run_stop()
        # marks the data file as done so you know everything is complete.
        app.record_done()

        #Set the record filename back to '' so we don't overwrite things
        rFileName = self.getRecordFileName()
        if (rFileName is not None):
           app.record_selectfile(fname='')

        # This is the end of the RunSet function.
        return 1


    def RunTrial(self,app, t):
        """
        RunTrial is called by RunSet.  It does housekeeping stuff associated
        with recording behavioral data for an individual trial, and calls the
        _RunTrial function which actually does the stimulus presentation and
        task control. 
        """
        # On every trial, we check to see if any parameters have been updated
        # while the last trial was running
        P = self.myTaskParams.check(mergewith=app.getcommon())
        params = self.myTaskParams.check()

        # Note the time that the trial started, again explicitly handled
        # in PypeFile class.
        # Do we need this?
        # Note that the comment above is not accurate.  the time is actually the time that RunTrial is called, the actual trial has not yet started, although the ITI has
        app.record_note('trialtime', (app.globals.ntrials, Timestamp()))

        # This call starts the data record for this trial. The datafile will
        # have a 'start' event encoded with timestamp = 0. Also plexon will 
        # have an event encoded
        app.record_start()
	
        # This function will actually do the task control and stimulus display
        # and return its results back here for housekeeping.
        (result, rt,t) = self._RunTrial(app,t)

        # Stop recording for this trial, reset eye trace and signal trial stop
        # to Plexon.  Encode 'stop' in the datafile, which is the very last
        # thing to get
        app.record_stop()

        self.saveEvents(app);   ### Edited for Neuropixel. Test 2/9/2022, Taekjun        
	
        # VERY IMPORTANT, this call actually writes all of the info collected
        # in this trial into the datafile.  Don't muck with it.
        app.record_write(result, rt, P, taskinfo=None)
	
        # Check to see whether we've exceeded the max allowable uninitiated
        # trials, and if so, pop up a little warning box that will stall the
        # task until the user clicks it.  Note result is one of the variables
        # returned by _RunTrial.
        if result == UNINITIATED_TRIAL:
           app.globals.uicount = app.globals.uicount + 1
           if app.globals.uicount > P['uimax']:
              warn('Warning',
                   'UI Count exceeded @ %s\nPlease intervene.\n' % now(), wait=1)
              app.globals.uicount = 0
        else:
           # Re-set the uicount after every good trial, so uimax can only
           # be exceeded by a number of ui trials in a row.  Otherwise,
           # the count would be cumulative
           app.globals.uicount = 0
	
        # This is the end of RunTrial.  In RunSet, the call to RunTrial expects
        # the 'result' variable to get returned, and this is how we do that:
        return result,t


    def _RunTrial(self,app, t):
        """
        _RunTrial actually does the behavioral control for the task and shows
        whatever stimuli are specified, etc.  This is the meat of the task,
        and this is where you're going to make changes to make the task do
        what you want it to do. 
        """
	
        # # # # # # # # # # # # # # # # # #
        # General setup stuff
        # # # # # # # # # # # # # # # # # #

        # Create a second instances of Timer class (also in pype.py), which counts 
        # milliseconds until it's reset. Can be queried without reset
        t2 = Timer()

        # Get the parameters again
        P = self.myTaskParams.check(mergewith=app.getcommon())
        params = self.myTaskParams.check()

        # Draw a line at the beginning of every trial
        con(app,">---------------------------")
        # You can write anything you want to the console, and in color.
        con(app,"Next trial",'blue')
	
        # Initialize default reaction time in case trial is aborted
        rt = -1
	
        # Check for "testing" mode (rig params table; no eye or bar monitoring)
        TESTING = int(P['testing'])
        if TESTING:
           # put a big red note on the console so I don't forget
           con(app, 'TESTING','red')
	
        # Clear the user display before starting
        app.udpy.display(None)
	
        # The dlist manages what gets shown on the screen, it gets
        # re-initialized every trial.  app.fb is the framebuffer
        app.globals.dlist = DisplayList(app.fb)
        # set the background color - in this case, I've got a color defined
        # for the intertrial interval
        #app.globals.dlist.bg = params['bg_before']
        app.globals.dlist.bg = params['bg_before']
        # Update the dlist and flip the framebuffer
        app.globals.dlist.update()
        app.fb.flip()
        # At this point, screen color is bg_before, and otherwise blank.
	
        # # # # # # # # # # # # # # # # # #
        # Code for making a fixation spot
        # # # # # # # # # # # # # # # # # #
	 
        # Fixation position at P['fix_x'] and P['fix_y'], which are in the
        # monk_params table
        fx, fy = P['fix_x'], P['fix_y']
        fx = fx + eval(params['FixationShift'])[0];
        fy = fy + eval(params['FixationShift'])[1];        

        # I'm not clear on what this does, but it has something to do with
        # aligning the user display, and you need it.
        app.looking_at(fx, fy)

        # Here is some basic fixation point code. Depth sets the layer of sprite
        # Always set fixspot to be layer 0; other stimuli to be layers below
        # i.e. set depth higher for other stimuli Note that fix_size and 
        # fix_ring are from monk_params, but fixspot color has to be 
        # specified by the task.
	
        if P['fix_ring'] > 0:
           # Create the sprite
           spot = Sprite(2*P['fix_ring'], 2*P['fix_ring'],
                         fx, fy, fb=app.fb, depth=0, on=0, centerorigin=1)
           # fill the square with bg color
           spot.fill(params['bg_during'])
           # make a black circle of radius fix_ring at the center of the
           # sprite
           spot.circlefill((1,1,1), r=P['fix_ring'], x=0, y=0)
           # and now for the actual fixation point...
           if P['fix_size'] > 1:
              # make another circle of radius fix_size
              spot.circlefill(params['fixcolor1'], r=P['fix_size'], x=0, y=0)
           else:
              # just color the center pixel - r=1 doesn't work well
              spot[0,0] = params['fixcolor1']
        else:
           # Create a sprite without the surrounding ring
           spot = Sprite(2*P['fix_size'], 2*P['fix_size'],
                         fx, fy, fb=app.fb, depth=0, on=0, centerorigin=1)
           spot.fill(params['bg_during'])
           if P['fix_size'] > 1:
              spot.circlefill(params['fixcolor1'], r=P['fix_size'], x=0, y=0)
           else:
              spot[0,0] = params['fixcolor1']
	
        # This is redundant with on=0 above, but make sure the sprite is off
        spot.off()
        # Add spot to the dlist  
        app.globals.dlist.add(spot)
	
        # # # # # # # # # # # # # # # # # #
        # Code for making the fixation window
        # # # # # # # # # # # # # # # # # #
	
        # This is the virtual boundary that defines a "good" fixation,
        # again only necessary if yours is a fixation task.
	
        # Adjust fixation window size for target eccentricity, since it's
        # harder to fixate on more eccentric points and there's more
        # eye tracker error too.  The min and max error parameters are
        # task-specific.
        #min_e, max_e = params['min_err'], params['max_err']
        #r = ((fx**2)+(fy**2))**0.5
        #z = min_e + (max_e - min_e) * r / ((app.fb.w+app.fb.h)/4.0)
        z = 0
        # Set a parameter value that's the actual window size to use
        # this trial, so it's saved in data file.
        P['_winsize'] = int(round(P['win_size'] + z))
	
        # Create an instance of the FixWin class (defined in pype.py) that
        # will actually keep track of the eye position for you
        fixwin = FixWin(fx, fy, P['_winsize'], app)
        fixwin.draw(color='grey') #draws the fixwin radius on user display

        ##### Now create the visual stimuli
        Cstim_arr = []; # Center
        Sstim_arr = []; # Surround
        ####This is for multiple stimulus presentation; number of stimuli to
        ####be shown in this run is min of P['nstim'] and the number of
        ####stimuli left
        stm_start = app.globals.stimCorrect
        con(app,"%d stimuli presented, %d stimuli remaining" % (stm_start,self.getNumStim()-stm_start),"Black")
        sshow = min(params['nstim'], self.getNumStim()-stm_start)
        Numframes = self.Numframes
        
        #import pdb; pdb.set_trace();
        """
        col0: Stim condition number
        col1: gray center
        col2: color center
        col3: gray near surr 1
        col4: gray near surr 3        
        col5: gray near surr 6        
        col6: color near surr 6                
        col7: gray middle surr 12                        
        col8: gray far surr 18
        col9: gray near surr circle 6
        col10: gray near surr small 12
        col11: gray near surr small circle 12        
        col12: PS version
        col13: Shuffled order
        """
        for i in arange(0,sshow):
            spr = self.getCondNum(stm_start+i)

            # Default: do not show Cstim, Sstim 
            Cstim = self.myEmptySprites[0];
            Sstim = self.myEmptySprites[0];                        

            if spr[12]==0: #non-PS version
                # Center Sprite
                if spr[1]>0:
                    Cstim = self.myCenterSprites_Gray[spr[1]-1];
                elif spr[2]>0:    
                    Cstim = self.myCenterSprites_Color[spr[2]-1];					
                    
                # Surround Sprite
                if spr[3]>0:
                    Sstim = self.mySurr1NearSprites_Gray[spr[3]-1];
                elif spr[4]>0:
                    Sstim = self.mySurr3NearSprites_Gray[spr[4]-1];         
                elif spr[5]>0:
                    Sstim = self.mySurr6NearSprites_Gray[spr[5]-1];         
                elif spr[6]>0:
                    Sstim = self.mySurr6NearSprites_Color[spr[6]-1];         
                elif spr[7]>0:
                    Sstim = self.mySurrMiddleSprites_Gray[spr[7]-1];         
                elif spr[8]>0:
                    Sstim = self.mySurrFarSprites_Gray[spr[8]-1];         
                elif spr[9]>0:
                    Sstim = self.mySurr6NearCircleSprites_Gray[spr[9]-1];         
                elif spr[10]>0:
                    Sstim = self.mySurr12NearSmallSprites_Gray[spr[10]-1];         
                elif spr[11]>0:
                    Sstim = self.mySurr12NearSmallCircleSprites_Gray[spr[11]-1];         
            else:
                # Center Sprite
                if spr[5]>0:
					Cstim = self.myGrayCenter6SurrPS_Sprites[spr[5]-1][spr[1]-1];
                elif spr[9]>0:
					Cstim = self.myGrayCenter6CircleSurrPS_Sprites[spr[9]-1][spr[1]-1];
                elif spr[10]>0:
                    Cstim = self.myGrayCenter12SmallSurrPS_Sprites[spr[10]-1][spr[1]-1];         
                elif spr[11]>0:
                    Cstim = self.myGrayCenter12SmallCircleSurrPS_Sprites[spr[11]-1][spr[1]-1];         


            Cstim_arr.append(Cstim);
            #import pdb; pdb.set_trace();
            Cstim_arr[i].off();
            Cstim.x = self.RF_X + eval(params['FixationShift'])[0];
            Cstim.y = self.RF_Y + eval(params['FixationShift'])[1];                
            
            Sstim_arr.append(Sstim);
            Sstim_arr[i].off();
            Sstim.x = self.RF_X + eval(params['FixationShift'])[0];
            Sstim.y = self.RF_Y + eval(params['FixationShift'])[1];                
                
            app.globals.dlist.update()

        # # # # # # # # # # # # # # # # # #
        # Initiate the trial
        # # # # # # # # # # # # # # # # # #

        # Start monitoring the eye trace.  This encodes an 'eye_start' event
        # in the datafile that will always be equal to the first timestamp
        # at which eyetrace data are collected.
        app.eyetrace(1)

        # set background color to the color defined for during the trial
        app.globals.dlist.bg = params['bg_during']
        app.globals.dlist.update()
	
        # Note that we haven't flipped the framebuffer yet...
	
        # We put the entire trial inside a try statement 
        # with exceptions to stop trial(correct, incorrect, aborted).
        try:
            # The idlefn method just lets the program do background
            # maintenance stuff.  You can give idlefn an argument that
            # specifies a number of milliseconds to wait
            # Timer t was set at the very beginning of the trial,
            # I want to know how long it's been since then.)
            app.idlefn(params['iti']-t.ms())
            app.encode_plex(END_ITI)
            app.encode(END_ITI) 

            #remember we already encoded START_ITI

            # Reset this timer to zero
            t.reset()
		
            # Flip the framebuffer to show the current dlist
            app.fb.flip()

            fixwin.draw(color='red')
            ttt = fixwin.on()
            # Now the background color is bg_during
            # set a little dummy flag to keep track of stuff
            spot_on=0
            # When we get here either the bar has been grabbed or we're not
            # monitoring it.  If the fixation point is not already
            # on, we'll turn it on now.
            if not spot_on:
                spot.on()
                app.globals.dlist.update()
                app.fb.flip()
                app.udpy.display(app.globals.dlist)
                spot_on=1
                #app.reward()                
     
            # Now we're waiting for the subject to acquire the fixation point
            info(app, "waiting fix acquisition")
            app.idlefn()
            t.reset()

            # Again, a dummy flag to help with task control
            go_on = 0
            while not go_on:
                # We are waiting for the eye position to move inside the
                # fixation window.  Whether this is the case is one of
                # the things that the FixWin class keeps track of.
                while not fixwin.inside() and not TESTING:
                    # We use the same abortafter limit again
                    if P['abortafter'] > 0 and t.ms() > P['abortafter']:
                        info(app, "no acquisition")
                        con(app, "no acquisition", 'blue')
                        #app.encode_plex(UNINITIATED_TRIAL)
                        beep(2000,100)
                        result = UNINITIATED_TRIAL
                        raise MonkError
                    app.idlefn()

                # At this point, the fixwin.inside returned 1 (meaning eye
                # is inside window).  Sometimes if the spot has just come
                # on and the subject is in the process of saccading across
                # the screen, the eye position will go through the fixwin.
                # Only count this as acquiring fixation if the eye stays in
                # the window for "fixwait" milliseconds.
                t2.reset()
                # First, assume we will continue if eye stays in window
                go_on = 1
                while t2.ms() < params['fixwait']:
                    if not fixwin.inside() and not TESTING:
                        # If at any time during the fixwait the eye
                        # moves back out of the window, go back to waiting
                        # for the eye to enter the window again.
                        info(app, "passthrough")
                        go_on = 0
                        # This resets fixwin.inside back to zero
                        fixwin.reset()
                        # This exits the innermost while loop, and sends
                        # us back to the top of the "while not go_on"
                        # loop
                        break

            # # # # # # # # # # # # # # # # # #
            # Do real trial stuff
            # # # # # # # # # # # # # # # # # #

            # Now, fixation has been acquired.  We can start timing the
            # length of the fixation.
            t.reset() # Reset the timer to monitor fixation length for each stim
            t2.reset() #We will now use t2 as an absolute timer for this trial
            #app.encode(FIX_ACQUIRED) # Standard event encoding

            app.encode_plex(FIX_ACQUIRED)
            app.encode(FIX_ACQUIRED)
            fixwin.draw(color='blue') # Blue is our "active" fixwin color

            ####This is for multiple stimulus presentation; number of stimuli to
            ####be shown in this run is min of P['nstim'] and the number of
            ####stimuli left
            scount = 0
            while scount < sshow:
                P = self.myTaskParams.check(mergewith=app.getcommon())
                self.encodeISI(app,scount+stm_start)
                while t.ms() < params['IStime']:
                    if fixwin.broke() and not TESTING:
                        #app.encode(FIX_LOST) #standard event code
                        app.encode_plex(FIX_LOST)
                        app.encode(FIX_LOST)
                        info(app, "early break")
                        con(app, "early break at %d, %d ms into ISI of stim %d, fixwin time of %d" % (t2.ms(),t.ms(),scount, fixwin.break_time()), 'red')
                        #app.encode('exact_fix_lost=%d' % fixwin.break_time())
                        result = BREAK_FIX
                        # Auditory feedback
                        app.warn_trial_incorrect(flash=None)
                        # Skip to end of trial
                        raise MonkError
                    # Again, a call to idlefn lets the computer catch up
                    # and monitor for key presses.
                    app.idlefn()
                    
                # now display stimulus 
                # now turn it on put it on the dlist; update and flip buffer
                Cstim_arr[scount].render() ### in order to unrender later                      
                app.globals.dlist.add(Cstim_arr[scount])
                Cstim_arr[scount].on() #turn on first frame
                
                Sstim_arr[scount].render() ### in order to unrender later                      
                app.globals.dlist.add(Sstim_arr[scount])
                Sstim_arr[scount].on() #turn on first frame
                
                foff = 0                  #this is the frame number currently on
         
                self.toggle_photo_diode(app) #note: toggle_photo_diode updates the dlist
                app.encode_plex(SAMPLE_ON)
                app.encode(SAMPLE_ON)

                app.fb.flip()
                
                #app.encode(SAMPLE_ON)
                app.udpy.display(app.globals.dlist)

                # wait for stimulus time
                t.reset()
                fon = 0
                while fon < self.mon_Hz*params['stimon']/1000-1:
                    if fixwin.broke() and not TESTING:
                        app.encode(FIX_LOST) #standard event code
                        app.encode_plex(FIX_LOST)
                        app.encode(FIX_LOST)

                        info(app, "early break")
                        con(app, "early break at %d, %d ms into presentation of stim %d, fixwin time of %d" % (t2.ms(),t.ms(), scount,fixwin.break_time()), 'red')
                        #app.encode('exact_fix_lost=%d' % fixwin.break_time())
                        result = BREAK_FIX
                        app.warn_trial_incorrect(flash=None)
                        #turn off stimuli
                        Cstim_arr[scount].off()
                        Sstim_arr[scount].off()
                        app.fb.flip()
                        # Skip to end of trial
                        raise MonkError
                    fon = fon + 1                    
                    app.fb.flip()                        

                # Again, a call to idlefn lets the computer catch up
                # and monitor for key presses.
                app.idlefn()
                # now turn off stimulus
                Cstim_arr[scount].off();
                Sstim_arr[scount].off();                
                app.globals.dlist.delete(Cstim_arr[scount]);
                app.globals.dlist.delete(Sstim_arr[scount]);                
                self.toggle_photo_diode(app) #note: toggle_photo_diode updates the dlist
                app.fb.flip()
                #app.reward()

                t.reset() # Reset the timer to start ISI timer
                #app.encode(SAMPLE_OFF)
                app.encode_plex(SAMPLE_OFF)
                app.encode(SAMPLE_OFF)
                app.globals.stimCorrect = app.globals.stimCorrect + 1
                scount = scount+1

            ################################
            # If you are here then the trial is correct
            #print "Before raising NoProblem at %d abs time = %d" % (t.ms(), t2.ms())
            raise NoProblem

            # # # # # # # # # # # # # # # # # #
            # Handling exceptions generated in the trial
            # # # # # # # # # # # # # # # # # #
	
        except UserAbort:
            # If you pressed the escape key at any time to abort the trial
            # you will end up here.  No counters are incremented or
            # reset basically because this was not the subject's fault.

            # Turn off the fixation spot and tracker dot
            spot.off()
            #app.encode(FIX_OFF)
            #app.encode_plex(FIX_OFF)

            # Stop monitoring eye position, encode 'eye_stop' in the datafile
            # which will always be the last timestamp at which eyetrace data
            # were collected.
            fixwin.clear()
            app.eyetrace(0)
            #app.encode_plex(EYE_STOP)

            # Re-set the background for the intertrial interval
            app.globals.dlist.bg = params['bg_before']
            self.turn_off_photo_diode(app)
            app.fb.flip()

            result = USER_ABORT
            app.encode_plex(result)
            app.encode(result)
            t.reset()
            app.encode_plex(START_ITI)
            app.encode(START_ITI)

            con(app, "Aborted.", 'red')
            return (result, rt, t)
            
        except MonkError:
            # Any of the MonkError exceptions will land you here.  The
            # trial counter is incremented and the seqcorrect counter
            # is reset.

            # Turn off the fixation spot and tracker dot
            spot.off()
            #app.encode(FIX_OFF)
            #app.encode_plex(FIX_OFF)

            # Stop monitoring eye position, encode 'eye_stop' in the datafile
            # which will always be the last timestamp at which eyetrace data
            # were collected.
            fixwin.clear()
            app.eyetrace(0)
            #app.encode_plex(EYE_STOP)

            # Re-set the background for the intertrial interval
            app.globals.dlist.bg = params['bg_before']
            app.globals.dlist.update()
            self.turn_off_photo_diode(app)
            app.fb.flip()

            app.encode_plex(result)
            app.encode(result)
            t.reset()
            app.encode_plex(START_ITI)
            app.encode(START_ITI)

            app.globals.ntrials = app.globals.ntrials + 1
            app.globals.seqcorrect = 0
            return (result, rt, t)
		
        except NoProblem:
            # Having an exception for a correct trial is handy because
            # there are a number of ways of getting the trial correct
            # depending on whether we're monitoring the eye position or
            # touch bar or dot dimming, and we can put all the reward
            # code in one place.

            # Turn off the fixation spot and tracker dot
            spot.off()
            #app.encode(FIX_OFF)
            #app.encode_plex(FIX_OFF)

            # Stop monitoring eye position, encode 'eye_stop' in the datafile
            # which will always be the last timestamp at which eyetrace data
            # were collected.
            fixwin.clear()
            app.eyetrace(0)
            #app.encode_plex(EYE_STOP)

            # Re-set the background for the intertrial interval
            app.globals.dlist.bg = params['bg_before']
            app.globals.dlist.update()
            self.turn_off_photo_diode(app)
            app.fb.flip()

            result = CORRECT_RESPONSE
            app.encode_plex(CORRECT_RESPONSE)
            app.encode(CORRECT_RESPONSE)

            # Without arguments this call dispenses a reward of size
            # 'dropsize' with a variance of 'dropvar' (both specified
            # in monk_params). The multiplier argument multiplies the
            # "standard" reward by whatever value is passed in.
            clk_num = params['numdrops']
            while clk_num > 0:
                app.reward(multiplier=params['rmult'])
                app.idlefn(50)#time between juice drops
                clk_num = clk_num-1

            # Reset the timer and Start the next ITI as soon as the reward for this trial has been dispensed.

            app.warn_trial_correct() #Standard "correct" beep
            #app.encode_plex(REWARD)

            t.reset()
            app.encode_plex(START_ITI)
            app.encode(START_ITI)

            # Increment the sequence correct counter
            app.globals.seqcorrect=app.globals.seqcorrect + 1
            # Reporting stuff, variables returned to RunTrial
            app.globals.ncorrect = app.globals.ncorrect + 1
            app.globals.ntrials = app.globals.ntrials + 1

            return (result, rt, t)


    def toggle_photo_diode(self,app):
        app.globals.dlist.update()
        app.fb.sync_toggle()

    def turn_off_photo_diode(self,app):
        app.fb.sync(0)

    def warnNumStim(self):
        return 0

    def getCondNum(self, index):
        return self.StimInfoTable[index,:]

    def getNumStim(self):
        return self.numStim

    def getRecordFileName(self): #gets the record file for this task 
        params = self.myTaskParams.check()
        if(params['Use Special Name']):
            filename = "%s%s%s_%s_%02d_%02d.rec" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
        else:
            filename = None
        filename = None;  ## added to avoid conflict with Neuropixel. 02/09/2022. Taekjun                
        return filename

    def saveEvents(self,app):# Tomo Neuropixles Mar 8 2019 # edited for Neuropixel 02/09/2022 Taekjun

        if self.taskparam==0:
            from datetime import datetime; 
            params = self.myTaskParams.check()        
            tNow = datetime.now().strftime("_%y%m%d_%H%M%S"); 
            event_filename = "%s%s%s_%s.dat" % (params['RFDirectory'],params['AnimalPrefix'],tNow,params['TaskName'])
            self.event_filename = event_filename; 

            fid = open(event_filename,'w');
            ## make header: TaskParameters, and first start ITI
            Header = ['RF_x',int(params['RF_centerX']),'RF_y',int(params['RF_centerY']),
                      'num_cond',138,'V2orV4',int(params['V2orV4']),
                      'stimon',int(params['stimon']),'isi',int(params['IStime']),
                      'start_iti'];
            fid.write(str(Header)+"\n");
            fid.close();
            self.taskparam = 1; 

        data=app.record_buffer #Tomo Neuropixels
        EventNow = [];
        
        # need to remove START, STOP, EYE_STOP, EYE_START which are not sent to plexon
        for item in data:
            if item[1] not in ['start','stop','eye_stop','eye_start']:
                EventNow.append(item[1]);

        #print app.record_buffer
        app.record_buffer=[]
        event_filename = self.event_filename; 

        fid=open(event_filename,'a');
        fid.write(str(EventNow)+"\n");
        fid.close()	

