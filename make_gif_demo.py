import numpy as np
import matplotlib.pyplot as plt
import os
import imageio

from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1 import make_axes_locatable

plt.rcParams['ps.fonttype'] = 42
plt.rcParams['pdf.fonttype'] = 42

#%% read data

filename = '..\Raw_data\data_15-03-2022-10-59-57_analyzed.npz'

images = np.load(filename)

data_raw = images['data']
Open_data = np.sum(data_raw, axis = 3)[:, 6:-6, 6:-6]

sz = Open_data.shape

#%% Gif parameters

path = '.\Gifs'

try:
    os.mkdir(path)
except:
    pass

pxsize_x = 30/512 #um
pxsize_z = 12/30 #um

FPS = 2

start = 0
end = sz[0]

#%% Create gif

filenames = []
figures = []

Stack = Open_data

# Save files
for i in range(start,end):
    # plot the line chart
    fig, ax = plt.subplots()
    im = ax.imshow( Stack[i,:,:], cmap = 'hot' )
    ax.axis('off')
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = fig.colorbar(im, cax=cax, ticks = np.floor( [np.min(Stack[i,:,:]), np.max(Stack[i,:,:])] ), )
    ax.text(1.1,0.4, r'Counts / 50 $\mu s$',rotation=90, transform=ax.transAxes)
    
    depth = pxsize_z*i
    ax.text(0.75,0.05, f'z = {depth:.1f} $\mu m$', color = 'white', transform=ax.transAxes)
    
    scalebar = ScaleBar(
    pxsize_x, "um", # default, extent is calibrated in meters
    box_alpha=0,
    color='w',
    length_fraction=0.25)
    
    ax.add_artist(scalebar)
    
    figures.append(fig)
    
    # create file name and append it to a list
    filename = f'{path}\{i}.tif'
    filenames.append(filename)
    
    # save frame
    plt.savefig(filename)
    plt.close()

# Build gif
with imageio.get_writer(path + '\Open_data.gif', mode='I', fps = FPS) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
        
# Remove files
for filename in set(filenames):
    os.remove(filename)