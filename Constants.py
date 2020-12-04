# -*- coding: utf-8 -*-
#from SimulateHouse import Observer, appliance, Openings
"""
Created on Fri Nov  6 14:29:15 2020

@author: Christopher Wilson
"""
#Conversions
watt = 1 # .0001 khw
kw = 1000 #1k watts
cubic_feet = 100 # or 748 gallons of water
gallons = 748 # or 100 cubic feet of water

#Costs
electric_cost_perkHw = .12   #dollars
water_cost_per_gallon = 2.52 #dollars

#Electric Items Watt Usage,
#Consider listing in terms of kw?
Lightbulb_Wattage = 60 #60 
Bath_Fan_Wattage = 30 #30
Refrigerator_Wattage = 150 #150 
Microwave_Wattage = 1100 #1100
Water_Heater_Wattage = 4500 #4500
Stove_Wattage = 3500 #3500
Oven_Wattage = 4000 
Living_Room_TV_Wattage = 636 #636
Bedroom_TV_Wattage = 100 #100
Dishwasher_Wattage = 1800 #1800
Washing_Machine_Wattage = 500 #500
Drying_Machine_Wattage = 3000 #3000
HVAC_Wattage = 3500 #3500

#Water Item Gallon Usage 
Shower_Water_Usage = 25
Bath_Water_Usage = 30
Dishwasher_Water_Usage = 6
Washing_Machine_Water_Usage = 20

#Max Loads
Dishwasher_Max_Usage = 4
Washing_Machine_Max_Usage = 4
Drying_Machine_Max_Usage = 4

#Percentages
Washing_Machine_Hot_Water_Percent = .85
Shower_Hot_Water_Percent = .65
#Quick Temperature Calculations
ClosedHouseTempChange = 1/108000  # degree change per second
WindowTempChange = 1/1800     # degree change per second
DoorTempChange = 1/900    # degree change per second

