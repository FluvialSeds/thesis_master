'''
Script to plot Conclusion figure
'''

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#set plotting defaults
mpl.rcParams['mathtext.default']='regular' #math text font
mpl.rcParams['axes.linewidth'] = 0.5 #bounding box line width
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['legend.fontsize'] = 8
mpl.rcParams['axes.labelsize'] = 8
mpl.rcParams['axes.edgecolor'] = 'k'
mpl.rcParams['axes.facecolor'] = 'none'
mpl.rcParams['font.weight'] = 'light'


#make function to calc net
def net_co2(lYtss,be,fox):
	'''
	Calculates the theoretical net CO2 sink/source using Valier's yield curves
	and my fraction oxidized

	Parameters
	----------
	lYtss: log10 TSS yield (tkm-2y-1)
	be: burial efficiency, in fractoin
	fox: fraction of OCpetro oxidized

	Returns
	-------
	Fco2: flux of CO2 (tkm-2y-1)
	'''

	#calculate bio and petro yields (Galy et al., 2015)
	lYp = np.log10(0.0007) + 1.11*lYtss
	lYb = np.log10(0.081) + 0.56*lYtss
	Yp = 10**lYp #(tCkm-2y-1)
	Yb = 10**lYb #(tCkm-2y-1)

	#calculate burial sink, oxid source
	so_p = (fox/(1-fox))*Yp
	si_b = be*Yb

	#calculate net
	Fco2 = so_p - si_b

	return Fco2

# make plot
fig, ax = plt.subplots(1,1,figsize = (4.5,4))

## Case 1: fox = 0.15, .03 < be < 1
lYtss = np.linspace(0,6,100)

F_be3 = net_co2(lYtss,0.3,0.15)
F_be1 = net_co2(lYtss,1,0.15)

ax.fill_between(
	lYtss,
	F_be3,
	F_be1,
	facecolor = [0.05,0.45,0.70],
	alpha = 0.3,
	label = r'unweathered $OC_{petro}$ export ($\mathit{f}_{ox} = 0.15)$')

## Case 2: fox = 0.0.73, .03 < be < 1
lYtss = np.linspace(0,6,100)

F_be3 = net_co2(lYtss,0.3,0.73)
F_be1 = net_co2(lYtss,1,0.73)

ax.fill_between(
	lYtss,
	F_be3,
	F_be1,
	facecolor = [0.73,0.05,0],
	alpha = 0.3,
	label = r'residual $OC_{petro}$ export ($\mathit{f}_{ox} = 0.73)$')

#add line at zero and dashed vertical lines
ax.plot(
	[0,6],
	[0,0],
	'k',
	linewidth = 1.5)

ax.plot(
	[2,2],
	[-10,10],
	'--k',
	linewidth = 1)

ax.plot(
	[3.5,3.5],
	[-10,10],
	'--k',
	linewidth = 1)

#add legend and axis labels
ax.legend(loc='lower left',framealpha=0.0,scatterpoints=1)

#set axis labels
ax.set_xlabel(r'$\log (Y_{TSS})$ $(t km^{-2} yr^{-1})$')
ax.set_ylabel(r'net $CO_{2}$ flux $(t km^{-2} yr^{-1})$')

#set axis limits
ax.set_ylim([-3,3])
ax.set_xlim([0,5.5])

#add passive margin text
l1 = r'passive margin'
l2 = r'low elevation'
l3 = r'$\geq 5-6 \times 10^{10}$ $km^2$'
l4 = r'$\log (Y_{TSS}) \leq 2.5$'

pmt = l1 + '\n' + l2 + '\n' + l3 + '\n' + l4

ax.text(1,2.75,pmt,
	fontsize=8,
	horizontalalignment='center',
	verticalalignment='top')

#add active margin text
l1 = r'active margin'
l2 = r'high elevation'
l3 = r'$\leq 3 \times 10^{10}$ $km^2$'
l4 = r'$\log (Y_{TSS}) \geq 4$'

pmt = l1 + '\n' + l2 + '\n' + l3 + '\n' + l4

ax.text(4.5,2.75,pmt,
	fontsize=8,
	horizontalalignment='center',
	verticalalignment='top')


plt.tight_layout()
plt.show()

#save figure
fig.savefig('conclusion_net_flux.pdf',
	dpi=300,
	transparent=True,
	frameon=False)

