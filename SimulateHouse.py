# -*- coding: utf-8 -*-
import Constants
from datetime import datetime
import random
import time
import access_db
"""
Created on Fri Nov  6 15:51:02 2020

@author: Christopher Wilson
This will generally be a testing grounds for the data generation
and calculations for the graphs for the resource usage screen
I'm thinking about relying on the Observer Design Pattern
which will collect info on appliances on update/end of day/etc
However we're calculating the data. 

Docs:
- Remembering How To Use Python at all
    https://www.geeksforgeeks.org/default-arguments-in-python/
- Date and Times:
    https://docs.python.org/3/library/datetime.html
    https://www.programiz.com/python-programming/datetime/current-time
    https://www.youtube.com/watch?v=haC7eG-u2yQ
"""
class appliance:
    """
    A generalized format which all the appliances fit under
    We have an appliance name, watts, gallons of water used per load
    The amount of times it's used per week
    and the max amount of times it's used per week
    If it's the case where one of these attributes is unused, we initialize it with -1
    """
    def __init__(self,name = "N/A", watts = None, gallonsPerUse = None, timesUsed= None, maxUsage = None ):
        self.name = name
        self.watts = watts
        self.gallonsPerUse = gallonsPerUse
        self.timesUsed = timesUsed
        self.maxUsage = maxUsage
        self.activationTime = 0 #Use the datetime object
        self.deactivationTime = 0 #Use the datetime object
        self.status = False
        self.type = False
        self.observer = None
    
    def acceptObserver(self, newObserver):
        self.observer = newObserver
    
    def removeObserver(self):
        self.observer = None
    
    def getObserver(self):
        return self.observer
        
    def activate(self):
        self.activationTime = datetime.now() #Pretty much just filing the time start
        self.status = True
        #Throw activation time to db.
        
    def deactivate(self):
        #takes the deactivation time, then calculates how long the appliance was on
        self.deactivationTime = datetime.now()
        self.status = False
        thisObserver = self.getObserver()
        duration = self.deactivationTime - self.activationTime
        seconds = duration.total_seconds()
        wattsUsed = (seconds/3600) * self.watts
        waterUsed = self.gallonsPerUse
        # print('The amount of watts in this example  is: {0}'.format(wattsUsed))
        thisObserver.update(wattsUsed, waterUsed)

    def deactivate(self, seconds=0):
            self.status = False
            thisObserver = self.getObserver()
            wattsUsed = (seconds / 3600) * self.watts
            waterUsed = self.gallonsPerUse
            thisObserver.update(wattsUsed, waterUsed)

class Observer:
    """
    Keeps track of housewide energy usage and holds onto it
    until we find the need to update the energy log in the database.
    Though it's intended to grab every appliance in the house at some time (day's end?)
    It might be better to have it grab usage directly after it deactivates
    """
    def __init__(self):
        self.gallonUsage = 0
        self.wattUsage = 0
        
    def update(self, watts, gallons):
        self.wattUsage += watts
        self.gallonUsage += gallons
        # print("Update achieved")
    
    def reportBill(self):
        electricalCost = self.wattUsage * Constants.electric_cost_perkHw
        gallonCost = self.gallonUsage * Constants.water_cost_per_gallon/748
        #print('The electricity bill is: ${}'.format(electricalCost))
        #print('The water bill is: ${}'.format(gallonCost))
        return (electricalCost, gallonCost)
        #send sum to the appropriate day in the database
        #plot it on a graph

    def reset(self):
        self.gallonUsage = 0
        self.wattUsage = 0


class Openings:
    def __init__(self, name = "Opening", type = "N/A"):
        self.name = name
        if type == "W": #Give me a W or a D.
            self.Tick = Constants.WindowTempChange
            self.type = "W"
        else:
            self.Tick = Constants.DoorTempChange
            self.type = "D"
        self.status = False
    def stateChange(self):
        if self.status is False:
            self.status = True
        else:
            self.status = False

    def TickG(self):
        return self.Tick

