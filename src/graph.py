import pandas as pd
import matplotlib.pyplot as plt
import numpy
import sys
import os

WeekDayDict = {
    0 : 'Sun',
    1 : 'Mon',
    2 : 'Tue',
    3 : 'Wed',
    4 : 'Thu',
    5 : 'Fri',
    6 : 'Sat'
}

# Keys in Data File
GYM = 'gym'
CURRENT = 'current'
MAX = 'max'
TIME = 'time'
DATE = 'date'
WEEKDAY = 'weekday'

def __main__():
    data = pd.read_csv('GymOccupancyInfo.csv')

    gyms = []
    gymNames = data[GYM].unique()

    for gym in gymNames:
        temp = gyms.append(ClimbingGym(gym))
        temp.DataByWeekday = data.loc[(data[GYM] == 'Plano') & (data[WEEKDAY] == 'Thu')]

    PlanoData = data.loc[(data['gym'] == 'Plano') & (data['weekday'] == 'Thu')]

    # currentOccupancy = DallasData['current'].to_numpy()
    # currentTime = DallasData['time'].to_numpy()
    currentOccupancy = PlanoData['current'].to_numpy()
    currentTime = PlanoData['time'].to_numpy()

    plt.figure(1)
    plt.plot(currentOccupancy)
    plt.xticks(range(len(currentTime)), currentTime)
    plt.locator_params(axis='x', nbins=20)
    plt.title('Occupancy vs Time of Day - Plano')
    plt.show()
    return

class ClimbingGym:
    def __init__(self, name):
        self.name = name
        self.DataByWeekday = []

__main__()