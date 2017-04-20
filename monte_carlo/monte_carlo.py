import sys
import datetime
import matplotlib.pyplot as plt
import os
import math

#Insert extra paths to be able to import functions from those directories
sys.path.insert(0, '../gif_maker')
sys.path.insert(0, '../general_functions')

#General imports
from gif_maker_file import make_gif

#Simulation specific imports
from general_functions_file import check_and_make, make_name, delete_map_content
from extra_functions_monte_carlo import gen_func, monte_carlo

###############################################################################################################
# Description of simulation:
# Visualization of Monte-Carlo integration. 
# The user can make a mathematical function and integrate this within a range using the monte-carlo technique
# This is plotted and saved to jpg images in the specific folder, and those images will be processed into a 
# Gif image. 
# TO DO: Better information on plot
###############################################################################################################

###############################################################################################################
#General settings part of this project                                                                        #
###############################################################################################################
PLOT_FIGURE             = True  # Setting whether to plot the animation as the simulation is running
SAVE_FIGURE             = True  # Save the figures to the designated map
MAKE_GIFS               = True  # Choose to make a gif from the resulting images (Save figure must be True)
DELETE_IMAGES_AFTER_GIF = True  # If set to true, it will remove the images 

IMAGE_COUNTER           = 0     # Counter for naming the images
PLOT_PAUSE_TIME         = 0.01  # Pause time between each simulation step
FPS                     = 10    # Frames per second for the gif
PLOT_QUALITY            = 50    # Image quality (can be changed in order to reduce gif size)
GIF_PLOT_STEPS          = 3     # Make a gif of each xth plot (1 is every plot, 2 is every second plot etc etc)
PLOT_WIDTH              = 5     # Dimension of the resulting plot in inches
PLOT_HEIGTH             = 5     # Dimension of the resulting plot in inches

GENERAL_SIMULATION_NAME = 'monte_carlo'       # General project name
SAVE_FIGURE_FORMAT      = '.jpg'              # Figure format (should stay jpg or perhaps png)
SAVE_FIGURE_LOCATION    = 'plot_images'       # Fill in a (submap) location where the plot images are saved (default = 'plot_images') (necessary for making gifs)
GIFS_LOCATION           = 'simulation_gifs'   # Same goes for gif location (default = 'simulation_gifs')

DATETIME_NOW = datetime.datetime.now()
DATETIME_STRING = DATETIME_NOW.strftime("%Y_%m_%d_%H:%M")

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
        print "Starting program to generate "+str(GIF_NAME)

###############################################################################################################
#Simulation specific settings:  (User can change these values as they wish (debug before making gifs though!))#
###############################################################################################################

#Create your own functions to monte-carlo simulate and plot
def func_sin_squared(x):
    """
    Functions like this can be used to input in the gen_function and monte_carlo to
    to produce the values of a function
    """
    return math.sin(x**2)

def func_cos_squared(x):
    return math.cos(x**2)

def func_x_squared(x):
    return x**2

def func_sin(x):
    return math.sin(x)


#Specific settings for the function
function_name           = func_cos_squared        #Specified function to perform montecarlo simulation on
x_min, x_max            = 0.0, math.pi                #Lower and upper x bounds
steps                   = 1000                  #Total steps (which is, total random points)
PLOT_STEPS              = 10                    #The plot is shown per PLOT_STEPS (because plotting each individual point would be tedious and non insightful)

if SAVE_FIGURE:
    TOTAL_IMAGES = int(steps/float(PLOT_STEPS))
    print 'CREATING A TOTAL OF '+str(TOTAL_IMAGES)+' IMAGES'

#plotsettings:
good_color              = 'g'       # Color for the 'good' points (those inside the integral) 
bad_color               = 'r'       # Color for the 'bad' points (those outside the integral)
linewidth_box           = 2         # Linewidth of the box that is drawn around the curve
linewidth_figure        = 3         # Linewidth of the curve itself
display_info_on_graph   = True      # Whether to display the information of this integration on the canvas

###############################################################################################################
#Simulation itself                                                                                            #
###############################################################################################################
result_graph = gen_func(function_name, x_min, x_max, steps)
y_min, y_max = result_graph[2], result_graph[3]

#Set plot ratio and dimensions
plt.figure(figsize=(PLOT_WIDTH, PLOT_HEIGTH))

#Integration is from the zero x line, 
if y_min > 0:
    y_min = 0

Dy = y_max-y_min
Dx = x_max-x_min
SIZE_BOX = Dy * Dx

#Extract results monte carlo
resultaat_montecarlo = monte_carlo(function_name,x_min,x_max,y_min,y_max,steps)
x_list = [el[0][0] for el in resultaat_montecarlo]
y_list = [el[0][-1] for el in resultaat_montecarlo]
in_or_out_list = [el[-1] for el in resultaat_montecarlo]

percent_inside = 0
percent_outside = 0
surface_integral = 0

#Create a range to plot the simulation. At some points you may want to increase plot
#stepsize, as it would take very long to animate/make a gif
plot_range = range(0, steps, PLOT_STEPS)