class HouseSim:
    def __init__(self, OpeningList = []):
        self.temperature = random.randint(68,80)
        self.OpeningList = OpeningList

    def updateTemp(self, setPoint = 75): #get set point somehow
        OutsideTemp = 200 #Get outisde temperature
        for i in range(len(self.OpeningList)):
            num = self.OpeningList[i].TickG()
            diff = self.temperature - OutsideTemp
            diff2 = OutsideTemp - self.temperature
            if OutsideTemp < self.temperature:
                self.temperature -= num * (diff/10)
            else:
                self.temperature += num * (diff2/10)
            print(self.temperature)
            return self.temperature


OB1 = Observer()

L1 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L2 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L3 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L4 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L5 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L6 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L7 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L8 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None) #13 Lights
L9 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L10 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L11 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L12 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
L13 = appliance(name = "Lightbulbs", watts = 60, gallonsPerUse = None, timesUsed= None, maxUsage = None)
a1 = appliance(name = "Bathfan", watts = 30, gallonsPerUse = None, timesUsed= None, maxUsage = None) #2 Bathfans
a2 = appliance(name = "Bathfan", watts = 30, gallonsPerUse = None, timesUsed= None, maxUsage = None) #2 Bathfans1
a3 = appliance(name = "Bedroom TV", watts = 100, gallonsPerUse = None, timesUsed= None, maxUsage = None) #1 Bedroom TVs
a4 = appliance(name = "Livingroom TV", watts = 636, gallonsPerUse = None, timesUsed= None, maxUsage = None) #1
a5 = appliance(name = "Microwave", watts = 1100, gallonsPerUse = None, timesUsed= None, maxUsage = None)
a6 = appliance(name = "Oven", watts = 4000, gallonsPerUse = None, timesUsed= None, maxUsage = None)
a7 = appliance(name = "Stove", watts = 3500, gallonsPerUse = None, timesUsed= None, maxUsage = None)
a8 = appliance(name = "Dishwasher", watts = 1800, gallonsPerUse = 6, timesUsed= None, maxUsage = 4)
a9 = appliance(name = "Washing Machine", watts = 500, gallonsPerUse = 20, timesUsed= None, maxUsage = 4)
a10 = appliance(name = "Drying Machine", watts = 3000, gallonsPerUse = None, timesUsed= None, maxUsage = 4)
a11 = appliance(name = "HVAC", watts = 4500, gallonsPerUse = None, timesUsed= None, maxUsage = None)
FullApplianceList = [L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12,L13,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11]

for i in FullApplianceList:
    i.acceptObserver(OB1)



Door1 = Openings(name= "Front Door", type = "D")
Door2 = Openings(name= "Back Door", type = "D")
Door3 = Openings(name= "Garage Door", type = "D")
Win1 = Openings(name= "Master Bedroom Window", type = "W")
Win2 = Openings(name= "Master Bedroom Window2", type = "W")
Win3 = Openings(name= "Bedroom1 Window", type = "W")
Win4 = Openings(name= "Bedroom1 Window2", type = "W")
Win5 = Openings(name= "Bedroom2 Window", type = "W")
Win6 = Openings(name= "Bedroom2 Window2", type = "W")
Win7 = Openings(name= "Master Bath Window", type = "W")
Win8 = Openings(name= "Bath Window2", type = "W")
Win9 = Openings(name= "Kitchen Window", type = "W")
Win10 = Openings(name= "Kitchen Window2", type = "W")
Win11= Openings(name= "Living Room Window", type = "W")
Win12 = Openings(name= "Living Room Window2", type = "W")
Win13 = Openings(name= "Living Room Window3", type = "W")
FL = [Door1, Door2,Door3,Win1,Win2,Win3,Win4,Win5,Win6,Win7,Win8,Win9,Win10,Win11,Win12,Win13]

FinalList = FullApplianceList + FL
HOUSE = HouseSim(OpeningList=FL)
#HOUS.updateTemp()
# i = 0
# for i in range(len(FinalList)):
#     A = FinalList[i]
#     access_db.write_to_db("sensors", (i, 1, A.name, A.status), None)


# access_db.write_to_db("usages", (DATES[i], str(round(WATTS[i], 2)), GALLONS[i], WATTBILLS[i],WATERBILLS[i]), None)
