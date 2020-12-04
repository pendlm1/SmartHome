import json
import subprocess
import psycopg2


def get_data(api_key, interval, station, start, end):
    result = subprocess.check_output(["curl", "-s", "--header", "x-api-key: {}".format(api_key),
                                      "https://api.meteostat.net/v2/stations/{}?station={}&start={}&end={}".format(interval,
                                                                                                                   station,
                                                                                                                   start,
                                                                                                                   end)]
                                     )
    new_str = result.decode('utf-8')

    result = json.loads(new_str)

    return result


def write_to_db(table, values, raw):
    """
    Writes weather api data to weather_data table.
    :param table: string table name
    :param values:
    :param raw:
    :return:
    """
    conn = psycopg2.connect(
        host="164.111.161.243",
        database="Team5DB",
        user="Team5",
        password="5Team5")

    cur = conn.cursor()

    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = '{}';".format(table))

    columns = cur.fetchall()
    holders = ""
    col_names = ""
    for name in columns:
        holders = holders + "%s"
        col_names = col_names + name[0]

        if name[0] != columns[-1][-1]:
            holders = holders + ", "
            col_names = col_names + ", "

    #print(col_names)
    # print(holders)

    command = "INSERT INTO {} ({}) VALUES({});".format(table, col_names, holders)
    command = command.format(values)

    # print(command)

    if raw is None:
        cur.execute(command, values)
    else:
        cur.execute(raw, values)

    conn.commit()
    cur.close()


# data = get_data("EBlIsCCfj8n8XjOvIMHXP7si9ej49XSU", "daily", "72228", "2020-11-10", "2020-11-10")["data"][0]
# values = ["72228"]
#
# print(data)
#
# for key in data:
#     if key != "wpgt":
#         values.append(data[key])

# write_to_db("weather_data", None, None)

# write_to_db("weather_data", tuple(values), None)
