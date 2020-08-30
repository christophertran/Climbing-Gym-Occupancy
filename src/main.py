from helium import *
from datetime import datetime
import pandas as pd
import time as time

def __main__():
    print('Starting Program.')
    print('Creating Gym Objects.')
    Gyms = []
    Gyms.append(ClimbingGym('Dallas'))
    Gyms.append(ClimbingGym('Denton'))
    Gyms.append(ClimbingGym('Fort Worth'))
    Gyms.append(ClimbingGym('Grapevine'))
    Gyms.append(ClimbingGym('Plano'))
    Gyms.append(ClimbingGym('OKC'))
    Gyms.append(ClimbingGym('Norman'))

    firstTime = True
    chromeOpen = False
    hadError = False
    errorStr = ''
    count = 1

    print('Starting Event Loop')
    while(True):
        print('\n=============================================================')
        print('The time is: ' + datetime.now().ctime())
        if(isDay() and not chromeOpen):
            print('It is daytime, starting Chrome.')
            start_chrome('https://summitgyms.com/tracker', headless=True)
            chromeOpen = True
        print('=============================================================\n')

        try:
            while(isDay()):
                print('\n=============================================================')
                
                if(hadError):
                    print('We had an error. Count: ' + str(count) + ' Error: ' + errorStr)
                
                print(str(count) + ' - Grabbing Information, the time is: ' + datetime.now().ctime())

                DataFrame = pd.DataFrame()

                for gym in Gyms:
                    print('Scraping for: ' + gym.name)
                    gym.makeGymInformationFrame()
                    gym.printCurrentInfo()
                    DataFrame = DataFrame.append(gym.infoFrame, ignore_index=True)

                if(firstTime):
                    print('Exporting information to CSV for the first time')
                    firstTime = False
                    DataFrame.to_csv('GymOccupancyInfo.csv', header=True, index=False)
                else:
                    print('Exporting information to CSV')
                    DataFrame.to_csv('GymOccupancyInfo.csv', mode='a', header=False, index=False)

                count += 1
                print('Sleeping for 10 minutes.')
                print('=============================================================\n')
                time.sleep(600)

        except Exception as ex:
            print('\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            print('Error: ', ex)
            print('Count: ', count)
            kill_browser()
            chromeOpen = False
            hadError = True
            errorStr = ex
            print('Continuing the event loop.')
            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n')

        print('\n=============================================================')
        if(chromeOpen):
            print('It is night time, killing browser.')
            kill_browser()
            chromeOpen = False
        if(not isDay()):
            print('It is night time, sleeping for 30 minutes and checking again.')
        print('=============================================================\n')
        time.sleep(1800)

def isDay():
    currentTime = datetime.now()
    currentHour = int(currentTime.strftime('%H'))
    currentWeekday = currentTime.strftime('%a')
    if(currentWeekday == 'Sat' or currentWeekday == 'Sun'):
        # If it is a weekend and between 9am-12am then return true
        if(9 <= currentHour and currentHour <= 23):
            return True
        else:
            return False
    else:
        # If it is a weekday and between 6am-12am then return true
        if(6 <= currentHour and currentHour <= 23):
            return True
        else:
            return False

class ClimbingGym:
    def __init__(self, name):
        self.name = name
        self.maxCapacity = 0
        self.currentOccupancy = 0
        self.infoFrame = {}

    def printCurrentInfo(self):
        print('Name: ' + self.name + 
            '\nCurrent: ' + self.currentOccupancy + 
            '\nMax: ' + self.maxCapacity + '\n')

    def getGymInformation(self):
        splitInfo = Text(self.name).value.split(' ')
        print(splitInfo)
        self.currentOccupancy = splitInfo[len(splitInfo) - 1].split('/')[0]
        self.maxCapacity = splitInfo[len(splitInfo) - 1].split('/')[1]

    def makeGymInformationFrame(self):
        self.getGymInformation()
        timeNow = datetime.now()
        self.infoFrame = {
            'gym': self.name,
            'current': self.currentOccupancy,
            'max': self.maxCapacity,
            'weekday': timeNow.strftime('%a'),
            'time': timeNow.strftime('%H:%M:%S'),
            'timefull': timeNow.strftime('%Y-%m-%d %H:%M:%S')
        }

__main__()