"""
This creates a colour thematic map from single colour thematic map

Pick colours from anywhere, e.g.,  https://htmlcolorcodes.com/

neliswillers@gmail.com
"""

import numpy as np
import scipy
from scipy import ndimage
from numpy import ndarray
import imageio
import pylab
import skimage
from skimage.morphology import medial_axis
from scipy.interpolate import interp1d
from scipy import arange, array, exp
from scipy.interpolate import InterpolatedUnivariateSpline

thmapcol = {
0  :[   0,   0,   0 ],
8  :[  85, 217, 255 ],
16 :[ 150, 230, 133 ],
19 :[ 178, 209,  59 ],
20 :[ 191, 209,  59 ],
32 :[  96, 209,  59 ],
40 :[ 140, 188, 138 ],
48 :[ 244, 247, 178 ],
49 :[ 247, 231, 178 ],
50 :[ 212, 187, 155 ],
52 :[ 242, 169, 110 ],
56 :[ 147, 184, 195 ],
57 :[ 115, 148, 157 ],
80 :[ 254,  29,  29 ],
81 :[  79,  54, 180 ] ,
88 :[ 254, 124, 145 ],
91 :[ 124, 254, 246 ],
96 :[ 162, 124, 254 ],
104:[ 219, 219, 219 ],
128:[ 142, 142, 143 ],
160:[ 229, 124, 254 ],
200:[ 190, 254, 124 ],
}

def readParameters(pfilename):
    themes = []
    themenames = []
    number = 100000
    with open(pfilename,'r') as fin:
        lines = fin.readlines()
        counting = 0
        for line in lines:
            if counting > 0:
                themes.append(int(line.split()[0]))
                themenames.append(line.split()[6])
                counting += 1
            if 'number of defined classes' in line:
                number = int(line.split(' ')[0])
                counting = 1
            if counting > number:
                break
    return themes,themenames

#read image file, as grey scale
# img = ndimage.imread(filename, True)
filename = 'themap-Them.bmp'
pfilename = 'themap.parameters'
tfilename = filename.replace('.bmp','.png')
tfilename = tfilename.replace('-Them','-Colour')
cfilename = filename.replace('.bmp','-patch.png')

if tfilename == filename or cfilename == filename:
    print('check thematic image file type: expected *.bmp')
    exit()

theimg = imageio.imread(filename)
print(f'{filename} has size {theimg.shape}')

pthemes,themenames = readParameters(pfilename)
# print(f'Theme numbers in parameters file: \n{pthemes}')
# print(f'Theme theme names in parameters file: \n{themenames}')

themes = np.unique(theimg)
# print(f'Theme numbers in image: \n{themes}')

inParameters = True
for t in themes:
    if t not in pthemes:
        print('Theme {t} in bitmamp but not in parameter file')
        inParameters = False

inColours = True
for t in themes:
    if t not in thmapcol.keys():
        print('Theme {t} in bitmamp but not in colour set')
        inColours = False

if  inParameters == False or inColours==False:
    exit()

# make a new image same size as thematic map
colimg = np.ndarray((theimg.shape[0],theimg.shape[1],3),np.uint8)

for row in range(theimg.shape[0]):
    for col in range(theimg.shape[1]):
        colimg[row,col,:] = thmapcol[theimg[row,col]]

imageio.imwrite(tfilename,colimg)

