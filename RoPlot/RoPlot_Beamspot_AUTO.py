import numpy as np
import configparser
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import sys
from matplotlib import rc
import glob	
rc('text', usetex=True)													#use LaTeX

def main():
	filename = GetData()
	filename = filename[2:]
	plotname = "Heatmap_"									
	plotname += filename
	#create savename for .png and .pdf
	plotname = plotname.replace(".txt", "").replace(".dat", "")
	Filter = filename[0]
	DoseFactor = GetDoseFactor(Filter)
	threshold = GetThreshold()
	pdfname = "Plots/Heatmap/" + plotname + ".pdf"
	pngname = "Plots/Heatmap/" + plotname + ".png"								
	
	x, y, current = np.loadtxt(filename, unpack=True, skiprows=1, usecols=(0, 1, 2))	#loadtxt
	#test: print(x[0], " ", y[0], " ", current[0])
	
	#get darkcurrent
	f = open(filename)
	a = f.readline()
	a = a.replace("xstep ystep diode current ","")
	darkcurrent = (float(a))
	
	#calculate dose
	z = abs(current-darkcurrent)*DoseFactor
	list_for_mean = []
	threshold *= np.max(z)
	print("max(z): " + str(max(z)) + " Gy/h")
	for i in z:
		if i >= threshold:
			list_for_mean.append(i)
	mean = np.mean(list_for_mean)
	print("mean dose: " + str(mean) + " Gy/h")
	
	#Plot
	x,y = x.astype(int), y.astype(int)
	maxX, maxY = max(x), max(y)
	width, height = maxX+1, maxY+1
	
	imdata = np.zeros((height, width))
	
	for i in range(len(x)):
		imdata[y[i], x[i]] = z[i]
		
	plt.imshow(imdata, cmap='hot', interpolation='nearest')
	clb = plt.colorbar()
	plt.axis(GetBeamspotAxis())
	clb.set_label(r"\textbf{Dose (Gy/h)}", size="14")
	plt.xlabel(r"\textbf{x Distance (mm)}", size="14")
	plt.ylabel(r'\textbf{y Distance (mm)}', size="14")
	plt.title("Heatmap X-Ray Tube", size="18")
	plt.gcf()
	plt.savefig(pdfname, bbox_inches="tight")
	plt.savefig(pngname, bbox_inches="tight")
	
def GetBeamspotAxis():
	Config = configparser.ConfigParser()
	Config.read("PlotConfig.cfg")
	xmin = Config.getint("Beampspot","xmin")
	xmax = Config.getint("Beampspot","xmax")
	ymin = Config.getint("Beampspot","ymin")
	ymax = Config.getint("Beampspot","ymax")
	plotlist = [xmin,xmax,ymax,ymin]
	return plotlist
	
def GetData():
	datfile = glob.glob("./*.dat")
	txtfile = glob.glob("./*.txt")
	if datfile!=[]:
		filename = datfile[0]
	elif txtfile!=[]:
		filename = txtfile[0]
	return filename

def GetDoseFactor(element):
	Config = configparser.ConfigParser()
	Config.read("PlotConfig.cfg")
	Factor = Config.getfloat("Dose",element)
	return Factor
	
def GetThreshold():
	Config = configparser.ConfigParser()
	Config.read("PlotConfig.cfg")
	threshold = Config.getfloat("Dose","threshold")
	return threshold
	
	
if __name__=='__main__':
	main()
