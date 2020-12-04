import psycopg2
import datetime


def get_usages(output, **kwargs):
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

    table = "usages"

    cur.execute("SELECT * FROM {} ORDER BY date ASC LIMIT 1;".format(table))
    least_recent = cur.fetchone()[0]
    cur.execute("SELECT * FROM {} ORDER BY date DESC LIMIT 1;".format(table))
    most_recent = cur.fetchone()[0]

    if kwargs.get('start') is not None and kwargs.get('end') is not None:
        cur.execute("SELECT * FROM {} WHERE date BETWEEN '{}' AND '{}'".format(table, kwargs.get('start'),
                                                                                          kwargs.get('end')))
    elif kwargs.get('start') is not None and kwargs.get('end') is None:
        cur.execute("SELECT * FROM {} WHERE date BETWEEN '{}' AND '{}'".format(table, kwargs.get('start'),
                                                                                          str(most_recent)))
    elif kwargs.get('start') is None and kwargs.get('end') is not None:
        cur.execute("SELECT * FROM {} WHERE date BETWEEN '{}' AND '{}'".format(table, str(least_recent),
                                                                                          kwargs.get('end')))
    else:
        cur.execute("SELECT * FROM {} WHERE date BETWEEN '{}' AND '{}'".format(table, least_recent,
                                                                                          (most_recent)))

    result = cur.fetchall()
    if output:
        for entry in result:
            print(entry)

    return result
