
import sys
import math
import random
import time
import datetime
import os
import numpy as np
import matplotlib.pyplot as plt


#Insert extra paths to be able to import functions from those directories
sys.path.insert(0, '../gif_maker')
sys.path.insert(0, '../general_functions')

from gif_maker_file import make_gif
from general_functions_file import check_and_make, make_name, delete_map_content


###############################################################################################################
#General settings of this project                                                                        #
###############################################################################################################
PLOT_FIGURE             = True  # Setting whether to plot the animation as the simulation is running
SAVE_FIGURE             = True  # Save the figures to the designated map
MAKE_GIFS               = True
DELETE_IMAGES_AFTER_GIF = True  # If set to true, it will remove the images 

IMAGE_COUNTER           = 0     # Counter for naming the images
PLOT_PAUSE_TIME         = 0.01  # Pause time between each simulation step
FPS                     = 20    # Frames per second for the gif
PLOT_QUALITY            = 100   # Image quality (can be changed in order to reduce gif size)
GIF_PLOT_STEPS          = 1     # Make a gif of each xth plot (1 is every plot, 2 is every second plot etc etc)

GENERAL_SIMULATION_NAME = 'diffusion'         # General project name
SAVE_FIGURE_FORMAT      = '.jpg'              # Figure format (should stay jpg or perhaps png)
SAVE_FIGURE_LOCATION    = 'plot_images'       # Fill in a (submap) location where the plot images are saved (default = 'plot_images') (necessary for making gifs)
GIFS_LOCATION           = 'simulation_gifs'   # Same goes for gif location (default = 'simulation_gifs')

DATETIME_NOW = datetime.datetime.now()                      # Gets the current time
DATETIME_STRING = DATETIME_NOW.strftime("%Y_%m_%d_%H:%M")   # Turn it into a string with date formatting

#Functions to check whether the directories exist, incase no: make them.
if SAVE_FIGURE:
  check_and_make(SAVE_FIGURE_LOCATION)
if MAKE_GIFS:
  check_and_make(GIFS_LOCATION)

if MAKE_GIFS:
    GIF_NAME = GENERAL_SIMULATION_NAME + '_' + DATETIME_STRING
    if not SAVE_FIGURE:
        print 'WARNING: NO GIF CAN BE MADE IF THE FIGURES ARE NOT SAVED TO A LOCATION\nPLEASE CHANGE THE "SAVE_FIGURE" SETTING'
    else:
        print "Starting program to generate %s"%(GIF_NAME)

###############################################################################################################
#Simulation settings                                                                                          #
###############################################################################################################

#This section is used to store simulation specific parameter settings, e.g. plot colors or simlation bounds



###############################################################################################################
#Simulation itself                                                                                            #
###############################################################################################################

#In this section the simulation itself is placed. 

#This part with save figure is necessary, as this saves the plots to the specific directory, in order to generate a GIF later on.
if SAVE_FIGURE:
    short_save_name = make_name(IMAGE_COUNTER,TOTAL_IMAGES,SAVE_FIGURE_FORMAT)
    save_name = os.path.join(SAVE_FIGURE_LOCATION,short_save_name)
    plt.savefig(save_name, bbox_inches='tight', quality = PLOT_QUALITY)

    IMAGE_COUNTER += 1

###############################################################################################################
#End of simulation and wrapping up                                                                            #
###############################################################################################################

#This last part is a small section, closing the plot canvas and making the gif image and cleaning up the directory

if PLOT_FIGURE:
    plt.close()

print "FINISHED"
if MAKE_GIFS:
    print "GENERATING GIF IMAGE"
    make_gif(SAVE_FIGURE_LOCATION, GIFS_LOCATION, GIF_NAME, FPS, GIF_PLOT_STEPS)
    print "DONE"
if DELETE_IMAGES_AFTER_GIF:
    delete_map_content(SAVE_FIGURE_LOCATION)