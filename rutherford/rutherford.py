import sys
import datetime
import matplotlib.pyplot as plt
import os

#Insert extra paths to be able to import functions from those directories
sys.path.insert(0, '../gif_maker')
sys.path.insert(0, '../general_functions')

#General imports
from gif_maker_file import make_gif
from general_functions_file import check_and_make, make_name, delete_map_content

#Simulation specific imports
from extra_functions_rutherford import update_location, calc_length_vector, calc_unit_vector
from extra_functions_rutherford import calc_direction_vector, calc_force, calc_new_velocity, check_inside_box

###############################################################################################################
#Description of simulation:
#
#
#
#
###############################################################################################################


###############################################################################################################
#General settings part of this project																		  #
###############################################################################################################
PLOT_FIGURE             = True 	# Setting whether to plot the animation as the simulation is running
SAVE_FIGURE             = True 	# Save the figures to the designated map
MAKE_GIFS               = True 	# Choose to make a gif from the resulting images (Save figure must be True)
DELETE_IMAGES_AFTER_GIF = True 	# If set to true, it will remove the images 

IMAGE_COUNTER           = 0		# Counter for naming the images
PLOT_PAUSE_TIME         = 0.01	# Pause time between each simulation steps
FPS                     = 10	# Frames per second for the gif
PLOT_QUALITY            = 50	# Image quality (can be changed in order to reduce gif size)
GIF_PLOT_STEPS          = 1     # Make a gif of each xth plot (1 is every plot, 2 is every second plot etc etc)

GENERAL_SIMULATION_NAME = 'rutherford'		# General project name
SAVE_FIGURE_FORMAT      = '.jpg'			# Figure format (should stay jpg or perhaps png)
SAVE_FIGURE_LOCATION    = 'plot_images'    	# Fill in a (submap) location where the plot images are saved (default = 'plot_images') (necessary for making gifs)
GIFS_LOCATION           = 'simulation_gifs' # Same goes for gif location (default = 'simulation_gifs')

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
#Simulation specific settings:	(User can change these values as they wish (debug before making gifs though!))#
###############################################################################################################
PLOT_STEPS 							= 1
steps 								= 100
dt 									= .05
time 								= 0
POWER 								= 2			# Power is the power to which the force is inversely proptional to

if SAVE_FIGURE:
	TOTAL_IMAGES 					= 10000 	#This number is only important for the saving of the images (e.g.: 000001.jpg)

#Keep in mind that these values are not really that meaningfull. It is all with respect to some unit mass and normalisation. 
mass_test_particle 					= 1
mass_fixed_particle 				= 1
charge_test_particle 				= -1
charge_fixed_particle 				= -10

initial_position_test_particle 		= [0.0,0.5]
initial_position_fixed_particle 	= [10.0,0.0]
initial_velocity_test_particle 		= [10.0,0.0]

plot_path 							= True
plot_unaffected_path 				= True
plot_zero_height_line 				= True
plot_height_info 					= False
plot_background_color 				= '#94E1E3'
plot_x_ticks 						= True
plot_y_ticks 						= True

plot_color_test_particle 			= 'r'
plot_color_fixed_particle 			= 'b'
plot_size_test_particle 			= 5
plot_size_fixed_particle 			= 10

plot_colors 						= [plot_color_test_particle,plot_color_fixed_particle]
plot_sizes 							= [plot_size_test_particle,plot_size_fixed_particle]
plot_x_padding_factors 				= [.1,.5] #These factors are to determine the box for the simulation, and the separation is multiplied by this number
plot_y_padding_factors 				= [.5,.5] #idem.


###############################################################################################################
#Simulation itself				 																			  #
###############################################################################################################

#Copy the position vectors
position_test_particle = initial_position_test_particle[:]
position_fixed_particle = initial_position_fixed_particle[:]
velocity_test_particle = initial_velocity_test_particle[:]

#Make list of all positions and the history of the positions
all_positions = [position_test_particle,position_fixed_particle]
all_positions_history = [all_positions]

#Calculate separation
Dx = abs(initial_position_test_particle[0]-initial_position_fixed_particle[0])
Dy = abs(initial_position_test_particle[1]-initial_position_fixed_particle[1])

#Calculate the draw limits of the plot
draw_limits_x = [initial_position_test_particle[0] - plot_x_padding_factors[0] * Dx,\
	initial_position_fixed_particle[0] + plot_x_padding_factors[1] * Dx]
draw_limits_y = [initial_position_test_particle[1] - plot_y_padding_factors[0] * Dx,\
	initial_position_fixed_particle[1] + plot_y_padding_factors[1] * Dx]

