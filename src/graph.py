import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Keys in Data File
GYM = 'gym'
CURRENT = 'current'
MAX = 'max'
TIME = 'time'
DATE = 'date'
WEEKDAY = 'weekday'

TimeRanges = [
    ['6:00', '6:59'],
    ['7:00', '7:59'],
    ['8:00', '8:59'],
    ['9:00', '9:59'],
    ['10:00', '10:59'],
    ['11:00', '11:59'],
    ['12:00', '12:59'],
    ['13:00', '13:59'],
    ['14:00', '14:59'],
    ['15:00', '15:59'],
    ['16:00', '16:59'],
    ['17:00', '17:59'],
    ['18:00', '18:59'],
    ['19:00', '19:59'],
    ['20:00', '20:59'],
    ['21:00', '21:59'],
    ['22:00', '22:59'],
    ['23:00', '23:59']
]

TimeCategories = [
    '6:00', '7:00', 
    '8:00', '9:00', 
    '10:00', '11:00', 
    '12:00', '13:00', 
    '14:00', '15:00', 
    '16:00', '17:00', 
    '18:00', '19:00', 
    '20:00', '21:00', 
    '22:00', '23:00'
]

def __main__():
    data = pd.read_csv('GymOccupancyInfo.csv', index_col='time', parse_dates=True)

    gyms = []
    gymNames = data[GYM].unique()
    weekdays = data[WEEKDAY].unique()

    # Create climbing gym objects
    for gym in gymNames:
        gyms.append(ClimbingGym(gym, weekdays))

    # Store all different weekday data for specific gym in ClimbingGym object
    for gym in gyms:
        gym.currGymData = data.loc[(data[GYM] == gym.name)]

    # Create a graph for each weekday for each gym
    for gym in gyms:
        gym.graphData()

class ClimbingGym:
    def __init__(self, name, weekdays):
        self.name = name
        self.currGymData = []
        self.weekdays = weekdays

    def graphData(self):
        for weekday in self.weekdays:
            self.__graphByWeekday(weekday)

    def __graphByWeekday(self, weekday):
        allDataByWeekday = self.__getAllDataByWeekday(weekday)
        occupancyDataByWeekday = self.__getOccupancyDataByWeekday(weekday, allDataByWeekday)

        y_pos = np.arange(len(TimeCategories))
        rects = plt.bar(y_pos, occupancyDataByWeekday, align='center', alpha=0.5, width=1.0, facecolor='black', edgecolor='black')
        plt.xticks(y_pos, TimeCategories)
        plt.ylabel('Occupancy')
        plt.xlabel('Time')
        plt.title('Occupancy over time - ' + weekday + ' - ' + self.name)
        self.__labelPlot(rects)
        plt.show()

    def __getAllDataByWeekday(self, weekday):
        return self.currGymData.loc[self.currGymData[WEEKDAY] == weekday]
    
    def __getOccupancyDataByWeekday(self, weekday, data):
        occupancyDataByWeekday = []
        for timeRange in TimeRanges:
            dataBetweenTimeRange = self.__getOccupancyDataByWeekdayBetweenTimeRange(timeRange, data)
            if(dataBetweenTimeRange[CURRENT].sum() != 0):
                occupancyDataByWeekday.append(round(dataBetweenTimeRange[CURRENT].sum()/dataBetweenTimeRange[CURRENT].count()))
            else:
                occupancyDataByWeekday.append(0.0)
        return occupancyDataByWeekday

    def __getOccupancyDataByWeekdayBetweenTimeRange(self, timeRange, data):
        return data.between_time(timeRange[0], timeRange[1])

    def __labelPlot(self, rects, xpos='center'):
        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')

__main__()