from random import *
from pdb import *
def movecar(cartomove,targetlane):
        newhghwy.lnlst[cartomove.whchln].lnarry[cartomove.pos] = None
        targetlane.lnarry[cartomove.pos] = cartomove
        cartomove.whchln = targetlane.lindex

class car(object):
    namecounter = 0
    def __init__(self, whchln):
        self.size = 5
        self.name = "XX-" + str(car.namecounter)
        self.speed = 1
        self.pos = 0
        car.namecounter+=1
        self.whchln = whchln
        car.setinitcspeed(self)   

    def __str__(self):
        return self.name
   
    def __repr__(self):
        return self.name

    def setinitcspeed(self):
        if self.whchln == 0:
            self.speed = 1 #60
        elif self.whchln == 1:
            self.speed = 1 #40


class lane(object):
    def __init__(self, i, maxspeed, minspeed):
        self.lindex = i
        self.maxspeed = maxspeed 
        self.minspeed = minspeed
        self.lnarry = [None]*10

    def nagelmodel(self, cobj):
        #step 1 increment velocity by 1m/s^2 (acceleration)
        cobj.speed += 1
        #step 2 variation of canmerge(forward) to see how many spots are ahead
        firstahead = 0    
        for i in range(cobj.pos,len(self.lnarry)-1):
            if(not (type(self.lnarry[i]) is type(None))):
                firstahead = self.lnarry[i]
            else:
                break
        #step 3 continue moving or adopt behavior of car in front
        if(type(firstahead) is type(None)):
            if cobj.speed > ((firstahead.pos-(firstahead.size)) - cobj.pos):
                cobj.speed = firstahead.speed
        #step 4 randomly reduce speed
        if 0.05 > random():
            cobj.speed -= 1


    def lookleft(self, cposition):
        mergelane = self.lindex - 1
        spcounter = 0

        if mergelane < 0:
            return spcounter
        else:
            while((type(newhghwy.lnlst[mergelane].lnarry[cposition]) is type(None)) & (cposition >= 0)):
            #if(type(newhghwy.lnlst[mergelane].lnarry[cposition]) is None):
                spcounter += 1
                cposition -= 1
            return spcounter 
    def canmerge(self,cartomerge):
        firstahead = 0
        lastbehind = 0
        for i in range(cartomerge.pos,len(self.lnarry)-1):
                if(not (type(self.lnarry[i]) is type(None))):
                        firstahead = self.lnarry[i]
                        break
        for i in reversed(range(0,max(cartomerge.pos-cartomerge.size,0))):
                if(not (type(self.lnarry[i]) is type(None))):
                        lastbehind = self.lnarry[i]
                        break
        thisafterfront = cartomerge.pos + cartomerge.speed
        thisafterback = cartomerge.pos - cartomerge.size + cartomerge.speed
        if(type(firstahead) == type(cartomerge)):
                frontafterfront = firstahead.pos + firstahead.speed
                frontafterback = max(firstahead.pos - firstahead.size + firstahead.speed,0)
                thishitfront = thisafterfront > frontafterback & thisafterfront < frontafterfront
                fronthitthis = thisafterback > frontafterback & thisafterback < frontafterfront
                thisabsorbfront = frontafterfront > thisafterback & frontafterfront < thisafterfront
                toofarforward = thishitfront | fronthitthis | thisabsorbfront
        else:
                toofarforward = 0
        
        if(type(lastbehind) == type(cartomerge)):
                backafterfront = lastbehind.pos + lastbehind.speed
                backafterback = lastbehind.pos - lastbehind.size + lastbehind.speed
                thishitback = thisafterfront > backafterback & thisafterfront < backafterfront
                backhitthis = thisafterback > backafterback & thisafterback < backafterfront
                thisabsorbback = backafterfront > thisafterback & backafterfront < thisafterfront
                toofarback = thishitback | backhitthis | thisabsorbback
        else:
                toofarback = 0

        return (not toofarforward) & (not toofarback)
        
    def handlemerges(self):
        for i in reversed(range(len(self.lnarry))):
            if(type(self.lnarry[i]) is car):
                self.nagelmodel(self.lnarry[i])
                
                bouttamerge = 0
                if(self.lnarry[i].whchln):
                        bouttamerge = (newhghwy.lnlst[self.lindex-1].canmerge(self.lnarry[i]))
                
                if(bouttamerge):
                        movecar(self.lnarry[i],newhghwy.lnlst[self.lindex-1])

    def move_carinlane(self):
        # for the last car in the lane to the first car
        # move the car
        
        for i in reversed(range(len(self.lnarry))):
        
            if(type(self.lnarry[i]) is car):
                #regular movement
                                
                if(i + self.lnarry[i].speed < len(self.lnarry)):
                        #update position attribute of car object
                        self.lnarry[i].pos = i + self.lnarry[i].speed
                        #update location of car in the lane
                        self.lnarry[i + self.lnarry[i].speed] = self.lnarry[i]
                        #car previous location is now empty
                        self.lnarry[i] = None

    def enter_carinlane(self): 
        if((self.lnarry[0] is  None) & (0.2 > random())): 
            self.lnarry[0] = car(self.lindex)
            
        # check if the spots equal to size + 1 are empty in the lane
        # if the space is empty then create a car and speed equals 5
        # car occupies that many slots
      
class highway(object):
    def __init__(self):
        self.lnlst = []
        self.maxlanes = 3
        maxspeed = [80, 60, 40]
        minspeed = [60, 40, 20]
        for i in range(self.maxlanes):
            self.lnlst.append(lane(i, maxspeed[i], minspeed[i]))

newhghwy = highway()

def entercar(n_newhghwy):
    for laney in newhghwy.lnlst:
        laney.handlemerges()
        laney.move_carinlane()
        laney.enter_carinlane()
    for laney in newhghwy.lnlst:
        print(laney.lnarry)
    #for each lane
        #move the car in the lane 
        #if lane has a spot then populate car
        #else car waits for empty space

for i in range(30):
    entercar(newhghwy)
    print(
    '''
    THIS IS THE END OF A SECOND

    THIS SHOULD BE REALLY OBVIOUS

    NOTICE THIS
    ''')
