# -*- coding: utf-8 -*-
import datetime as dt
import random
import SimulateHouse
"""
Created on Wed Nov 11 11:44:37 2020
This file is for:
- generating the historical(fake) resource(electricity and water) usage data (random number gen and math)
    - Create a method which generates an event schedule for weekdays and weekends based on rng (Full package)
    OR
    - Just randomly generate 2 numbers for resource usages and use that as the "historical data" (Bare bones)
- generating the projected (realer than fake) resource usage data.
    - Possibly use machine learning on the dataset we've created? (insane effort but accurate)
    - Throw the averages of the historical data and real data together? (Low effort but efficient)

Something important
The constants here are placeholders for now
For now, we work on just making it logical.
We may consider using a striaght modifier
to randomize the calculations.
@author: Christopher Wilson
"""


def randomMorningDuration():  # generates a random number of seconds up to a max of 2.5 hours
    return random.uniform(1, 60) * random.uniform(1, 60) * random.uniform(0, 2.5)


def randomAfternoonDuration():  # generates a random number of seconds up to a max of 6.5 hours
    return random.uniform(1, 60) * random.uniform(1, 60) * random.uniform(0, 6.5)


def randomWeekendDuration():  # Modifier, until I can figure this other thing out.
    return random.uniform(.5, 1.5)


def generateUseList(applianceList):
    eventList = []
    for i in range(len(applianceList)):  # 12 distinct appliances. (except fridge, which stays on permanently)
        eventList.append(random.randint(0, 1))  # 1 means on, 0 means off.

    return eventList


def WaterHeater(watergallons, percentHot):  # This thing takes so many watts
    hotWater = watergallons * percentHot
    wattage = Constants.Water_Heater_Wattage * (hotWater * 4 / 60)
    return wattage


def randomMorningRoutine(applianceList):
    wattage = 0
    gallons = 0
    usageList = generateUseList(applianceList)
    gallons += Constants.Bath_Water_Usage + Constants.Shower_Water_Usage
    wattage += WaterHeater(gallons, Constants.Shower_Hot_Water_Percent)
    for i in range(len(usageList)):
        if usageList[i] == 1:
            activeApp = applianceList[i]
            wattage += activeApp.watts * randomMorningDuration() / 3600
            if (activeApp.gallonsPerUse != None):
                gallons += activeApp.gallonsPerUse

    return (wattage, gallons)


def randomAfternoonRoutine(applianceList):
    wattage = 0
    gallons = 0
    usageList = generateUseList(applianceList)
    gallons += Constants.Bath_Water_Usage + Constants.Shower_Water_Usage
    wattage += WaterHeater(gallons, Constants.Shower_Hot_Water_Percent)
    for i in range(len(usageList)):
        if usageList[i] == 1:
            activeApp = applianceList[i]
            wattage += activeApp.watts * randomAfternoonDuration() / 3600
            if (activeApp.gallonsPerUse != None):
                gallons += activeApp.gallonsPerUse
    return (wattage, gallons)


def randomWeekendRoutine(applianceList):
    wattage = 0
    gallons = 0
    usageList = generateUseList(applianceList)
    gallons += (Constants.Bath_Water_Usage * 3) + (Constants.Shower_Water_Usage * 3)
    wattage += WaterHeater(gallons, Constants.Shower_Hot_Water_Percent)
    for i in range(len(usageList)):
        if usageList[i] == 1:
            activeApp = applianceList[i]
            wattage += activeApp.watts * randomWeekendDuration()
            if activeApp.gallonsPerUse is not None:
                gallons += activeApp.gallonsPerUse
    return (wattage, gallons)


def generateData(prevDate, currDate, applianceList):  # return date list, water list, khW list
    numOfDays = (currDate.date() - prevDate.date()).days
    weekday = prevDate.weekday()
    dateList = []
    gallonList = []
    wattList = []
    wattBills = []
    waterBills = []
    OB1 = applianceList[0].getObserver()
    for i in range(numOfDays):
        wattage = 0
        gallons = 0
        wattage += Constants.Refrigerator_Wattage * 24  # fridges are on 24/7
        if weekday > 7:
            weekday = 0
        if weekday < 5:
            wattHold, gallonHold = randomMorningRoutine(applianceList)
            wattage += wattHold
            gallons += gallonHold

            wattHold, gallonHold = randomAfternoonRoutine(applianceList)
            wattage += wattHold
            gallons += gallonHold

        else:
            wattHold, gallonHold = randomWeekendRoutine(applianceList)
            wattage += wattHold
            gallons += gallonHold

        dateList.append(prevDate + dt.timedelta(days=i))
        wattList.append(wattage / 1000)
        gallonList.append(gallons)
        OB1.update(wattage / 1000, gallons)
        wattBills.append(OB1.reportBill()[0])  # REPORT FINAL BILL
        waterBills.append(OB1.reportBill()[1])
        OB1.reset()
        print()
        weekday += 1

    return dateList, wattList, gallonList, wattBills, waterBills


# --------------------------------------------------------
import Constants

HOUSE = SimulateHouse.FullApplianceList

today = dt.datetime.now()
prevDate = today - dt.timedelta(days=64)
numOfDays = (today.date() - prevDate.date()).days
DATES, WATTS, GALLONS, WATTBILLS, WATERBILLS = generateData(prevDate, today, HOUSE)

# for i in range(numOfDays):
# print("Date: {0}\t khws: {1}\t Gallons: {2}\t WATTBILL: ${3}\t GALLONBILL: ${4}".format(DATES[i], WATTS[i], GALLONS[i],WATTBILLS[i], WATERBILLS[i]))
# access_db.write_to_db("usages", (DATES[i], str(round(WATTS[i], 2)), GALLONS[i], WATTBILLS[i],WATERBILLS[i]), None)
