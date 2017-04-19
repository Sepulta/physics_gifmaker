import sys
import datetime
import random
import matplotlib.pyplot as plt
import os

#Insert extra paths to be able to import functions from those directories
sys.path.insert(0, '../gif_maker')
sys.path.insert(0, '../general_functions')

#General imports
from gif_maker_file import make_gif
from general_functions_file import check_and_make, make_name, delete_map_content, gen_random_color

#Simulation specific imports
from extra_functions_3_body import calc_new_velocity, update_location, check_total_inside_box, generate_force_matrix

###############################################################################################################
# Description of simulation:
# This simulation visualizes the gravitational interaction of 3 (or more) particles/masses
# The user can change settings like the amount of particles and whether to plot the paths of the particles 
#
#
###############################################################################################################

###############################################################################################################
#General part of this project																				  #
###############################################################################################################
PLOT_FIGURE             = True		# Setting whether to plot the animation as the simulation is running
SAVE_FIGURE             = True		# Save the figures to the designated map
MAKE_GIFS               = True		# Choose to make a gif from the resulting images (Save figure must be True)
DELETE_IMAGES_AFTER_GIF = True		# If set to true, it will remove the images 

IMAGE_COUNTER           = 0			# Counter for naming the images
PLOT_PAUSE_TIME         = 0.01		# Pause time between each simulation step
FPS                     = 10		# Frames per second for the gif
PLOT_QUALITY            = 50		# Image quality (can be changed in order to reduce gif size)
GIF_PLOT_STEPS          = 1     # Make a gif of each xth plot (1 is every plot, 2 is every second plot etc etc)
PLOT_WIDTH              = 5     # Dimension of the resulting plot in inches
PLOT_HEIGTH             = 5     # Dimension of the resulting plot in inches

GENERAL_SIMULATION_NAME = '3_body'				# General project name
SAVE_FIGURE_FORMAT      = '.jpg'				# Figure format (should stay jpg or perhaps png)
SAVE_FIGURE_LOCATION    = 'plot_images'    		# Fill in a (submap) location where the plot images are saved (default = 'plot_images') (necessary for making gifs)
GIFS_LOCATION           = 'simulation_gifs'   	# Same goes for gif location (default = 'simulation_gifs')

DATETIME_NOW = datetime.datetime.now()			# Gets the current time
DATETIME_STRING = DATETIME_NOW.strftime("%Y_%m_%d_%H:%M")	#Turn it into a string with date formatting

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
generate_random_positions 		= True		# Decide to generate random positions, if not; You need to define the positions yourself
simulate_until_out_of_bounds 	= True		# Run the simulation until one of the particles gets out out the box
generate_random_colors 			= True		# Let the script generate some random colors (can happen that they look like eachother though!) 
plot_particle_history 			= True		# Plot the history of the particle

number_of_particles 			= 3 		# Amount of particles to simulate
max_steps 						= 200 		# Amount of maximal simulation steps before the simulation is terminated
	
dt 								= 0.05 		# Timestep for simulation
softening_length 				= 0.1 		# Softening length is the error introduced in the calculation of the force, to evade zero division
default_color 					= 'r'		# Default color for particles and their paths
default_plot_size 				= 5			# Default plot size for the particles. Particles could have different sizes, proportional to masses
plot_background_color 			= 'white' 	# Not all names of colors can be used. If a specific color is desired, use hexadecimal or rgb

#Set bounds of simulation
x_bounds 						= [0,10]	#Lower and upper x_bounds of simulated box
y_bounds 						= [0,10]	#Lower and upper y_bounds of simulated box

#Initialize some lists 
masses_of_particles 			= [1 for el in range(number_of_particles)]
velocities_of_particles 		= [[0,0] for el in range(number_of_particles)]
colors_of_particles 			= [default_color for el in range(number_of_particles)]
sizes_of_particles 				= [default_plot_size for el in range(number_of_particles)]

##If you change the list of masses, the sizes will be set to default_size*mass. 
#Beware, if the masses are manually set, the list has to be as long as the number of particles


masses_of_particles = [1,2,1]
if not masses_of_particles.count(masses_of_particles[0]/masses_of_particles[0]) == len(masses_of_particles):
	sizes_of_particles = [default_plot_size * el for el in masses_of_particles]

#Generate random colors for particles
if generate_random_colors:
	colors_of_particles = [gen_random_color(.2,.8) for el in range(number_of_particles)]

Dx = x_bounds[1]-x_bounds[0]
Dy = y_bounds[1]-y_bounds[0]

#Generate random positions of particles, but only if the setting is set to True
if generate_random_positions:
	particle_positions = []
	for i in range(number_of_particles):
		particle_positions.append([x_bounds[0] + 0.1*Dx + 0.8*Dx * random.random(), y_bounds[0] + 0.1*Dy + 0.8*Dy * random.random()])

if plot_particle_history:
	particle_position_history = [particle_positions]

###############################################################################################################
#Simulation itself																							  #
###############################################################################################################

#Set plot ratio and dimensions
plt.figure(figsize=(PLOT_WIDTH, PLOT_HEIGTH))


inside_box = True
ctr = 0 		# Iterator initiation
while inside_box == True and ctr < max_steps:
	#Make new lists for positions and velocities each time.
	new_positions = []
	new_velocities = []

	#Generate force_matrix:

	forces_list = generate_force_matrix(particle_positions,masses_of_particles,softening_length)
	for i in range(number_of_particles):
		new_current_velocity = calc_new_velocity(forces_list[i],masses_of_particles[i],velocities_of_particles[i],dt)
		new_current_position = update_location(particle_positions[i],new_current_velocity,dt)
		new_positions.append(new_current_position)
		new_velocities.append(new_current_velocity)

	#Copy the lists again
	particle_positions = new_positions[:]
	if plot_particle_history:
		particle_position_history.append(particle_positions)
	velocities_of_particles = new_velocities[:]

	#Calculate whether the particles are still inside the box. This determines whether the simulation ends or not.
	if simulate_until_out_of_bounds:
		inside_box = check_total_inside_box(particle_positions,x_bounds[0],x_bounds[1],y_bounds[0],y_bounds[1])

	#Manipulate lists to plot more easily
	x_positions = [el[0] for el in particle_positions]
	y_positions = [el[1] for el in particle_positions]

	#Set plot limits
	plt.xlim(x_bounds)
	plt.ylim(y_bounds)

	#Set background colors
	plt.rcParams['axes.facecolor']=plot_background_color
	plt.rcParams['savefig.facecolor']='white'

	#Plot their paths
	if plot_particle_history:
		for number in range(number_of_particles):
			x_position_history = [el[number][0] for el in particle_position_history]
			y_position_history = [el[number][1] for el in particle_position_history]
			plt.plot(x_position_history,y_position_history, color = colors_of_particles[number], linestyle = '--')

	#Plot particles
	for number in range(number_of_particles):
		plt.plot(x_positions[number],y_positions[number], color = colors_of_particles[number], marker = 'o', markersize = sizes_of_particles[number])

	if PLOT_FIGURE:
		plt.draw()
		plt.pause(PLOT_PAUSE_TIME)

	##Save the figure to the specified directory
	if SAVE_FIGURE:
		short_save_name = make_name(IMAGE_COUNTER,max_steps,SAVE_FIGURE_FORMAT)
		save_name = os.path.join(SAVE_FIGURE_LOCATION,short_save_name)
		plt.savefig(save_name,bbox_inches='tight', quality = PLOT_QUALITY)
		IMAGE_COUNTER += 1
	plt.clf()

	#Increment iterator
	ctr += 1

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