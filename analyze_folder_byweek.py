# rldw 04/04/15
# https://github.com/rldw
#
# DESCRIPTION:
# - gets unix timestamp from filenames in indir
#	 generated by detect_faces.py script
# - generates a stacked bar chart plotting info for every week
#
# USAGE:
# python analyze_folder_byweek.py
# -i --indir	older with images generated by detect_faces.py script
# -o --outfile if set graph will be saved to file, e.g. pdf or png

import os, datetime, argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# parse command line arguments
parser = argparse.ArgumentParser(description='Creates bar chart from image filenames, plotting info for every weekd')
parser.add_argument('-i','--indir', required=True,
	help='folder with images generated by detect_faces.py script')
parser.add_argument('-o','--outfile',
	help='if set graph will be saved to file, e.g. pdf or png')
args = parser.parse_args()

# folder to look for images
folder = args.indir

faces_imgPerWeek  = {}
nofac_imgPerWeek  = {}
faces1_imgPerWeek = {}
facesPerWeeknum   = {}


for filename in os.listdir(folder):
	splitted   = filename.split('_')
	numOfFaces = str(splitted[0])
	timestamp  = int(splitted[1])
	datestring = datetime.datetime.fromtimestamp(timestamp)
	y,m,d      = str(datestring).split(' ')[0].split('-')
	weeknum    = datetime.datetime(int(y), int(m), int(d)).isocalendar()[1] - 1

	if y not in facesPerWeeknum:
		facesPerWeeknum[y]   = [0]*52
		nofac_imgPerWeek[y]  = [0]*52
		faces_imgPerWeek[y]  = [0]*52
		faces1_imgPerWeek[y] = [0]*52

	facesPerWeeknum[y][weeknum] += int(numOfFaces)

	if int(numOfFaces) == 0:
		nofac_imgPerWeek[y][weeknum] += 1
	elif int(numOfFaces) == 1:
		faces1_imgPerWeek[y][weeknum] += 1
	else:
		faces_imgPerWeek[y][weeknum] += 1


data   = []
labels = []
keys = facesPerWeeknum.keys()
for i in range(len(keys)):
	keys[i] = int(keys[i])

keys.sort()

for key in keys:
	key = str(key)
	for i in range(len(facesPerWeeknum[key])):
		val = facesPerWeeknum[key][i]
		if val > 0:
			labels.append(facesPerWeeknum[key].index(val) + 1)
			datapoint = [faces_imgPerWeek[key][i], faces1_imgPerWeek[key][i], nofac_imgPerWeek[key][i]]
			data.append(datapoint)


plt.style.use('ggplot')


df2 = pd.DataFrame(data, columns=['>1 faces', '1 face', 'no faces'])
ax  = df2.plot(kind='bar', alpha=0.6, stacked=True)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_xticklabels(labels, rotation='horizontal')
ax.yaxis.grid(True)
ax.xaxis.grid(False)
ax.set_ylabel('number of posts')
ax.set_xlabel('week of year')

for container in ax.containers:
	plt.setp(container, width=1)

x0, x1 = ax.get_xlim()
ax.set_xlim(x0+0.5, x1)


if args.outfile:
	plt.savefig(args.outfile)
	print "Generated plot and saved it to: " + args.outfile
else:
	plt.show()