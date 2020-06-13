import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('InputData/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fd403b3054061a52e5c4a08dadc245bc6e1b0adabbf12a9eadba68e8')

#Read from csv file
df = pd.read_csv('InputData/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

#Sort based on month and date for an Year
df = df.sort_values(by=['ID','Date'])
df['Year'], df['Month-date'] = zip(*df['Date'].apply(lambda x: (x[:4], x[5:])))
df = df[df['Month-date'] != '02-29']

#Find min /max temp of the day
temp_min = df[(df['Element'] == 'TMIN') & (df['Year'] != '2015')].groupby('Month-date').aggregate({'Data_Value':np.min})
temp_max = df[(df['Element'] == 'TMAX') & (df['Year'] != '2015')].groupby('Month-date').aggregate({'Data_Value':np.max})

#Find min /max temp of the day for 2015
temp_min_15 = df[(df['Element'] == 'TMIN') & (df['Year'] == '2015')].groupby('Month-date').aggregate({'Data_Value':np.min})
temp_max_15 = df[(df['Element'] == 'TMAX') & (df['Year'] == '2015')].groupby('Month-date').aggregate({'Data_Value':np.max})

#Find broken temp
broken_min = np.where(temp_min_15['Data_Value'] < temp_min['Data_Value'])
broken_max = np.where(temp_max_15['Data_Value'] > temp_max['Data_Value'])


#start Drawing line and scatter plots

plt.figure()
plt.plot(temp_max.values, c='r', label='record high')
plt.plot(temp_min.values, c='b', label='record low')
plt.xlabel('Day of the Year')
plt.ylabel('Temperature (Tenths of Degrees C)')
plt.title('Global Daily Climate Records')
plt.scatter(broken_max, temp_max_15.iloc[broken_max], s=50, c='green', label='broken high')
plt.scatter(broken_min, temp_min_15.iloc[broken_min], s=50, c='red', label='broken low')
plt.gca().axis([-5, 370, -150, 600])
plt.xticks(range(0, len(temp_max), 30), temp_max.index[range(0, len(temp_max), 30)], rotation=40)
plt.fill_between(range(len(temp_max)), temp_max['Data_Value'], temp_min['Data_Value'], facecolor='yellow', alpha=0.25)
plt.legend(frameon=False, loc=0)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)