#!/bin/bash

if [ -d Plots ]
	then
		echo "Verzeichnisse existieren bereits und werden nicht neu angelegt"
	else 
		mkdir Plots
		mkdir Plots/Heatmap
		mkdir Plots/Heatmap/2DGauss
		mkdir Plots/Cuts
		mkdir Plots/Cuts/xCut
		mkdir Plots/Cuts/yCut
		mkdir Plots/SurfacePlot
		echo "Verzeichnisse erstellt"
fi
echo "Start plotting"
python 2DGauss_Beamspot_AUTO.py
python RoPlot_Beamspot_AUTO.py
python xSchnitt_AUTO.py
python ySchnitt_AUTO.py
python SurfPlot_AUTO.py
