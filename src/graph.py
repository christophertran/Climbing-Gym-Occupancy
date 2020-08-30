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

# TODO
# I want for each gym, 7 bar graphs, one for each day of the week. 
# Each bar graph will have hour increments where they take the average of the data in the file for that weekday
# And graph that for that hour in that bucket for all hours between 6am-12am for Weekdays, and 9am-12am for Weekends

def __main__():
    data = pd.read_csv('GymOccupancyInfo.csv')

    gyms = []
    gymNames = data[GYM].unique()
    weekdays = data[WEEKDAY].unique()

    # Create climbing gym objects
    for gym in gymNames:
        gyms.append(ClimbingGym(gym, weekdays))

    # Store all different weekday data for specific gym in ClimbingGym object
    for gym in gyms:
        gym.currGymData = data.loc[(data[GYM] == gym.name)]

    gyms[0].graphData()

class ClimbingGym:
    def __init__(self, name, weekdays):
        self.name = name
        self.currGymData = []
        self.weekdays = weekdays

    def getDataByWeekday(self, weekday):
        return self.currGymData.loc[self.currGymData[WEEKDAY] == weekday]

    def graphByWeekday(self, weekday):
        dataByWeekday = self.getDataByWeekday(weekday)
        currentOccupancy = self.getCurrentOccupancy(dataByWeekday)
        currentTime = self.getCurrentTime(dataByWeekday)

        plt.figure(1)
        plt.plot(currentOccupancy)
        plt.xticks(range(len(currentTime)), currentTime)
        plt.locator_params(axis='x', nbins=20)
        plt.title('Occupancy vs Time of Day - ' + self.name + ' - ' + weekday)
        plt.show()

    def getCurrentOccupancy(self, data):
        return data[CURRENT].to_numpy()
    
    def getCurrentTime(self, data):
        return data[TIME].to_numpy()

    def graphData(self):
        for weekday in self.weekdays:
            self.graphByWeekday(weekday)

__main__()