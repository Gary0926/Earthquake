from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd
import numpy as np
from matplotlib.patches import Polygon      #載入設定著色需要的 Polygon 與 PatchCollection
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap    #載入 GIS 所需的 Basemap
import warnings                  #載入 warning 模組並將警告過濾設為 “ignore”
warnings.filterwarnings('ignore')
BasePath='/content/drive/MyDrive/Python'
plt.figure(figsize=(16,8))
map = Basemap(llcrnrlon = 119.3, llcrnrlat = 20.7, urcrnrlon = 124.6, urcrnrlat = 26,resolution = 'h', epsg = 3415)
map.drawmapboundary(fill_color = 'aqua')
map.fillcontinents(color = 'coral', lake_color = 'aqua')
map.drawcoastlines()
plt.show()

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap(llcrnrlon = 119.3, llcrnrlat = 20.7, urcrnrlon = 124.6, urcrnrlat = 26,
resolution = 'h', epsg = 3415)
map.drawmapboundary(fill_color = 'aqua')
map.fillcontinents(color = 'coral', lake_color = 'aqua')
map.drawcoastlines()
plt.show()

https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_TWN_shp.zip
!wget--no--check--certificate 'https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_TWN_shp.zip'-O temp.zip 2> /dev/null
def practice(request):
     map = Basemap(projection='merc' , 
                              resolution='i' , fix_aspect=True,
                              llcrnrlon=119.0 , llcrnlat=21.8,
                              urcrnlon=122.05 , urcrnrlat=25.4,
                              lat_ts =20)
import  folium
m = folium.Map((25.0133904,121.52245),zoom_start=14)
