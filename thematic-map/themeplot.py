"""This creates a colour thematic map from single colour thematic map
Pick colours from anywhere, e.g.,  https://htmlcolorcodes.com/
neliswillers@gmail.com
"""

import numpy as np
# from numpy import ndarray
import imageio
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

import pyradi.ryfiles as ryfiles


thmapcol = {
0  :[ 255, 255, 255 ],
8  :[   0, 205, 255 ],
9  :[ 174, 214, 241 ],
16 :[ 150, 230, 133 ],
17 :[ 118, 215, 196 ],
18 :[  30, 132,  73 ],
19 :[ 178, 209,  59 ],
20 :[ 209, 211, 118 ],
21 :[  26, 188, 156 ],
24 :[ 171, 235, 198 ],
26 :[  53, 104,  90 ],
32 :[  63, 196,  63 ],
33 :[ 213, 245, 227 ],
34 :[  89, 172, 118 ],
40 :[   0, 126,   0 ],
41 :[  20, 143, 119 ],
42 :[  46, 204, 113 ],
43 :[  14,  98,  81 ],
48 :[ 244, 247, 178 ],
49 :[ 126,  78,  43 ],
50 :[ 212, 187, 155 ],
51 :[ 247, 220, 111 ],
52 :[ 242, 169, 110 ],
53 :[ 110,  44,   0 ],
56 :[ 147, 184, 195 ],
57 :[ 115, 148, 157 ],
64 :[ 229, 231, 233 ],
72 :[ 250, 219, 216 ],
73: [ 245, 203, 167 ],
80 :[ 254,  29,  29 ],
81 :[  79,  54, 180 ],
88 :[ 254, 124, 145 ],
89 :[ 187, 143, 206 ],
90 :[ 108,  52, 131 ],
91 :[ 124, 254, 246 ],
96 :[ 162, 124, 254 ],
97 :[ 232, 218, 239 ],
104:[ 219, 219, 219 ],
105:[ 128, 139, 150 ],
106:[  88,  88, 100 ],
107:[ 121, 125, 127 ],
108:[  95, 106, 106 ],
112:[  23,  32,  42 ],
120:[ 135,  54,   0 ],
121:[ 156, 100,  12 ],
128:[  40, 180 , 99 ],
129:[  88, 214, 141 ],
130:[  27, 180, 155 ],
131:[  17, 122, 101 ],
133:[ 162, 217, 206 ],
136:[  24, 106,  59 ],
144:[  88, 214, 100 ],
145:[  80, 180,  99 ],
152:[ 217, 136, 128 ],
153:[ 236, 112,  99 ],
160:[ 250, 198, 216 ],
168:[ 160,  64,   0 ],
176:[ 252, 243, 207 ],
184:[ 212, 172,  13 ],
192:[ 104,  73,  53 ],
216:[  46,  64,  83 ] ,
200:[ 190, 254, 124 ],
224:[ 250, 215, 160 ],
}

# check for duplicates
dicDCheck = {}
lstDoubles = []
for key in thmapcol.keys():
    if tuple(thmapcol[key]) in dicDCheck.keys():
        lstDoubles.append([
            key,
            dicDCheck[tuple(thmapcol[key])],
            thmapcol[key],
            ])
    else:
        dicDCheck[tuple(thmapcol[key])] = key
if len(lstDoubles)>0:
    print('The following colours are duplicates in the colour map:')
    for item in lstDoubles:
        print(item)
else:
    print('There are no duplicates in the colour map')
print(' ')

#convert to unity values
thmapcolN = {}
for key in thmapcol.keys():
    # thmapcolN.append([{key:i/255. for i in thmapcol[key]})
    thmapcolN[key] = [i/255. for i in thmapcol[key]]

#################################################################

def readParameters(pfilename):
    """Read the theme numbers and names from data file
    """
    pthemes = {}
    number = 100000
    with open(pfilename,'r') as fin:
        lines = fin.readlines()
        counting = 0
        for line in lines:
            if counting > 0:
                pthemes[int(line.split()[0])] = line.split()[6]
                counting += 1
            if 'number of defined classes' in line:
                number = int(line.split(' ')[0])
                counting = 1
            if counting > number:
                break
    return pthemes