if plot_range[-1] != steps - 1:
    plot_range.append(steps - 1)

#Loop for creating plots, possibly saving them
for step in plot_range:
    #Reshape plot field
    plt.ylim(y_min - 0.1 * Dy, y_max + 0.1 * Dy)
    if display_info_on_graph:
        plt.ylim(y_min - 0.1 * Dy, y_max + 0.5 * Dy)
    plt.xlim(x_min - 0.1 * Dx, x_max +0.1 * Dy)

    #Draw axes-labels
    plt.xlabel('x')
    plt.ylabel('y(x)')

    plot_result_list = []

    #Draw result data:
    #Take result list
    plot_result_list = resultaat_montecarlo[:step]
    
    #Split lists according to in or out
    inside_list = [el for el in plot_result_list if el[-1] == 1]
    outside_list = [el for el in plot_result_list if el[-1] == 0] 

    #Split those lists for coordinates
    #All coordinates inside the graph
    x_inside_list = [el[0][0] for el in inside_list]
    y_inside_list = [el[0][-1] for el in inside_list]

    x_outside_list = [el[0][0] for el in outside_list]
    y_outside_list = [el[0][-1] for el in outside_list]

    #All coordinates outside the graph
    x_inside_list_pos = [el[0][0] for el in inside_list if el[0][-1] >= 0]
    x_inside_list_neg = [el[0][0] for el in inside_list if el[0][-1] < 0]

    amt_inside_pos =len(x_inside_list_pos)
    amt_inside_neg =len(x_inside_list_neg)

    amt_outside = len(x_outside_list)
    amt_tot = amt_outside + amt_inside_pos + amt_inside_neg

    if step != 0:
        percent_inside_pos = float(amt_inside_pos)/float(amt_tot)
        percent_inside_neg = float(amt_inside_neg)/float(amt_tot)
        percent_outside = float(amt_outside)/float(amt_tot)
        surface_integral = (percent_inside_pos-percent_inside_neg) * SIZE_BOX
        step_text = str(step)+'/'+str(steps)
        amt_outside_text = str(amt_outside)+'/'+str(amt_tot)
        amt_inside_neg_text = str(amt_inside_neg)+'/'+str(amt_tot)
        amt_inside_pos_text = str(amt_inside_pos)+'/'+str(amt_tot)

        ##Figure out a way to nicely do this
        if display_info_on_graph:
            info_text = 'Step: %s'%str(step_text)
            info_text += '\nCalculated surface: %0.4f'%(surface_integral)
            info_text += '\nAmt outside: %s/%s'%(str(amt_outside),str(amt_tot))
            info_text += '\nAmt inside (neg): %s/%s'%(str(amt_inside_neg),str(amt_tot))
            info_text += '\nAmt inside (pos): %s/%s'%(str(amt_inside_pos),str(amt_tot))
            plt.text(x_min,y_max+0.1*Dy,info_text)   
    plt.plot(x_inside_list, y_inside_list, good_color+'o')
    plt.plot(x_outside_list, y_outside_list, bad_color+'o')

    ##Plot Graph itself and box
    
    #Draw box around graph
    plt.plot([x_min,x_min],[y_min,y_max],'g-',linewidth = linewidth_box)
    plt.plot([x_max,x_max],[y_min,y_max],'g-',linewidth = linewidth_box)
    plt.plot([x_min,x_max],[y_min,y_min],'g-',linewidth = linewidth_box)
    plt.plot([x_min,x_max],[y_max,y_max],'g-',linewidth = linewidth_box)

    #Draw figure
    plt.plot(result_graph[0],result_graph[1],'b-',linewidth = linewidth_figure)

    #Draw dashed dashed zero-line if y_max < 0:
    if y_min < 0:
        plt.plot([x_min,x_max],[0,0],'--',linewidth = linewidth_figure)

    ##Draw textbox and text
    if PLOT_FIGURE:
        #Draw amt steps
        plt.draw()
        plt.pause(PLOT_PAUSE_TIME)

    #
    if SAVE_FIGURE:
        short_save_name = make_name(IMAGE_COUNTER,TOTAL_IMAGES,SAVE_FIGURE_FORMAT)
        save_name = os.path.join(SAVE_FIGURE_LOCATION,short_save_name)
        plt.savefig(save_name, bbox_inches='tight', quality = PLOT_QUALITY)

        IMAGE_COUNTER += 1

    plt.clf()
    

###############################################################################################################
#End of simulation and wrapping up                                                                            #
###############################################################################################################

if PLOT_FIGURE:
    plt.close()

print "FINISHED"
if MAKE_GIFS:
    print "GENERATING GIF IMAGE"
    make_gif(SAVE_FIGURE_LOCATION, GIFS_LOCATION, GIF_NAME, FPS, GIF_PLOT_STEPS)
    print "DONE"
if DELETE_IMAGES_AFTER_GIF:
    delete_map_content(SAVE_FIGURE_LOCATION)