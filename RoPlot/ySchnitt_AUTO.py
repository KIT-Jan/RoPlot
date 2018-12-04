import numpy as np
import configparser
import matplotlib.pyplot as plt
import pylab as plb
from scipy.interpolate import griddata
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import sys
from scipy import optimize
from matplotlib import rc
import glob	
rc('text', usetex=True)													#use LaTeX


def main():
	filename = GetData()
	filename = filename[2:]
	plotname = "yCut"									
	plotname += filename
	#create savename for .png and .pdf
	plotname = plotname.replace(".txt", "").replace(".dat", "")
	Filter = filename[0]
	DoseFactor = GetDoseFactor(Filter)
	pdfname = "Plots/Cuts/yCut/" + plotname + ".pdf"
	pngname = "Plots/Cuts/yCut/" + plotname + ".png"
	
	x, y, current = np.loadtxt(filename, unpack=True, skiprows=1, usecols=(0, 1, 2))	#loadtxt
	
	#get darkcurrent
	f = open(filename)
	a = f.readline()
	a = a.replace("xstep ystep diode current ","")
	darkcurrent = float(a)
	
	#calculate dose
	z = abs(current-darkcurrent)*DoseFactor
	

	y_plot_liste = list()
	x_plot_liste = list()
	Beamspot = GetBeamspot()
	xmin = Beamspot[0]
	xmax = Beamspot[1]
	yCut = GetyCut()

	for i in range(0,len(x)):
		if(y[i]==yCut):
			if x[i]>xmin and x[i]<xmax:	
				y_plot_liste.append(z[i])
				x_plot_liste.append(x[i])
	
	x_plot = np.asarray(x_plot_liste)
	y_plot = np.asarray(y_plot_liste)
	
	plt.plot(x_plot, y_plot,"r.-")
	plt.xlabel(r"\textbf{x Distance (mm)}", size="14")
	plt.ylabel(r'\textbf{Dose (Gy/h)}', size="14")
	plt.grid(True)
	plt.title("Cut through y={0}mm".format(str(yCut)), size="18")
	plt.gcf()
	plt.savefig(pdfname, bbox_inches="tight")
	plt.savefig(pngname, bbox_inches="tight")
	
def GetDoseFactor(element):
	Config = configparser.ConfigParser()
	Config.read("PlotConfig.cfg")
	Factor = Config.getfloat("Dose",element)
	return Factor

def GetData():
	datfile = glob.glob("./*.dat")
	txtfile = glob.glob("./*.txt")
	if datfile!=[]:
		filename = datfile[0]
	elif txtfile!=[]:
		filename = txtfile[0]
	return filename
	
def GetBeamspot():
	Config = configparser.ConfigParser()
	Config.read("PlotConfig.cfg")
	xmin = Config.getint("Beampspot","xmin")
	xmax = Config.getint("Beampspot","xmax")
	ymin = Config.getint("Beampspot","ymin")
	ymax = Config.getint("Beampspot","ymax")
	plotlist = [xmin,xmax,ymin,ymax]
	return plotlist
	
def GetyCut():
	Config = configparser.ConfigParser()
	Config.read("PlotConfig.cfg")
	yCut = Config.getint("yCut","y")
	return yCut
	
if __name__=='__main__':
	main()
