"""
This is an example of how to digitize a (x,y) graph

Get a bitmap of the graph (scan or screencapture)
Take care to not rotate the graph (x and y axes must be horizontal/vertical).
The current version of the software does not work with rotated images.
Bitmap edit the graph. Clean the graph to the maximum extent possible,
by removing all the clutter
Cut only the central block that contains the graph box, by deleting
the x and y axes notation and other clutter. You must end up with nothing
in the image except the line you want to digitize.
Also the graph box must be cut out such that the x and y axes min and max
correspond exactly with the edges of the bitmap.

The current version does not properly handle vertical lines, i.e., where
different yvalues apply to the same xvalue.

This code requires a number of non-standard python packages:
numpy & scipy, pylab,
PIL - easy_install PIL
skimage - easy_install skimage or see  http://scikit-image.org/

neliswillers@gmail.com
"""

import numpy as np
import scipy
from scipy import ndimage
import imageio
import pylab
import skimage
from skimage.morphology import medial_axis
from scipy.interpolate import interp1d
from scipy import arange, array, exp
from scipy.interpolate import InterpolatedUnivariateSpline

# def extrap1d(interpolator):
#     xs = interpolator.x
#     ys = interpolator.y

#     def pointwise(x):
#         if x < xs[0]:
#             return ys[0]+(x-xs[0])*(ys[1]-ys[0])/(xs[1]-xs[0])
#         elif x > xs[-1]:
#             return ys[-1]+(x-xs[-1])*(ys[-1]-ys[-2])/(xs[-1]-xs[-2])
#         else:
#             return interpolator(x)

#     def ufunclike(xs):
#         return array(map(pointwise, array(xs)))

#     return ufunclike


def find_runs(x):
    """Find runs of consecutive items in an array."""

    # ensure array
    x = np.asanyarray(x)
    if x.ndim != 1:
        raise ValueError('only 1D array supported')
    n = x.shape[0]

    # handle empty array
    if n == 0:
        return np.array([]), np.array([]), np.array([])

    else:
        # find run starts
        loc_run_start = np.empty(n, dtype=bool)
        loc_run_start[0] = True
        np.not_equal(x[:-1], x[1:], out=loc_run_start[1:])
        run_starts = np.nonzero(loc_run_start)[0]

        # find run values
        run_values = x[loc_run_start]

        # find run lengths
        run_lengths = np.diff(np.append(run_starts, n))

        return run_values, run_starts, run_lengths


def extractGraph(filename, xmin, xmax, ymin, ymax, outfile="",doPlot=False,
        xaxisLog=False, yaxisLog=False,numXVal=100,IntPHead = None,skipYRuns=False,
        threshold=0.5):
    """
    This function processes an image, calculate the location, and scale the
    (r,c) or (x,y) values of pixels with non-zero values. This can be used
    to scan a graph to text values.

    Args:
        | filename: name of the image file
        | xmin: the value corresponding to the left side (column=0)
        | xmax: the value corresponding to the right side (column=max)
        | ymin: the value corresponding to the bottom side (row=bottom)
        | ymax: the value corresponding to the top side (row=top)
        | outfile: write the sampled points to this output file
        | doPlot: plot the digitised graph for visual validation
        | xaxisLog: x-axis is in log10 scale (min max are log values)
        | yaxisLog: y-axis is in log10 scale (min max are log values)
        | numXVal: number of v values required (int)
        | IntPHead: OSSIM 1D interpolation table header (str)
        | skipYRuns: = do not repeat duplicate runs of y values (bool)
        | threshold: = percentage of spread (double)

    Returns:
        | xval: the sampled and scaled x-values
        | yval: the sampled and scaled y-values
        | side effect: a file may be written
        | side effect: a graph may be displayed
    """

    #read image file, as grey scale
    # img = ndimage.imread(filename, True)
    img = imageio.imread(filename)
    img = img[:,:,0]
    print(img.shape)

    # find threshold up the way
    threslevel = img.min() + threshold *(img.max()-img.min()) 
    # form binary image by thresholding
    img = img < threslevel
    #find the skeleton one pixel wide
    imgskel = medial_axis(img)
    # pylab.imshow(imgskel)
    # pylab.gray()
    # pylab.show()

    # set up indices arrays to get x and y indices
    ind = np.indices(img.shape)

    #skeletonise the graph to one pixel only
    #then get the y pixel value, using indices
    yval = ind[0,...] * imgskel.astype(float)
    # pylab.imshow(yval>0)
    # pylab.gray()
    # pylab.show()
    # invert y-axis origin from left top to left bottom
    yval = yval.shape[0] - np.max(yval, axis=0)
    #get indices for only the pixels where we have data
    wantedIdx = np.where(np.sum(imgskel, axis = 0) > 0)

    # convert to original graph coordinates
    cvec = np.arange(0.0,img.shape[1])
    xval = xmin + (cvec[wantedIdx] / img.shape[1]) * (xmax - xmin)
    yval = ymin + (yval[wantedIdx] / img.shape[0]) * (ymax - ymin)
    if xaxisLog:
        xval = 10 ** xval
    else:
        xval = xval
    if yaxisLog:
        yval = 10 ** yval
    else:
        yval = yval

    #process and write output file
    if len(outfile) > 0 :
        if skipYRuns:
            # find runs of duplicate y-values, don't repeat inside the run
            run_values, run_starts, run_lengths = find_runs(yval.reshape(-1,))
            outX = xval[run_starts]
            outY = yval[run_starts]
        else:
            outX = xval
            outY = yval

        # interpolate to get the required number of values
        # do inter/extrapolation
        sinter = InterpolatedUnivariateSpline(outX, outY, k=1)

        # new values for outX and outY
        outX = np.linspace(xmin,xmax,numXVal)
        outY = sinter(outX)

        # form the output array
        oarray = np.hstack((outX.reshape(-1,1),outY.reshape(-1,1)))

        if IntPHead is None:
            np.savetxt(outfile,oarray)
        else:
            with open(outfile, 'wb') as fout:
                dstr = '0 infty'
                fout.write('{}\n'.format(IntPHead).encode())
                fout.write('{}\n'.format(dstr).encode())
                fout.write('{}\n'.format(dstr).encode())
                np.savetxt(fout, oarray,fmt='%.12e')

        if doPlot:
            if xaxisLog and yaxisLog:
                pylab.plot(np.log10(outX),np.log10(outY))
            if not xaxisLog and yaxisLog:
                pylab.plot(outX,np.log10(outY))
            if xaxisLog and not yaxisLog:
                pylab.plot(np.log10(outX),outY)
            else:
                pylab.plot(outX,outY)
            pylab.show()

    return outX, outY


xval,yval = extractGraph('kline-csir-asd-grass.png', 0.3452, 1.7, -0.1, 0.7,'kline-csir-asd-grass.txt',
         True,numXVal=200,IntPHead='wavelength radiance',skipYRuns=True,threshold=0.3)




