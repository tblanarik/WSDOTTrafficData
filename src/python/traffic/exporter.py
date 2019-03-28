import pandas
import datetime
import traffic.dbutil as dbutil
from datetime import timedelta

def export_all(csv_filename, min_date='2018-04-15', max_date=None):
    min_date = datetime.datetime.strptime(min_date, '%Y-%m-%d')
    if not max_date:
        max_date = datetime.datetime.now()
    else:
        max_date = datetime.datetime.strptime(max_date, '%Y-%m-%d')        
    current_date = min_date

    base_query = "SELECT * FROM TravelTimes WHERE TIMEUPDATED BETWEEN '{0}' AND '{1}'"#.format(startdate, enddate)

    df_list = []

    while(current_date < max_date):
        next_date = current_date + timedelta(days=1)
        print(current_date.strftime('%Y-%m-%d'), "..." ,next_date.strftime('%Y-%m-%d'))
        tquery = base_query.format(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
        df_list.append(dbutil.query(tquery))
        current_date = next_date
    df = pandas.concat(df_list)   
    df.to_csv(csv_filename)
    
