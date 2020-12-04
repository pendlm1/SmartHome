from flask import Flask, render_template, url_for, session, redirect, request
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField, RadioField,
SelectField, FloatField, TextField, TextAreaField, IntegerField)
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import weather_data
import usage_data
from datetime import *
import SimulateHouse
import access_db



def toggle(a,b):
    a =request.form.get(b)
    if a == None:
        a = session[b]
    else:
        session[b] = a
    return a


def update_sensors():
    import psycopg2
    conn = psycopg2.connect(
        host="164.111.161.243",
        database="Team5DB",
        user="Team5",
        password="5Team5")

    cur = conn.cursor()
    for key in session:
        value = session[key]
        if value == "ON" or value == "OPEN":
            value = "true"
        elif value == "OFF" or value == "CLOSED":
            value = "false"

        command = ("UPDATE sensors SET status = {} WHERE location = '{}';".format(value, str(key)))
        cur.execute(command)
    for key in session:
        if session[key] == "ON":
            print(key)

#AWS requires a variable called application
application = app = Flask(__name__)
app.secret_key = "mykey"

@app.route('/')
def index():
    session["Master_Light"]= "OFF"
    session["Master_Lamp1"]= "OFF"
    session["Master_Lamp2"]= "OFF"
    session["Master_TV"]= "OFF"
    session["Master_Window1"]= "CLOSED"
    session["Master_Window2"]= "CLOSED"
    session["Master_Bath_Light"]= "OFF"
    session["Master_Bath_Water"]= "OFF"
    session["Master_Exhaust_Fan"]= "OFF"
    session["Master_Bath_Window"]= "CLOSED"

    session["Bedroom2_Light"]= "OFF"
    session["Bedroom2_Lamp1"]= "OFF"
    session["Bedroom2_Lamp2"]= "OFF"
    session["Bedroom2_TV"]= "OFF"
    session["Bedroom2_Window1"]= "CLOSED"
    session["Bedroom2_Window2"]= "CLOSED"

    session["Bedroom3_Light"]= "OFF"
    session["Bedroom3_Lamp1"]= "OFF"
    session["Bedroom3_Lamp2"]= "OFF"
    session["Bedroom3_TV"]= "OFF"
    session["Bedroom3_Window1"]= "CLOSED"
    session["Bedroom3_Window2"]= "CLOSED"

    session["Bath_Light"]= "OFF"
    session["Bath_Water"]= "OFF"
    session["Exhaust_Fan"]= "OFF"
    session["Bath_Window"]= "CLOSED"

    session["Kitchen_Light"]= "OFF"
    session["Kitchen_Window1"]= "CLOSED"
    session["Kitchen_Window2"]= "CLOSED"
    session["Stove"]= "OFF"
    session["Oven"]= "OFF"
    session["Microwave"]= "OFF"
    session["Dishwasher"]= "OFF"
    session["Backdoor"]= "CLOSED"
    session["Kitchen_Water"]= "OFF"
    session["Refigerator"] = "OFF"

    session["Living_Room_Light"]= "OFF"
    session["Living_Room_Lamp1"]= "OFF"
    session["Living_Room_Lamp2"]= "OFF"
    session["Living_Room_TV"]= "OFF"
    session["Living_Room_Window1"]= "CLOSED"
    session["Living_Room_Window2"]= "CLOSED"
    session["Living_Room_Window3"]= "CLOSED"
    session["Front_Door"]= "CLOSED"

    session["Garage_Light"]= "OFF"
    session["Washer"]= "OFF"
    session["Dryer"]= "OFF"
    session["Entry_Door"]= "CLOSED"
    session["Garage_Door1"]= "CLOSED"
    session["Garage_Door2"]= "CLOSED"

    return render_template("home.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/thermostat', methods = ["GET","POST"])
def thermostat():
    data = weather_data.get_hourly("72228", "EBlIsCCfj8n8XjOvIMHXP7si9ej49XSU", str(date.today().strftime("%Y-%m-%d")))
    ct = SimulateHouse.HOUSE.temperature
    tt = 30
    if request.method == "POST":
        print(request.form.get("Thermostat"))
    return render_template("thermostat.html", outdoor_temp=round(data[2][-1], 2), currentTemp = ct, targetTemp = tt)

@app.route('/weather')
def weather():
    data = weather_data.get_hourly("72228", "EBlIsCCfj8n8XjOvIMHXP7si9ej49XSU", str(date.today().strftime("%Y-%m-%d")))
    historic_data = weather_data.get_weather(False)

    datelist = []
    hist_temps = []

    for entry in historic_data:
        datelist.append(str(entry[1]))
        if entry[2]:
            hist_temps.append(float((entry[2] * (9/5)) + 32))

    return render_template("weather.html", day=data[0], hours=data[1], temps=data[2], hist_temps=hist_temps,
                           datelist=datelist)


@app.route('/usages')
def usage():
    # database call
    data = usage_data.get_usages(False)
    dateList = []
    electric_data = []
    water_data = []
    electric_cost = []
    water_cost = []
    total = 0
    num_entries = 0

    for entry in data:
        dateList.append(str(entry[0]))
        electric_data.append(float(entry[1]))
        water_data.append(float(entry[2]))
        electric_cost.append(float(entry[3]))
        water_cost.append(float(entry[4]))

    avg_payment = (sum(electric_cost) + sum(water_cost)) / 2

    return render_template("usage.html", dateList=dateList, electric_data=electric_data, water_data=water_data,
                           electric_cost=electric_cost, water_cost=water_cost, avg_payment=round(avg_payment, 2))


@app.route('/info')
def info():
    return render_template("info.html")


@app.route('/controls',methods=["GET","POST"])
def controls():

    ml = session.get("Master_Light")
    ml1 = session.get("Master_Lamp1")
    ml2 = session.get("Master_Lamp2")
    mtv = session.get("Master_TV")
    mw1 = session.get("Master_Window1")
    mw2 = session.get("Master_Window2")
    mbl = session.get("Master_Bath_Light")
    mbw = session.get("Master_Bath_Window")
    mef = session.get("Master_Exhaust_Fan")
    mbwater = session.get("Master_Bath_Water")

    b2l = session.get("Bedroom2_Light")
    b2l1 = session.get("Bedroom2_Lamp1")
    b2l2 = session.get("Bedroom2_Lamp2")
    b2tv = session.get("Bedroom2_TV")
    b2w1 = session.get("Bedroom2_Window1")
    b2w2 = session.get("Bedroom2_Window2")

    b3l = session.get("Bedroom3_Light")
    b3l1 = session.get("Bedroom3_Lamp1")
    b3l2 = session.get("Bedroom3_Lamp2")
    b3tv = session.get("Bedroom3_TV")
    b3w1 = session.get("Bedroom3_Window1")
    b3w2 = session.get("Bedroom3_Window2")

    bl = session.get("Bath_Light")
    bwater = session.get("Bath_Water")
    ef = session.get("Exhaust_Fan")
    bw = session.get("Bath_Window")

    kl = session.get("Kitchen_Light")
    kw1 = session.get("Kitchen_Window1")
    kw2 = session.get("Kitchen_Window2")
    Stove = session.get("Stove")
    Oven = session.get("Oven")
    Microwave = session.get("Microwave")
    Dishwasher = session.get("Dishwasher")
    Backdoor = session.get("Backdoor")
    kw = session.get("Kitchen_Water")
    Refigerator = session.get("Refigerator")

    ll = session.get("Living_Room_Light")
    ll1 = session.get("Living_Room_Lamp1")
    ll2 = session.get("Living_Room_Lamp2")
    ltv = session.get("Living_Room_TV")
    lw1 = session.get("Living_Room_Window1")
    lw2 = session.get("Living_Room_Window2")
    lw3 = session.get("Living_Room_Window3")
    Frontdoor = session.get("Front_Door")

    gl = session.get("Garage_Light")
    Washer =  session.get("Washer")
    Dryer = session.get("Dryer")
    entry = session.get("Entry_Door")
    gd1 = session.get("Garage_Door1")
    gd2 = session.get("Garage_Door2")

    if request.method == "POST":
        ml = toggle(ml,"Master_Light")
        ml1 = toggle(ml1,"Master_Lamp1")
        ml2 = toggle(ml2,"Master_Lamp2")
        mtv = toggle(mtv,"Master_TV")
        mw1 = toggle(mw1,"Master_Window1")
        mw2 = toggle(mw2,"Master_Window2")

        mbl = toggle(mbl,"Master_Bath_Light")
        mbwater = toggle(mbw,"Master_Bath_Water")
        mef = toggle(mef,"Master_Exhaust_Fan")
        mbw = toggle(mbw,"Master_Bath_Window")

        b2l = toggle(b2l,"Bedroom2_Light")
        b2l1 = toggle(b2l1,"Bedroom2_Lamp1")
        b2l2 = toggle(b2l2,"Bedroom2_Lamp2")
        b2tv = toggle(b2tv,"Bedroom2_TV")
        b2w1 = toggle(b2w1,"Bedroom2_Window1")
        b2w2 = toggle(b2w2,"Bedroom2_Window2")

        b3l = toggle(b3l,"Bedroom3_Light")
        b3l1 = toggle(b3l1,"Bedroom3_Lamp1")
        b3l2 = toggle(b3l2,"Bedroom3_Lamp2")
        b3tv = toggle(b3tv,"Bedroom3_TV")
        b3w1 = toggle(b3w1,"Bedroom3_Window1")
        b3w2 = toggle(b3w2,"Bedroom3_Window2")

        bl = toggle(bl,"Bath_Light")
        bw = toggle(bw,"Bath_Window")
        ef = toggle(ef,"Exhaust_Fan")
        bwater = toggle(bwater,"Bath_Water")

        kl = toggle(kl,"Kitchen_Light")
        kw1 = toggle(kw1,"Kitchen_Window1")
        kw2 = toggle(kw2,"Kitchen_Window2")
        Stove = toggle(Stove,"Stove")
        Oven = toggle(Oven,"Oven")
        Microwave = toggle(Microwave,"Microwave")
        Dishwasher = toggle(Dishwasher,"Dishwasher")
        Backdoor = toggle(Backdoor,"Backdoor")
        kw = toggle(kw,"Kitchen_Water")
        Refigerator = toggle(Refigerator,"Refigerator")


        ll = toggle(ll,"Living_Room_Light")
        ll1 = toggle(ll1,"Living_Room_Lamp1")
        ll2 = toggle(ll2,"Living_Room_Lamp2")
        ltv = toggle(ltv,"Living_Room_TV")
        lw1 = toggle(lw1,"Living_Room_Window1")
        lw2 = toggle(lw2,"Living_Room_Window2")
        lw3 = toggle(lw3,"Living_Room_Window3")
        Frontdoor = toggle(Frontdoor,"Front_Door")

        gl = toggle(gl,"Garage_Light")
        Washer = toggle(Washer,"Washer")
        Dryer = toggle(Dryer,"Dryer")
        entry = toggle(entry,"Entry_Door")
        gd1 = toggle(gd1,"Garage_Door1")
        gd2 = toggle(gd2,"Garage_Door2")

        update_sensors()

    return render_template("controls.html", ml=ml, ml1=ml1, ml2=ml2, mtv=mtv,mw1=mw1,mw2=mw2,
    mbl=mbl,mbw=mbw,mef=mef,mbwater=mbwater,b2l=b2l,b2l1=b2l1,b2l2=b2l2,b2tv=b2tv,b2w1=b2w1,b2w2=b2w2,
    b3l=b3l,b3l1=b3l1,b3l2=b3l2,b3tv=b3tv,b3w1=b3w1,b3w2=b3w2,bl=bl,bw=bw,ef=ef,bwater=bwater,
    kl=kl,kw1=kw1,kw2=kw2,Stove=Stove,Oven=Oven,Microwave=Microwave,Dishwasher=Dishwasher,
    Backdoor=Backdoor,kw=kw,Refigerator=Refigerator,ll=ll,ll1=ll1,ll2=ll2,ltv=ltv,lw1=lw1,lw2=lw2,
    lw3=lw3,Frontdoor=Frontdoor,gl=gl,Washer=Washer,Dryer=Dryer,entry=entry,gd1=gd1,gd2=gd2)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/livingroom', methods=["GET","POST"])
def livingroom():
    ll = session.get("Living_Room_Light")
    ll1 = session.get("Living_Room_Lamp1")
    ll2 = session.get("Living_Room_Lamp2")
    ltv = session.get("Living_Room_TV")
    lw1 = session.get("Living_Room_Window1")
    lw2 = session.get("Living_Room_Window2")
    lw3 = session.get("Living_Room_Window3")
    Frontdoor = session.get("Front_Door")
    if request.method == "POST":
        ll = toggle(ll,"Living_Room_Light")
        ll1 = toggle(ll1,"Living_Room_Lamp1")
        ll2 = toggle(ll2,"Living_Room_Lamp2")
        ltv = toggle(ltv,"Living_Room_TV")
        lw1 = toggle(lw1,"Living_Room_Window1")
        lw2 = toggle(lw2,"Living_Room_Window2")
        lw3 = toggle(lw3,"Living_Room_Window3")
    return render_template("LivingRoom.html",ll=ll,ll1=ll1,ll2=ll2,ltv=ltv,lw1=lw1,lw2=lw2,
    lw3=lw3,Frontdoor=Frontdoor)

@app.route('/masterbath', methods=["GET","POST"])
def masterbath():
    mbl = session.get("Master_Bath_Light")
    mbw = session.get("Master_Bath_Window")
    mef = session.get("Master_Exhaust_Fan")
    mbwater = session.get("Master_Bath_Water")
    if request.method == "POST":
        mbl = toggle(mbl,"Master_Bath_Light")
    return render_template("masterbath.html",mbl=mbl,mbw=mbw,mef=mef,mbwater=mbwater)

@app.route('/bath', methods=["GET","POST"])
def bath():
    bl = session.get("Bath_Light")
    bwater = session.get("Bath_Water")
    ef = session.get("Exhaust_Fan")
    bw = session.get("Bath_Window")
    if request.method == "POST":
        bl = toggle(bl,"Bath_Light")
        bw = toggle(bw,"Bath_Window")
        ef = toggle(ef,"Exhaust_Fan")
        bwater = toggle(bwater,"Bath_Water")
    return render_template("bath.html",bl=bl,bw=bw,ef=ef,bwater=bwater)

@app.route('/masterbed', methods=["GET","POST"])
def masterbed():
    ml = session.get("Master_Light")
    ml1 = session.get("Master_Lamp1")
    ml2 = session.get("Master_Lamp2")
    mtv = session.get("Master_TV")
    mw1 = session.get("Master_Window1")
    mw2 = session.get("Master_Window2")
    mbl = session.get("Master_Bath_Light")
    mbw = session.get("Master_Bath_Window")
    mef = session.get("Master_Exhaust_Fan")
    mbwater = session.get("Master_Bath_Water")
    if request.method == "POST":
        ml = toggle(ml,"MasterLight")
        ml1 = toggle(ml1,"Master_Lamp1")
        ml2 = toggle(ml2,"Master_Lamp2")
    return render_template("masterbed.html",ml=ml,ml1=ml1,ml2=ml2,mtv=mtv,mw1=mw1,mw2=mw2,mbl=mbl,mbw=mbw,mef=mef,mbwater=mbwater)


@app.route('/bedroom2', methods=["GET","POST"])
def bedroom2():
    b2l = session.get("Bedroom2_Light")
    b2l1 = session.get("Bedroom2_Lamp1")
    b2l2 = session.get("Bedroom2_Lamp2")
    b2tv = session.get("Bedroom2_TV")
    b2w1 = session.get("Bedroom2_Window1")
    b2w2 = session.get("Bedroom2_Window2")
    if request.method == "POST":
        b2l = toggle(b2l,"Bedroom2_Light")
        b2l1 = toggle(b2l1,"Bedroom2_Lamp1")
        b2l2 = toggle(b2l2,"Bedroom2_Lamp2")
        b2tv = toggle(b2tv,"Bedroom2_TV")
        b2w1 = toggle(b2w1,"Bedroom2_Window1")
        b2w2 = toggle(b2w2,"Bedroom2_Window2")
    return render_template("bedroom2.html",b2l=b2l,b2l1=b2l1,b2l2=b2l2,b2tv=b2tv,b2w1=b2w1,b2w2=b2w2)

@app.route('/bedroom3', methods=["GET","POST"])
def bedroom3():
    b3l = session.get("Bedroom3_Light")
    b3l1 = session.get("Bedroom3_Lamp1")
    b3l2 = session.get("Bedroom3_Lamp2")
    b3tv = session.get("Bedroom3_TV")
    b3w1 = session.get("Bedroom3_Window1")
    b3w2 = session.get("Bedroom3_Window2")
    if request.method == "POST":
        b3l = toggle(b3l,"Bedroom3_Light")
        b3l1 = toggle(b3l1,"Bedroom3_Lamp1")
        b3l2 = toggle(b3l2,"Bedroom3_Lamp2")
        b3tv = toggle(b3tv,"Bedroom3_TV")
        b3w1 = toggle(b3w1,"Bedroom3_Window1")
        b3w2 = toggle(b3w2,"Bedroom3_Window2")
    return render_template("bedroom3.html",b3l=b3l,b3l1=b3l1,b3l2=b3l2,b3tv=b3tv,b3w1=b3w1,b3w2=b3w2)

@app.route('/kitchen', methods=["GET","POST"])
def kitchen():
    kl = session.get("Kitchen_Light")
    kw1 = session.get("Kitchen_Window1")
    kw2 = session.get("Kitchen_Window2")
    Stove = session.get("Stove")
    Oven = session.get("Oven")
    Microwave = session.get("Microwave")
    Dishwasher = session.get("Dishwasher")
    Backdoor = session.get("Backdoor")
    kw = session.get("Kitchen_Water")
    Refigerator = session.get("Refigerator")
    if request.method == "POST":
        kl = toggle(kl,"Kitchen_Light")
        kw1 = toggle(kw1,"Kitchen_Window1")
        kw2 = toggle(kw2,"Kitchen_Window2")
        Stove = toggle(Stove,"Stove")
        Oven = toggle(Oven,"Oven")
        Microwave = toggle(Microwave,"Microwave")
        Dishwasher = toggle(Dishwasher,"Dishwasher")
        Backdoor = toggle(Backdoor,"Backdoor")
        kw = toggle(kw,"Kitchen_Water")
        Refigerator = toggle(Refigerator,"Refigerator")
    return render_template("kitchen.html",kl=kl,kw1=kw1,kw2=kw2,Stove=Stove,Oven=Oven,Microwave=Microwave,Dishwasher=Dishwasher,
    Backdoor=Backdoor,kw=kw,Refigerator=Refigerator)

@app.route('/garage', methods=["GET","POST"])
def garage():
    gl = session.get("Garage_Light")
    Washer =  session.get("Washer")
    Dryer = session.get("Dryer")
    entry = session.get("Entry_Door")
    gd1 = session.get("Garage_Door1")
    gd2 = session.get("Garage_Door2")
    if request.method == "POST":
        gl = toggle(gl,"Garage_Light")
        Washer = toggle(Washer,"Washer")
        Dryer = toggle(Dryer,"Dryer")
        entry = toggle(entry,"Entry_Door")
        gd1 = toggle(gd1,"Garage_Door1")
        gd2 = toggle(gd2,"Garage_Door2")    
    return render_template("UtilityGarage.html",gl=gl,Washer=Washer,Dryer=Dryer,entry=entry,gd1=gd1,gd2=gd2)

@app.route('/pic')
def pic():
    light = False
    return render_template("pixel.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

if __name__ == '__main__':
    app.run(debug=True)
