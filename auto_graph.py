import matplotlib.pyplot as plt
import argparse
import os
import sys
import numpy
import math

#===== GENERAL SETTINGS =====
numpy.set_printoptions(formatter={'float': '{:0.3f}'.format})
#===== ARGPARSE SETTINGS =====
parser = argparse.ArgumentParser(description='A script to plot graph of s11 or VSWR from messy pile of numbers in *.txt from TBK; CTU FEE')
parser.add_argument("-v","--v", dest="VERSION", required=True, type=str, help="type of graph plotted, \033[3muse:\033[94m'1', 'A', 'S' or 'S11'\033[0m\033[3m for s11 graph and \033[94m'2', 'B', 'V' or 'VSWR'\033[0m\033[3m for VSWR graph\033[0m")
parser.add_argument("-f","--f", dest='FILE_PATH', required=True, type=str, help="path to *.txt file with s11 params (downloaded from Moodle)")
parser.add_argument("-s","--s", dest='PRINT_PATH', required=False, type=str, help="saves graph as image to PRINT_PATH, filename can be specified as *.png (default) or *.svg")
parser.add_argument("-t","--t", dest='TITLE', required=False, type=str, help="title of plotted graph")
parser.add_argument("-c","--c", dest='COLOR', required=False, type=str, help = "set color of graph, \033[3muse: \033[94m'blue','green','red','yellow','magenta', 'cyan', 'black' and 'white'\033[0m\033[3m or color names defined by CSS\033[0m")
parser.add_argument("-b","--b", dest='BLIND_MODE', action='store_true', help="blind mode, does not show loaded data and does not show graph after save, ignored if PRINT_PATH is not specified")
args = parser.parse_args()
#Saving paths to folders / variables
file_path = args.FILE_PATH
print_path = args.PRINT_PATH
blind_mode = args.BLIND_MODE
color = args.COLOR
title = args.TITLE
version = args.VERSION

#===== INPUT FILENAME EXTRACT =====
directory, filename = os.path.split(file_path)
file_filename, file_extension = os.path.splitext(filename)

print("Loading...")

#===== PATHS CHECK =====
if(os.path.exists(file_path)):  #checking requested *.txt file location
    if(os.path.isfile(file_path)):  #checking if requested *.txt file is file
        print("\033[92mOK\033[0m, input file found.")
    else:
        print("\033[91mFAIL\033[0m")
        sys.exit("\033[91mPath is valid but it misses filename!\033[0m")
else:
    print("\033[91mFAIL\033[0m")
    sys.exit("\033[91mPath to data does not exist!\033[0m")

#===== GRAPH TYPE =====
version_num = 0
version_1 = ["1","A","a","S","s","s11","S11"]   #all posible variants of '-v' (version) param for s11 graph
version_2 = ["2","B","b","V","v","VSWR","vswr"] #all posible variants of '-v' (version) param for VSWR graph
if(version in version_1):   #s11 graph
    print("\033[33m   Info:\033[0m \033[93m\033[3mGraph type: \033[0m\033[3ms11\033[0m")
    version_num=1
elif(version in version_2): #VSWR graph
    print("\033[33m   Info:\033[0m \033[93m\033[3mGraph type: \033[0m\033[3mVSWR\033[0m")
    version_num=2
else:   #FAIL (no match)
    print("\033[91mFAIL\033[0m")
    print("\033[3mUse:\033[94m'1', 'A', 'S' or 'S11'\033[0m\033[3m for s11 graph and \033[94m'2', 'B', 'V' or 'VSWR'\033[0m\033[3m for VSWR graph\033[0m.")
    sys.exit("\033[91mCannot match graph type with one of the defined names!\033[0m")

#===== TITLE EXTRACTION =====
if(title is None):  #if title was not specified, create it automatically from chart type and input file name
    title = "Graph of " + file_filename
    if(version_num==1): title = "Graph s11 of " + file_filename
    elif(version_num==2): title = "Graph VSWR of " + file_filename

