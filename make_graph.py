import matplotlib.pyplot as plt
import argparse
import os
import sys
import numpy

#===== GENERAL SETTINGS =====
numpy.set_printoptions(formatter={'float': '{:0.3f}'.format})
#===== ARGPARSE SETTINGS =====
parser = argparse.ArgumentParser(description='A script to plot graph of antenna radiation pattern from messy pile of numbers in *.txt from TBK; CTU FEE')
parser.add_argument("-f","--f", dest='FILE_PATH', required=True, type=str, help="path to *.txt file obtained by script (obtained in LAB)")
parser.add_argument("-s","--s", dest='PRINT_PATH', required=False, type=str, help="saves graph as image to PRINT_PATH, filename can be specified as *.png (default) or *.svg")
parser.add_argument("-b","--b", dest='BLIND_MODE', action='store_true',help="blind mode, does not show loaded data and does not show graph after save, ignored if PRINT_PATH is not specified")
parser.add_argument("-t","--t", dest='TITLE', required=False, type=str, help="title of plotted graph")
parser.add_argument("-c","--c", dest='COLOR', required=False, type=str, help = "set color of graph, \033[3muse: \033[94m'blue','green','red','yellow','magenta', 'cyan', 'black' and 'white'\033[0m\033[3m or color names defined by CSS\033[0m")

args = parser.parse_args()
#Saving paths to folders / variables
file_path = args.FILE_PATH
print_path = args.PRINT_PATH
blind_mode = args.BLIND_MODE
title = args.TITLE
color = args.COLOR

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

#===== PRINT PATH MAGIC =====
if(print_path is not None): #if save path is a folder, create file name for chart
    if(os.path.isdir(print_path)):
        graph_filename = "graph_" + file_filename + ".png"
        print_path = os.path.join(print_path,graph_filename)    #match user specified folder with created filename
    print_directory, print_filename = os.path.split(print_path)
    print_filename, print_extension = os.path.splitext(print_filename) #get filename extension for selecting saving command (later)
    print("\033[33m   Info:\033[0m \033[93m\033[3mGraph will be saved to:\033[0m\033[3m",print_path,"\033[0m")
else:
    print("\033[33m   Info:\033[0m \033[93m\033[3mGraph will not be saved.\033[0m")

#===== TITLE EXTRACTION =====
if(title is None):  #if title was not specified, create it automatically from input file name
    title = "Graph of " + file_filename

#===== COLOR SET =====
if(color is None):  #if no chart color was specified by the user, set it to default (blue) color
    color = "blue"

#===== MAIN CODE =====
with open(file_path, 'r') as file:  #open file content
    content = file.read()

if(file is None or content is None):
    print("\033[91mFAIL\033[0m")
    sys.exit("\033[91mReading file did not complete right!\033[0m")

if(blind_mode==False): print("\n Content of file: \n\n",content)    #debug data print
##numbers = list(map(float, content.split()))

numbers = numpy.fromstring(content, dtype=float, sep=' ')   #load data from string to float array

norm_const = max(numbers)   #find highest value in array to norm values
print("\033[33m   Info:\033[0m \033[93m\033[3mFound norming constant =\033[0m\033[3m",norm_const,"\033[0m")

numbers = numbers - norm_const  #norm numbers array

#print("\n Content of file (normed number array) with",len(numbers),"numbers: \n\n",numbers)
#meas_step = 360/(len(numbers)-1)

x=numpy.linspace(-180.0,180.0,len(numbers)) #prepare array of angles for x axis

plt.plot(x, numbers, color)                 #plot: x = angle, y = amplitude in dB
plt.grid(True)                              #show grid in chart
plt.xticks(numpy.linspace(-180, 180, 13))   #set x axis ticks from -180 to 180 in 13 steps
plt.yticks(numpy.linspace(-45, 0, 10))      #set y axis ticks from -45 to 0 in 10 steps
plt.xlim(-180, 180)                         #set x range in chart from -180° to 180°
plt.ylim(-45,2)                             #set y range in chart from -45 to 2
plt.xlabel("Úhel/°")                        #add x axis label
plt.ylabel("Amplituda/dB")                  #add y axis label
plt.title(title)                            #add title to the plot

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