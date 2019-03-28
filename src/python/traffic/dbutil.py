import datetime
import dateutil
import pandas
import pyodbc
from traffic.tconfig import db_config

connection_string = ('Driver={{ODBC Driver 13 for SQL Server}};'
                     'Server=tcp:{server};'
                     'Database={database};'
                     'Uid={uid};'
                     'Pwd={dbpassword};'
                     'Encrypt=yes;'
                     'TrustServerCertificate=no;'
                     'Connection Timeout=30;').format(**db_config['CONNECTION'])


def get_nameidtable():
    query = "SELECT * FROM NameIdTable"
    with pyodbc.connect(connection_string) as conn:
        df = pandas.read_sql_query(query, conn)
    return df.sort_values(by=['TRAVELTIMEID'])


def _format_date_as_string(dt, local_tz):
    if type(dt) == str:
        local_zone = dateutil.tz.gettz(local_tz)
        utc_zone = dateutil.tz.gettz('UTC')
        return dateutil.parser.parse(dt).replace(tzinfo=local_zone).astimezone(utc_zone).strftime('%Y-%m-%dT%H:%M:%S')
    if type(dt) == datetime.datetime:
        return dt.strftime('%Y-%m-%dT%H:%M:%S')


def get_travel_times(tid, startdate='1970-01-01', enddate='3000-01-01', local_tz = 'US/Pacific'):
    """Get the travel times for a route between given times
    Returns a Pandas DataFrame. The TimeUpdated field will be converted to the timezone specified
    in local_tz.
    The startdate and enddate fields are assumed to be in the same timezone as local_tz

    tid - TravelTimeID, the ID in the WSDOT API for the desired route
    startdate - a string or datetime object, assumed to be in the same tz as local_tz, specifying the lower bound (inclusive) for the query
    enddate - a string or datetime object, assumed to be in the same tz as local_tz, specifying the upper bound (inclusive) for the query
    """
    from_zone = dateutil.tz.gettz('UTC')
    to_zone = dateutil.tz.gettz(local_tz)
    startdate = _format_date_as_string(startdate, local_tz)
    enddate = _format_date_as_string(enddate, local_tz)

    query = "SELECT TimeUpdated,CurrentTime,Description FROM TravelTimes WHERE TRAVELTIMEID = {0} AND TIMEUPDATED BETWEEN '{1}' AND '{2}'".format(tid, startdate, enddate)
    with pyodbc.connect(connection_string) as conn:
        df = pandas.read_sql_query(query, conn)
    df['TimeUpdated'] = df['TimeUpdated'].dt.tz_localize(from_zone).dt.tz_convert(to_zone)
    return df.sort_values(by=['TimeUpdated'])

def query(query):
    with pyodbc.connect(connection_string) as conn:
        df = pandas.read_sql_query(query, conn)
    return df

def get_daily_row_count():
    """
    For diagnostic purposes
    Returns a count of the number of rows in the table, by day.
    """
    pass
    #query = "SELECT TimeUpdated,CurrentTime,Description FROM TravelTimes".format(tid, startdate, enddate)    