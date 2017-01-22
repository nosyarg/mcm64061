from random import *

class car(object):
    namecounter = 0
    def __init__(self, whchln):
        self.size = 5
        self.name = "XX-" + str(car.namecounter)
        self.speed = 0
        self.pos = 0
        car.namecounter+=1
        self.whchln = whchln
        car.setinitcspeed(self)   
 
    def __str__(self):
        return self.name

    def setinitcspeed(self):
        if self.whchln == 0:
            self.speed = 1 #60
        elif self.whchln == 1:
            self.speed = 1 #40

    '''
    def setcarspeed(whchln, crrntspd):
        if whchln == 0:
            speed = 60
        elif whchln == 1:
            speed = 40 
    '''

class lane(object):
    def __init__(self, i, maxspeed, minspeed):
        self.lindex = i
        self.maxspeed = maxspeed 
        self.minspeed = minspeed
        self.lnarry = [None]*10

    def lookleft(self, cposition):
        mergelane = self.lindex - 1
        spcounter = 0

        if mergelane < 0:
            return spcounter
        else:
            print(type(newhghwy.lnlst[mergelane].lnarry[cposition]))
            while((type(newhghwy.lnlst[mergelane].lnarry[cposition]) is type(None)) & (cposition >= 0)):
            #if(type(newhghwy.lnlst[mergelane].lnarry[cposition]) is None):
                spcounter += 1
                cposition -= 1
            return spcounter

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
        if cobj.speed > ((firstahead.pos-(firstahead.size)) - cobj.pos):
            cobj.speed = firstahead.speed
        #step 4 randomly reduce speed
        if 0.05 > random():
            cobj.speed -= 1

    def move_carinlane(self):
        # for the last car in the lane to the first car
        # move the car

        for i in reversed(range(len(self.lnarry))):
            if(type(self.lnarry[i]) is car):
                #look left and calculate number of spaces to merge
                x = lane.lookleft(self, i)
                print("spcounter " + str(x), "laneindex" + str(self.lindex))
                
                #if canmerge returns True, then run merge acceleration function and switch lanes
                #if you canmerge returns False, then run nagel model 

                self.nagelmodel(self.lnarry[i])        
                
                #car.setcarspeed(self.lnarry[i].whchln, self.lnarry[i].speed) 

                #regular movement
                if(i + self.lnarry[i].speed < len(self.lnarry)):
                    #update position attribute of car object
                    self.lnarry[i].pos = i + self.lnarry[i].speed
                    #update location of car in the lane
                    self.lnarry[i + self.lnarry[i].speed] = self.lnarry[i]
                    #car previous location is now empty
                    self.lnarry[i] = None
                else:
                    self.lnarry[i] = None

    def enter_carinlane(self): 
        if((self.lnarry[0] is  None) & (0.2 > random())): 
            self.lnarry[0] = car(self.lindex)
            
        print(self.lnarry)
        # check if the spots equal to size + 1 are empty in the lane
        # if the space is empty then create a car and speed equals 5
        # car occupies that many slots
      
class highway(object):
    def __init__(self):
        self.lnlst = []
        self.maxlanes = 2
        maxspeed = [80, 60]
        minspeed = [60, 40]
        for i in range(self.maxlanes):
            self.lnlst.append(lane(i, maxspeed[i], minspeed[i]))

newhghwy = highway()

def entercar(n_newhghwy):
    for laney in newhghwy.lnlst:
        laney.move_carinlane()
        laney.enter_carinlane()
     
    #for each lane
        #move the car in the lane 
        #if lane has a spot then populate car
        #else car waits for empty space

for i in range(3):
    entercar(newhghwy)
