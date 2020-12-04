import json
import subprocess
import psycopg2
import datetime


def update(api_key, **kwargs):
    """
    Updates Database according to the most recent date.

    api_key: (str) Your Api Key to invoke the Meteostat Weather API
    **start: (str) Custom Start Date to update the DB. (format: YYYY-MM-DD)
    """
    station_id = "72228"
    conn = psycopg2.connect(
        host="164.111.161.243",
        database="Team5DB",
        user="Team5",
        password="5Team5")

    cur = conn.cursor()
    # Get most recent date entry
    cur.execute("SELECT * FROM weather_data ORDER BY date_time DESC LIMIT 1;")
    # Get entry as a datetime object
    most_recent = cur.fetchone()[1]
    # Use start arg if present, otherwise use a day after the most recent entry
    start = kwargs.get('start') or (most_recent + datetime.timedelta(days=1))
    today = str(datetime.date.today().strftime("%Y-%m-%d"))

    if most_recent.strftime("%Y-%m-%d") == today:
        print("Database is already up to date.")

    else:
        result = subprocess.check_output(["curl", "-s", "--header", "x-api-key: {}".format(api_key),
                                          "https://api.meteostat.net/v2/stations/daily?station={}&start={}&end={}"
                                         .format(station_id, start, today)])

        new_str = result.decode('utf-8')

        result = json.loads(new_str)

        for entry in result['data']:
            cur.execute("INSERT INTO {} "
                        "(station_id, date_time, avg_temp, low_temp, high_temp,"
                        "precip, snow, wind_direction, wind_speed, air_pressure, total_sunshine) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format("weather_data"),
                        (station_id, entry['date'], entry['tavg'], entry['tmin'], entry['tmax'], entry['prcp'],
                         entry['snow'], entry['wdir'], entry['wspd'], entry['pres'], entry['tsun']))
            conn.commit()

    cur.close()


def get_weather(output, **kwargs):
    """
    Get historic weather from the Team5 Database.
    output: [boolean] Whether or not to print retrieved entries to console.
    **start: [str] Start point for retrieving data.
    **end: [str] End point for retrieving data.
    """
    conn = psycopg2.connect(
        host="164.111.161.243",
        database="Team5DB",
        user="Team5",
        password="5Team5")

    cur = conn.cursor()

    cur.execute("SELECT * FROM weather_data ORDER BY date_time ASC LIMIT 1;")
    least_recent = cur.fetchone()[1]
    cur.execute("SELECT * FROM weather_data ORDER BY date_time DESC LIMIT 1;")
    most_recent = cur.fetchone()[1]

    if kwargs.get('start') is not None and kwargs.get('end') is not None:
        cur.execute("SELECT * FROM weather_data WHERE date_time BETWEEN '{}' AND '{}'".format(kwargs.get('start'),
                                                                                          kwargs.get('end')))
    elif kwargs.get('start') is not None and kwargs.get('end') is None:
        cur.execute("SELECT * FROM weather_data WHERE date_time BETWEEN '{}' AND '{}'".format(kwargs.get('start'),
                                                                                          str(most_recent)))
    elif kwargs.get('start') is None and kwargs.get('end') is not None:
        cur.execute("SELECT * FROM weather_data WHERE date_time BETWEEN '{}' AND '{}'".format(str(least_recent),
                                                                                          kwargs.get('end')))
    else:
        cur.execute("SELECT * FROM weather_data WHERE date_time BETWEEN '{}' AND '{}'".format(least_recent,
                                                                                          (most_recent)))

    result = cur.fetchall()
    if output:
        for entry in result:
            print(entry)

    return result


def get_hourly(station_id, api_key, day):
    result = subprocess.check_output(["curl", "-s", "--header", "x-api-key: {}".format(api_key),
                                      "https://api.meteostat.net/v2/stations/hourly?station={}&start={}&end={}"
                                     .format(station_id, day, day)])

    new_str = result.decode('utf-8')

    result = json.loads(new_str)
    output = []
    day = result['data'][0]['time'].split(" ")[0]
    times = []
    bs_times = ["12am", "1am", "2am", "3am", "4am", "5am", "6am", "7am", "8am", "9am", "10am", "11am",
                "12pm", "1pm", "2pm", "3pm", "4pm", "5am", "6pm", "7pm", "8pm", "9pm", "10pm", "11pm"]
    temps = []

    for time in result['data']:
        times.append(str(time['time'].split(" ")[1]))
        if time['temp']:
            temps.append(((time['temp'] * (9/5)) + 32))

    output = [day, bs_times, temps]

    return output



# *Example use*
# data = get_weather(False, start='2020-10-6', end='2020-10-14')

# *Example use*
# update("EBlIsCCfj8n8XjOvIMHXP7si9ej49XSU")
get_hourly("72228", "EBlIsCCfj8n8XjOvIMHXP7si9ej49XSU", str(datetime.date.today().strftime("%Y-%m-%d")))
