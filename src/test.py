import pandas as pd
import numpy as np

data = pd.read_csv('GymOccupancyInfoOLD.csv', index_col='time', parse_dates=True)

PlanoFridayData = data.loc[(data['weekday'] == 'Fri') & (data['gym'] == 'Plano')]

PlanoFriday12PMData = PlanoFridayData.between_time('12:00', '12:59')
PlanoFriday1PMData = PlanoFridayData.between_time('13:00', '13:59')

print(PlanoFridayData)

print(PlanoFriday12PMData)
print(PlanoFriday1PMData)