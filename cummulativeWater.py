# load and plot atmo data


import sys
sys.path.append(r'W:\cms\green\red\user\tools\python\ossimutils') 
import readfiles

import numpy as np
import pandas as pd
import matplotlib as mpl
import pyradi.ryplot as ryplot

atmoFilename = './atmodata/atmoData.txt'
atmoData = readfiles.headtoDF(atmoFilename,skiplines=0)

# 100% absolute humidity as function of temperature
atmoData['AbsoluteHumidity'] = (1325.252/atmoData['Temperature[K]'])*np.power(10.,7.5892*(atmoData['Temperature[K]']-273.16)/(atmoData['Temperature[K]']-32.44))
# absolute humidity for the scenario [g/m3]
atmoData['AbsoluteHumidity'] *= atmoData['RH[%]']/100

# setup data to process

basePath = './'
theCase = 'rural23kmVIS'
theDict = {
    'july22-8h00-rh97': ['2009-07-22','08:00','96-56% at 0-3km, 2% at 4-5km', '9'],
    'july8-8h00-rh31' : ['2009-07-08','08:00','6% at 0km, 15-30% at 1-5km','8'],
    'march8-14h00-rh93': ['2009-03-08','14:00','87-98% at 0-2km, 55-16% at 3-5km','21'],
    'march10-14h00-rh25': ['2009-03-10','14:00','17-78% at 0-3km, 57-10% at 4-5km','39'],
    'march8-22h00-rh98': ['2009-03-08','22:00','99-72% at 0-3km, 38-73% at 4-5km','20'],
    'march5-22h00-rh45': ['2009-03-05','22:00','77% at 0km, 28-45% at 1-2km, 66-28 at 3-5km','22']
}
baseName = 'basic'

plotFrames = np.arange(0,1001,125)
plotFrames[0] += 1
numFramesProcessed = plotFrames.shape[0]

myPlotColours = ['b', 'g', 'r', 'c', 'm', 'y', 'k',
'#5D8AA8','#E52B50','#FF7E00','#9966CC','#66FF00','#8A3324',
'#008000','#FFDB58','#B2BEB5','#A1CAF1','#FE6F5E','#333399',
'#DE5D83','#800020','#1E4D2B','#00BFFF','#007BA7','#FFBCD9']

mpl.rc("savefig", dpi=300)
p = ryplot.Plotter(1,3,2,'Atmospheric Data',figsize=(14,18))
i = 0

for tp in theDict.keys():
    
    theDate = theDict[tp][0]
    theTime = theDict[tp][1]
    theData = atmoData[atmoData['Date']==theDate]
    theData = theData[theData['TimeOfDay']==theTime]
     
    theLabel = '{}, {}'.format(theDate,theTime)

###################################################################
#     p = ryplot.Plotter(1,3,2,'Atmospheric Data',figsize=(14,18))
    maxalt = int(np.max(theData['Altitude[m]'].values))
    alt = np.linspace(0,float(maxalt),maxalt+1)
    absprofile = np.interp(alt,theData['Altitude[m]'].values,theData['AbsoluteHumidity'].values)
    cumsum = np.cumsum(absprofile)

    p.plot(1,theData['Altitude[m]'].values/1000.,theData['Temperature[K]'].values-273.16,
            'Vertical temperature profile','Altitude [km]','Temperature [C]',
            plotCol=[myPlotColours[i]],label=[theLabel])
    p.plot(3,theData['Altitude[m]'].values/1000.,theData['RH[%]'].values,'Vertical relative humidity profile',
            'altitude [km]','Relative Humidity [%]',
            plotCol=[myPlotColours[i]],label=[theLabel])
    p.plot(2,theData['Altitude[m]'].values/1000.,theData['WindSpeed[m/s]'].values,
            'Vertical wind speed profile','altitude [km]','Wind speed [m/s]',
            plotCol=[myPlotColours[i]],label=[theLabel])
    p.plot(4,theData['Altitude[m]'].values/1000.,theData['AbsoluteHumidity'].values,
            'Vertical absolute humidity profile','altitude [km]','Absolute Humidity [g/m^3]',
            plotCol=[myPlotColours[i]],label=[theLabel])
    p.plot(5,alt/1000.,cumsum,'Cumulative water along path in square metre pipe','altitude [km]','Water along path [g/m^2]',
           plotCol=[myPlotColours[i]],label=[theLabel])
    p.plot(6,theData['Altitude[m]'].values/1000.,theData['Pressure[mBar]'].values,
            'Vertical pressure profile','altitude [km]','Pressure [mBar]',
            plotCol=[myPlotColours[i]],label=[theLabel])

####################################################################




    i = i + 1


pdfDoc = ryplot.PdfPages(basePath + 'atmosphere.pdf')
pdfDoc.savefig(p.getPlot(),dpi=300)
pdfDoc.close()
