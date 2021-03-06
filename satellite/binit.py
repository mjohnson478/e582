#updated 2012/Nov/02
from __future__ import division
#see http://pysclint.sourceforge.net/pyhdf/
import pyhdf.SD
import numpy as np
import matplotlib.pyplot as plt
import glob, sys

def progress(datanum,tot_loops):
    """
       print a message about percent complete
       input:      datanum: current index (int)
       tot_loops:  index when loop finishes
    """   
    the_frac=np.int(datanum/tot_loops*100.)
    sys.stdout.write("\rpercent complete: %d%%" % the_frac)
    sys.stdout.flush()


class binit(object):
    """histograms a vector of data, returning the bin index of every
       datapoint

       Constructor
       -----------

          bin_obj=binit(minval,maxval,numbins,
                         missingLowValue,missingHighValue)

        Parameters
        ----------

         minval: float
            left edge of smallest bin
         maxval: float
            right edge of largest bin
         numbins: int
            number of bins
         missingLowValue: float
            bin number indicating data is smaller than minval
         missingHighValue: float
            bin number indicating data is larger than maxval
                         
    """
    def __init__(self,minval,maxval,numbins,missingLowValue,missingHighValue):
        self.missingLowValue=missingLowValue
        self.missingHighValue=missingHighValue
        self.minval=minval
        self.maxval=maxval
        self.numbins=numbins
        self.binsize=(maxval-minval)/numbins
        self.bin_edges=np.arange(minval,maxval + 0.5*self.binsize,self.binsize)
        self.bin_centers= (self.bin_edges[:-1] + self.bin_edges[1:])/2.

    def do_bins(self,data_vec):
        """
           bin the items in data_vec into self.numbins
           see binit docstring for details

           parameters
           ----------

              data_vec: numpy 1d array (float)
                 vector of floating point numbers to be binned

           returns:
           --------
             bin_count: numpy vector of length self.numbins (int)
                vector containing bin counts
             
             bin_index: numpy vector of len(data_vec)
                vector containing the bin number of each datapoint

             lowcount: int
                number of points that were smaller
                than the smallest bin
                
             highcount: int
                number of points that were larger than the largest
                bin

           example
           -------
             
             (bin_count,bin_index,lowcount,hightcount)=obj.do_bins(lat_vec) 
        """   
        bin_index=np.empty_like(data_vec,dtype=np.int)
        bin_count=np.zeros([self.numbins],dtype=np.int)
        lowcount=0
        highcount=0
        tot_loops=len(data_vec)
        for datanum,dataval in enumerate(data_vec):
            if np.mod(datanum,10000)==0:
                progress(datanum,tot_loops)
            float_bin =  ((dataval - self.minval) /self.binsize)
            if float_bin < 0:
                lowcount+=1
                bin_index[datanum]=self.missingLowValue
                continue
            if float_bin > self.numbins:
                highcount += 1
                bin_index[datanum] = self.missingHighValue
                continue
            ibin=int(float_bin)
            bin_count[ibin]+=1
            bin_index[datanum]=ibin
        return (bin_count,bin_index,lowcount,highcount)

    def get_centers(self):
        """
          Get the bin centers for the historgram
        """
        return self.bin_centers

    def get_edges(self):
        """
          Get the bin edges for the historgram
        """
        return self.bin_edges
    
if __name__=="__main__":
    #
    # limits set for MOD03.A2006275.0440.005.2010182222019.hdf
    #
    #get the name of files ending in hdf
    the_files=glob.glob('MOD03*275*hdf')
    #take the first one (only one file fits this description)
    the_file=the_files[0]
    print the_file
    
    #get the full latitude and longitude arrays
    sdgeom=pyhdf.SD.SD(the_file)
    fullLats=sdgeom.select('Latitude')
    fullLats=fullLats.get()
    fullLons=sdgeom.select('Longitude')
    fullLons=fullLons.get()
    max_x=200
    max_y=300
    partLats=fullLats[:max_x,:max_y]
    partLons=fullLons[:max_x,:max_y]
    sdgeom.end()

    #plot the latitdue and longitude of every pixel
    #for a small part of the scene
    fig1,axis1=plt.subplots(1,1)
    axis1.plot(partLons,partLats,'b+',markersize=10)
    axis1.set_ylabel('latitude (deg North)')
    axis1.set_xlabel('longitude (deg East)')
    axis1.set_title('partial scene pixel map')
    
    #plot the latitdue and longitude of every pixel
    #for a small part of the scene
    fig1,axis1=plt.subplots(1,1)
    axis1.plot(partLons,partLats,'b+',markersize=10)
    axis1.set_ylabel('latitude (deg North)')
    axis1.set_xlabel('longitude (deg East)')

    #
    # put on a grid
    #
    regLons=np.arange(-82,-81,0.05)
    regLats=np.arange(-28,-27,0.05)
    lonMat,latMat=np.meshgrid(regLons,regLats)
    axis1.plot(lonMat,latMat,'r.',markersize=8)
    axis1.set_title('regular grid (red) and pixel map (blue)')
    #axis1.set_xlim([-82,-81])
    #axis1.set_ylim([-28.,-27])
    fig1.savefig('meshgrid.png')

    #
    #  now zoom the axis limits
    #
    fig2,axis2=plt.subplots(1,1)
    axis2.plot(partLons,partLats,'b+',markersize=10)
    axis2.set_ylabel('latitude (deg North)')
    axis2.set_xlabel('longitude (deg East)')
    axis2.plot(lonMat,latMat,'r.',markersize=8)
    axis2.set_xlim([-82,-81.5])
    axis2.set_ylim([-28,-27.5])
    axis2.set_title('zoomed overlay')
    fig2.savefig('meshgrid_small.png')

    numbins=20
    bin_lats=binit(-28,-27,numbins,-999,-888)
    bin_lons=binit(-82,-81,numbins,-999,-888)
    
    lat_count,lat_index,lowlats,highlats=bin_lats.do_bins(partLats.ravel())    

    plt.show()


