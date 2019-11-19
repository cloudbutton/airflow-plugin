import matplotlib.pyplot as plt
import json
import os
import numpy as np

from mpl_toolkits.basemap import Basemap
from io import BytesIO

def plot_temp(results, ibm_cos):
    country = os.environ.get('country')
    bucket = os.environ.get('bucket')
    plot = os.environ.get('plot')

    all_results = [item for sublist in results for item in sublist]
    
    llcrnrlon=min(all_results, key=lambda sample : sample['lon'])['lon']
    llcrnrlat=min(all_results, key=lambda sample : sample['lat'])['lat']
    urcrnrlon=max(all_results, key=lambda sample : sample['lon'])['lon']
    urcrnrlat=max(all_results, key=lambda sample : sample['lat'])['lat']

    lons = [sample['lon'] for sample in all_results]
    lats = [sample['lat'] for sample in all_results]

    fig = plt.gcf()
    fig.set_size_inches(8, 6.5)

    m = Basemap(
        llcrnrlon=llcrnrlon,
        llcrnrlat=llcrnrlat,
        urcrnrlon=urcrnrlon,
        urcrnrlat=urcrnrlat,
        projection='merc',
        resolution='h')
    
    x, y = m(lons, lats)

    if plot == 'temp':
        cmap = plt.get_cmap('coolwarm')
        data = [sample['temp'] for sample in all_results]
        plt.scatter(x, y, 2.5, alpha=0.5, c=data, zorder=2, cmap=cmap)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Temperature (ºC)')
        plt.title('{} temperature'.format(country))
    elif plot == 'humi':
        cmap = plt.get_cmap('Blues')
        data = [sample['humi'] for sample in all_results]
        plt.scatter(x, y, 2.5, alpha=0.5, c=data, zorder=2, cmap=cmap)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Humidity (%)')
        plt.title('{} humidity (%)'.format(country))
    elif plot == 'press':
        cmap = plt.get_cmap('seismic')
        data = [sample['press'] for sample in all_results]
        plt.scatter(x, y, 2.5, alpha=0.5, c=data, zorder=2, cmap=cmap)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Pressure (hPa)')
        plt.title('{} pressure (hPa)'.format(country))
    else:
        raise Exception()

    m.drawcountries(color="black", zorder=3)
    m.drawmapboundary(fill_color='cornflowerblue')
    m.fillcontinents(color='moccasin', lake_color='cornflowerblue', zorder=1)
    buff = BytesIO()
    plt.savefig(buff, dpi=100)
    buff.seek(0)

    key = 'image_{}_{}.png'.format(country, plot)
    ibm_cos.put_object(Bucket=bucket, Key=key, Body=buff)
    return key


# import manage_data
# import pywren_ibm_cloud as pywren

# bucket = 'aitor-data'
# countries = ['ES']

# pywex = pywren.ibm_cf_executor()
# pywex.call_async(manage_data.get_dataset, {'data_url' : 'http://bulk.openweathermap.org/sample/weather_16.json.gz', 'bucket' : bucket})
# pywex.wait()

# pywex.map(manage_data.parse_data, 'cos://{}/weather_data'.format(bucket), chunk_size=1024**2, extra_params=[countries, bucket])
# pywex.wait()

# pywex = pywren.ibm_cf_executor(runtime_memory=2048, runtime='aitorarjona/python3.6_pywren_matplotlib-basemap:1.0', log_level='DEBUG')
# pywex.map_reduce(map_function=manage_data.get_temp_data, map_iterdata='cos://{}/ES/'.format(bucket), reduce_function=merge_data, extra_params=['ES', bucket])
# pywex.wait()

