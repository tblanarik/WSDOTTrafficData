import pandas as pd
import requests
import os
from traffic.tconfig import keys_config

def get_seattle_weather(startdate, enddate=None):
    """
    A quick wrapper to get SEATAC weather data for a date or date range, including:
        - TMAX : high temperature
        - TMIN : low temperature
        - TAVG : avg temperature
        - PRCP : total inches of precipitation for the day
    """
    if not enddate:
        enddate = startdate
    token = {"token" : keys_config['NOAA']['apikey']}
    res = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=GHCND:USW00024233&' \
                       'startdate={startdate}&enddate={enddate}&limit=100&units=standard&datatypeid=TMAX&datatypeid=TMIN' \
                       '&datatypeid=TAVG&datatypeid=PRCP'.format(startdate=startdate, enddate=enddate), headers=token).json()
    return pd.DataFrame.from_dict(res['results'])