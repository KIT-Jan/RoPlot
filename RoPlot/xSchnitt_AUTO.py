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
	print("xCut plotting...")
	filename = GetData()
	filename = filename[2:]
	plotname = "xCut_"									
	plotname += filename
	#create savename for .png and .pdf
	plotname = plotname.replace(".txt", "").replace(".dat", "")
	Filter = filename[0]
	DoseFactor = GetDoseFactor(Filter)
	pdfname = "Plots/Cuts/xCut/" + plotname + ".pdf"
	pngname = "Plots/Cuts/xCut/" + plotname + ".png"	
	
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
	ymin = Beamspot[2]
	ymax = Beamspot[3]
	xCut = GetxCut()
	
	for i in range(0,len(x)):
		if(x[i]==xCut):
			if y[i]>ymin and y[i]<ymax:	
				y_plot_liste.append(z[i])
				x_plot_liste.append(y[i])
	
	x_plot = np.asarray(x_plot_liste)
	y_plot = np.asarray(y_plot_liste)
	
	plt.plot(x_plot, y_plot,"r.-")
	plt.xlabel(r"\textbf{y Distance (mm)}", size="14")
	plt.ylabel(r'\textbf{Dose (Gy/h)}', size="14")
	plt.grid(True)
	plt.title("Cut through x={0}mm".format(str(xCut)), size="18")
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
	
def GetxCut():
	Config = configparser.ConfigParser()
	Config.read("PlotConfig.cfg")
	xCut = Config.getint("xCut","x")
	return xCut
	
if __name__=='__main__':
	main()
