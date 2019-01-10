import pandas

def filter_for_weekdays(df):
    return df[df['TimeUpdated'].dt.weekday < 5]

def filter_day_of_week(df, dow):
    return df[df['TimeUpdated'].dt.weekday == dow]

def filter_hour_range(df, lh, hh):
    return df[(df['TimeUpdated'].dt.hour >= lh) & (df['TimeUpdated'].dt.hour <= hh)]

def max_time_by_day(df):
    return df.groupby(pandas.Grouper(freq='D')).max()

def annotate_am_pm(df):
    return df.assign(timeOfDay=pandas.cut(df.TimeUpdated.dt.hour,
        [-1, 12, 24],
        labels=['AM', 'PM']))