#===== PRINT PATH MAGIC =====
if(print_path is not None):
    if(os.path.isdir(print_path)): #if save path is a folder, create file name for chart
        if(version_num == 1):
            graph_type = "s11"
        elif(version_num == 2):
            graph_type = "VSWR"
        graph_filename = "graph_" + graph_type + "_" + file_filename + ".png"
        print_path = os.path.join(print_path,graph_filename) #match user specified folder with created filename
    print_directory, print_filename = os.path.split(print_path)
    print_filename, print_extension = os.path.splitext(print_filename) #get filename extension for selecting saving command (later)
    print("\033[33m   Info:\033[0m \033[93m\033[3mGraph will be saved to:\033[0m\033[3m",print_path,"\033[0m")
else:
    print("\033[33m   Info:\033[0m \033[93m\033[3mGraph will not be saved.\033[0m")

#===== COLOR SET =====
if(color is None): #if no chart color was specified by the user, set it to default (blue) color
    color = "blue"

#===== MAIN CODE =====
with open(file_path, 'r') as file: #open file content
    content = file.read()
freq = []   #frequency array
mag = []    #magnitude array
mag_db = [] #magnitude in dB array (calculated for |s11| graph)
ang = []    #angle array
run = 0     #counter of position in 'table' (used in data to array filler)
psv = []    #VSWR array (calculated for VSWR graph)
for x in content.split(): #fill arrays with data loaded in previous step, data must be this order: FREQ   MAG   ANG \n (frequency, magnitude, angle)
    modulo = run % 3
    match modulo:
        case 0:
            freq.append(float(x))
        case 1:
            mag.append(float(x))
        case 2:
            ang.append(float(x))
    run += 1
if(not(len(freq) == len(mag) == len(ang))): #all data must be the same length, if not, terminate
    print("\033[91mFAIL\033[0m")
    sys.exit("\033[91mTable is corrupted!\033[0m")

length = len(freq)  #defines number of iterations for next steps
for x in range(length): #values for |s11| and VSWR graphs calculator
    mag_db.append(20*math.log10(mag[x]))
    psv.append((1+mag[x])/(1-mag[x]))
for x in range(length): #frequency divider (from x*10^9 Hz to x GHz) + debug print of values
    freq[x] /= 1000000000
    if(not blind_mode): print("Freq:",freq[x],"magnitude |s11|:",mag[x],"angle |s11|:",ang[x])

if(version_num==1): #graph settings for |s11|
    plt.plot(freq,mag_db,color)             #plot: x = frequency, y = magnitude in dB
    plt.title(title)                        #add title to plot
    plt.xticks(numpy.arange(0, 26.1, 2))    #set x axis ticks from 0 to 26 with step of 2 (0-2-4-...-26)
    plt.yticks(numpy.linspace(-45,0,10))    #set y axis ticks from -45 to 0 with 10 steps
    plt.xlim(1,21)                          #set x axis range in chart from 1 to 21
    plt.ylim(-45,2)                         #set y axis range in chart from -45 to 2
    plt.xlabel("Frekvence/GHz")             #add x axis label
    plt.ylabel("|s11|/dB")                  #add y axis label
    plt.grid(True)                          #show grid in chart
elif(version_num==2):
    plt.plot(freq,psv,color)                #plot: x = frequency, y = VSWR
    plt.title(title)                        #add title to plot
    plt.xticks(numpy.arange(0, 26.1, 2))    #set x axis ticks from 0 to 26 with step of 2 (0-2-4-...-26)
    plt.yticks(numpy.linspace(1,2,11))      #set y axis ticks from -95 to 0 with 20 steps
    plt.xlim(1,21)                          #set x axis range in chart from 1 to 21
    plt.ylim(1,2.05)                        #set y axis range in chart from 1 to 2
    plt.xlabel("Frekvence/GHz")             #add x axis label
    plt.ylabel("VSWR/-")                    #add y axis label
    plt.grid(True)                          #show grid in chart

if(print_path is not None):
    print("\033[33m   Info:\033[0m \033[93m\033[3mSaving graph.\033[0m")
    if(print_extension == ".png"): plt.savefig(print_path, dpi=500, bbox_inches='tight', transparent=True)  #save to previously created print_path *.png file of chart
    if(print_extension == ".svg"): plt.savefig(print_path, format='svg')                                    #save to previously created print_path *.svg file of chart
    if(blind_mode == False):
        print("\033[33m   Info:\033[0m \033[93m\033[3mShowing graph.\033[0m")
        plt.show()
else:
    print("\033[33m   Info:\033[0m \033[93m\033[3mShowing graph.\033[0m")
    plt.show()


print("\033[92mDONE\033[0m, all finished.")
