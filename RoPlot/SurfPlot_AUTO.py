import numpy as np
import configparser
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
import sys
from matplotlib import rc
import glob
rc('text', usetex=True)													#use LaTeX

def main():
	print("3D/SurfacePlot plotting...")
	filename = GetData()
	filename = filename[2:]
	plotname = "SurfacePlot_"									
	plotname += filename
	#create savename for .png and .pdf
	plotname = plotname.replace(".txt", "").replace(".dat", "")
	Filter = filename[0]
	DoseFactor = GetDoseFactor(Filter)
	pdfname = "Plots/SurfacePlot/" + plotname + ".pdf"
	pngname = "Plots/SurfacePlot/" + plotname + ".png"

	a, b, current = np.loadtxt(filename, unpack=True, skiprows=1, usecols=(0, 1, 2))	#loadtxt
	#test: print(x[0], " ", y[0], " ", current[0])

	#get darkcurrent
	f = open(filename)
	A = f.readline()
	A = A.replace("xstep ystep diode current ","")
	darkcurrent = float(A)

	#calculate dose
	c = abs(current-darkcurrent)*DoseFactor
	
	y_plot_liste = list()
	x_plot_liste = list()
	z_plot_liste = list()
	Beamspot = GetBeamspot()
	xmin = Beamspot[0]
	xmax = Beamspot[1]
	ymin = Beamspot[2]
	ymax = Beamspot[3]
	
	for i in range(0,len(a)):
		if(a[i]>xmin and a[i]<xmax and b[i]>ymin and b[i]<ymax):
				y_plot_liste.append(b[i])
				x_plot_liste.append(a[i])
				z_plot_liste.append(c[i])

	x = np.asarray(x_plot_liste)
	y = np.asarray(y_plot_liste)
	z = np.asarray(z_plot_liste)


	#Plot
	y,x = x.astype(int), y.astype(int)
	maxX, maxY = max(x), max(y)
	width, height = maxX+1, maxY+1

	imdata = np.zeros((height, width))

	for i in range(len(x)):
			imdata[y[i], x[i]] = z[i]

	X, Y = np.meshgrid(np.arange(xmin, height), np.arange(ymin, width))
	Z = np.array([imdata[x, y] for x, y in zip(np.ravel(X), np.ravel(Y))])
	Z = Z.reshape(X.shape)

	fig = plt.figure()
	ax = fig.gca(projection='3d')

	surf = ax.plot_surface(X, Y, Z, cmap='hot', linewidth=0, rstride=1, cstride=1)

	clb = fig.colorbar(surf)
	clb.set_label(r"\textbf{Dose (Gy/h)}", size="10")
	ax.set_xlabel(r"\textbf{x Distance (mm)}", size="10")
	ax.set_ylabel(r'\textbf{y Distance (mm)}', size="10")
	ax.set_zlabel(r'\textbf{Dose (Gy/h)}', size="10")
	plt.title("3D Heatmap X-Ray", size="12")

	#Angle
	ax.view_init(35, -95)

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

if __name__=='__main__':
	main()