inside_box = True
#Set plot background colors
plt.rcParams['axes.facecolor'] = plot_background_color
plt.rcParams['savefig.facecolor'] = plot_background_color

while inside_box == True:
	#Calculate new force, new velocity and thereby the new position
	force_vector = calc_force(position_test_particle, position_fixed_particle, charge_test_particle, charge_fixed_particle, POWER)
	velocity_test_particle = calc_new_velocity(force_vector, mass_test_particle, velocity_test_particle, dt)
	position_test_particle = update_location(position_test_particle, velocity_test_particle, dt)	

	#Check whether the particle is still inside the box
	inside_box = check_inside_box(position_test_particle, draw_limits_x[0], draw_limits_x[1], draw_limits_y[0], draw_limits_y[1])

	#Manipulate and splitting some lists for plotting considerations
	all_positions = [position_test_particle, position_fixed_particle]
	all_positions_history.append(all_positions)
	x_positions = [el[0] for el in all_positions]
	y_positions = [el[1] for el in all_positions]

	#Setting draw limits
	plt.xlim(draw_limits_x)
	plt.ylim(draw_limits_y)

	#Set plot background colors
	plt.rcParams['axes.facecolor'] = plot_background_color
	plt.rcParams['savefig.facecolor'] = plot_background_color

	#Plot the path of the particle
	if plot_path:
		x_positions_test_history = [el[0][0] for el in all_positions_history]
		y_positions_test_history = [el[0][1] for el in all_positions_history]
		plt.plot(x_positions_test_history, y_positions_test_history, 'b--')

	#Plot the path of the particle as if there were no force acting on the 
	if plot_unaffected_path:
		plt.plot([initial_position_test_particle[0], initial_position_test_particle[0] + draw_limits_x[1] - draw_limits_x[0]],\
			[initial_position_test_particle[1], initial_position_test_particle[1]], 'r--', label='Unaffected path')

	#Plot the line with height = 0
	if plot_zero_height_line:
		plt.plot([initial_position_test_particle[0], initial_position_test_particle[0] + draw_limits_x[1] - draw_limits_x[0]], [0,0],\
			linestyle='--',color='b', label='Baseline (h=0)')
		plt.arrow(0, 0, 0, initial_position_test_particle[1], shape='full', lw=1, length_includes_head=True, head_width=.01)
	
	#Plot some text displaying b=...
	if plot_height_info:
		plt.text(initial_position_test_particle[0] + 0.2, initial_position_test_particle[1]/3.0, "b = %f"%initial_position_test_particle[1])

	#Plot the particle objects
	plt.plot(x_positions[0], y_positions[0], color = plot_colors[0], marker = 'o', markersize = plot_sizes[0],\
	 label='Test particle (m=%d, z=%d)'%(mass_test_particle,charge_test_particle))
	plt.plot(x_positions[1], y_positions[1], color = plot_colors[1], marker = 'o', markersize = plot_sizes[1],\
	 label=r"Fixed particle (z=%d, force $\propto \frac{1}{r^{%d}}$"%(charge_fixed_particle, POWER))
	
	for number in range(len(plot_colors)):
		plt.plot(x_positions[number], y_positions[number], color = plot_colors[number], marker = 'o', markersize = plot_sizes[number])

	#Generate the legend
	plt.legend( loc='lower left', numpoints = 1 )

	#Choose to set the axis visible
	plt.axes().xaxis.set_visible(plot_x_ticks)
	plt.axes().yaxis.set_visible(plot_y_ticks)

    ##Draw textbox and text
	if PLOT_FIGURE:
		plt.draw()
		plt.pause(PLOT_PAUSE_TIME)

	##Save the figure to the specified directory
	if SAVE_FIGURE:
		short_save_name = make_name(IMAGE_COUNTER, TOTAL_IMAGES, SAVE_FIGURE_FORMAT)
		save_name = os.path.join(SAVE_FIGURE_LOCATION,short_save_name)
		plt.savefig(save_name, bbox_inches='tight', quality = PLOT_QUALITY)
		IMAGE_COUNTER += 1

	#Clear canvas
	plt.clf()

###############################################################################################################
#End of simulation and wrapping up 																			  #
###############################################################################################################

#Close the canvas
if PLOT_FIGURE:
    plt.close()
#Make the gifs and delete the contents
print "FINISHED"
if MAKE_GIFS:
    print "GENERATING GIF IMAGE"
    make_gif(SAVE_FIGURE_LOCATION, GIFS_LOCATION, GIF_NAME, FPS, GIF_PLOT_STEPS)
    print "DONE"
if DELETE_IMAGES_AFTER_GIF:
    delete_map_content(SAVE_FIGURE_LOCATION)