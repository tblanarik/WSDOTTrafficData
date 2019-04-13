import pandas
from enum import Enum

class TrafficTable(pandas.DataFrame):
    @property
    def _constructor(self):
        return TrafficTable

    def weekdays(self):
        '''
        Returns a TrafficTable filtered to only weekdays (no Saturday or Sunday)
        '''
        return self[self['TimeUpdated'].dt.weekday < 5]
    
    def days_filter(self, days):
        '''
        Returns a TrafficTable filtered to only the specified days
        Args:
            days: a sequence containing integers representing days to keep
        '''
        return self[self['TimeUpdated'].dt.weekday in days]

    def hours_filter(self, lh, hh):
        '''
        Returns a TrafficTable filtered to only the specified hours (inclusive)
        Args:
            lh: lower hour
            hh: upper hour
        '''
        return self[(self['TimeUpdated'].dt.hour >= lh) & (self['TimeUpdated'].dt.hour <= hh)]

    def filter_ids(self, tid):
        '''
        Returns a TrafficTable filtered to only the TravelTimeIds specified
        '''
        return self[self['TravelTimeIds'] == tid]