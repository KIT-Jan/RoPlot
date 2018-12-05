import configparser
import numpy as np
import matplotlib.pyplot as plt
import pylab as plb
from scipy.interpolate import griddata
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import sys
from scipy import optimize
from matplotlib import rc
rc('text', usetex=True)
import glob									

def main():
	print("2DGauss plotting...")
	filename = GetData()
	filename = filename[2:]
	plotname = "2DGauss_"									
	plotname += filename
	#create savename for .png and .pdf
	plotname = plotname.replace(".txt", "").replace(".dat", "")
	Filter = filename[0]
	DoseFactor = GetDoseFactor(Filter)
	pdfname = "Plots/Heatmap/2DGauss/" + plotname + ".pdf"
	pngname = "Plots/Heatmap/2DGauss/" + plotname + ".png"	
	
	x, y, current = np.loadtxt(filename, unpack=True, skiprows=1, usecols=(0, 1, 2))	#loadtxt
	
	#get darkcurrent
	f = open(filename)
	a = f.readline()
	a = a.replace("xstep ystep diode current ","")
	darkcurrent = float(a)
	
	#calculate dose
	z = abs(current-darkcurrent)*DoseFactor

	#Plot
	x,y = x.astype(int), y.astype(int)
	maxX, maxY = max(x), max(y)
	width, height = maxX+1, maxY+1
	
	data = np.zeros((height, width))
	
	for i in range(len(x)):
		data[y[i], x[i]] = z[i]
		
	params = fitgaussian(data)
	fit = gaussian(*params)

	plt.contour(fit(*np.indices(data.shape)), cmap='hot')
	ax = plt.gca()
	(height, x, y, width_x, width_y) = params
	
	plt.imshow(data, cmap='hot', interpolation='nearest')
	clb = plt.colorbar()
	plt.axis(GetBeamspotAxis())
	clb.set_label(r"\textbf{Dose (Gy/h)}", size="14")
	plt.xlabel(r"\textbf{x Distance (mm)}", size="14")
	plt.ylabel(r'\textbf{y Distance (mm)}', size="14")
	plt.title("Heatmap X-Ray Tube", size="18")
	plt.gcf()
	plt.savefig(pdfname, bbox_inches="tight")
	plt.savefig(pngname, bbox_inches="tight")
		
def gaussian(height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*np.exp(
                -(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)

def moments(data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution by calculating its
    moments """
    total = data.sum()
    X, Y = np.indices(data.shape)
    x = (X*data).sum()/total
    y = (Y*data).sum()/total
    col = data[:, int(y)]
    width_x = np.sqrt(np.abs((np.arange(col.size)-y)**2*col).sum()/col.sum())
    row = data[int(x), :]
    width_y = np.sqrt(np.abs((np.arange(row.size)-x)**2*row).sum()/row.sum())
    height = data.max()
    return height, x, y, width_x, width_y

def fitgaussian(data):
    """Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution found by a fit"""
    params = moments(data)
    errorfunction = lambda p: np.ravel(gaussian(*p)(*np.indices(data.shape)) -
                                 data)
    p, success = optimize.leastsq(errorfunction, params)
    return p
    
def GetDoseFactor(element):
	Config = configparser.ConfigParser()
	Config.read("PlotConfig.cfg")
	Factor = Config.getfloat("Dose", element)
	return Factor

def GetData():
	datfile = glob.glob("./*.dat")
	txtfile = glob.glob("./*.txt")
	if datfile!=[]:
		filename = datfile[0]
	elif txtfile!=[]:
		filename = txtfile[0]
	return filename
	
def GetBeamspotAxis():
	Config = configparser.ConfigParser()
	Config.read("PlotConfig.cfg")
	xmin = Config.getint("Beampspot","xmin")
	xmax = Config.getint("Beampspot","xmax")
	ymin = Config.getint("Beampspot","ymin")
	ymax = Config.getint("Beampspot","ymax")
	plotlist = [xmin,xmax,ymax,ymin]
	return plotlist
	



if __name__=='__main__':
	main()