#################################################################
# to see a plan view of the target area
def plotTheColmap(thmapcol,thmapcolN,pfilename):
    """
    """
    mapfilename = pfilename.replace('.parameters','-cmap.png')
    if mapfilename == pfilename :
        print('check thematic parameters file type: expected *.bmp')
        exit()

    pthemes = readParameters(pfilename)
    numgrid = int(np.sqrt(len(thmapcolN.keys()))+1)

    blocksize = 1.
    fig = plt.figure(figsize=(10,10), dpi=150,)
    ax = fig.add_subplot(1, 1, 1)
    for ik,key in enumerate(pthemes.keys()):
        x = ik % numgrid
        y = (ik - ik % numgrid) / numgrid

        p = Rectangle((blocksize*x ,blocksize*y), blocksize,blocksize,color=thmapcolN[key],alpha=1)
        ax.add_patch(p)        

        ax.text(x+blocksize/2, y+(0.5 + 0.2) * blocksize, f'{key}',horizontalalignment='center',fontsize=7)
        ax.text(x+blocksize/2, y+(0.5) * blocksize, f'{pthemes[key]}',horizontalalignment='center',fontsize=7)
        ax.text(x+blocksize/2, y+(0.5-0.2) * blocksize, f'{thmapcol[key]}',horizontalalignment='center',fontsize=7)

    ax.set_xlim(0,numgrid*blocksize)
    ax.set_ylim(0,numgrid*blocksize)
    plt.savefig(mapfilename,dpi=300)


#################################################################
def makeColourImg(thmapcol,filename,pfilename, scaledown=1):

    theimgT = imageio.imread(filename)
    print(f'{filename} has size {theimgT.shape}')
    if scaledown != 1:
        print(f'****  Scaling down, using only every {scaledown}th pixel!')
        theimg = theimgT[::scaledown,::scaledown].copy()
        print(f'{filename} has new size {theimg.shape}')
        strScale = f'-scaled({scaledown})'
    else:
        theimg = theimgT
        strScale = ''

    tfilename = filename.replace('.bmp',f'{strScale}.png')
    tfilename = tfilename.replace('-Them','-Colour')

    if tfilename == filename:
        print('check thematic image file type: expected *.bmp')
        exit()

    pthemes = readParameters(pfilename)

    themes = np.unique(theimg)

    inParameters = True
    for t in themes:
        if t not in pthemes.keys():
            print(f'Theme {t} in bitmamp but not in parameter file')
            inParameters = False

    inColours = True
    for t in themes:
        if t not in  thmapcol.keys():
            print(f'Theme {t} in bitmamp but not in colour set')
            inColours = False

    if  inParameters == False or inColours==False:
        exit()

    # make a new image same size as thematic map
    colimg = np.ndarray((theimg.shape[0],theimg.shape[1],3),np.uint8)

    for row in range(theimg.shape[0]):
        for col in range(theimg.shape[1]):
            colimg[row,col,:] =  thmapcol[theimg[row,col]]

    imageio.imwrite(tfilename,colimg)

#################################################################
scaledown = 1

filenames = ryfiles.listFiles('.','.*Them.*\.bmp',1,0,True)
pfilenames = ryfiles.listFiles('.','*.parameters',1,0,False)

dicPathsThem = {os.path.dirname(path):os.path.basename(path) for path in filenames }
dicPathsParas = {os.path.dirname(path):os.path.basename(path) for path in pfilenames }

print('Found these thematic maps:')
for thempath in filenames:
    print(thempath)
print(' ')

for key in dicPathsThem:
    makeColourImg(thmapcol,filename=os.path.join(key,dicPathsThem[key]),
            pfilename=os.path.join(key,dicPathsParas[key]),scaledown=scaledown)
    plotTheColmap(thmapcol,thmapcolN,pfilename=os.path.join(key,dicPathsParas[key]))
