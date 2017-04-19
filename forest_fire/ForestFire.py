import sys
import datetime
import os
import fire_visualize

from extra_functions_forest_fire import RectangularRoom,check_if_in_room

#Insert extra paths to be able to import functions from those directories
sys.path.insert(0, '../gif_maker')
sys.path.insert(0, '../general_functions')

from gif_maker_file import make_gif
from general_functions_file import check_and_make, make_name, delete_map_content, gen_random_color

###############################################################################################################
# Description of simulation:                                                                                  #
# What this simulation mainly does is simulate a spreading fire, starting from the most upper row.            #
# The fire spreads throughout a grid (partially) filled with forest tiles, able to catch fire.                #
# The ratio of filling of forest tiles is adjustable, as well as the dimensions of the "forest"               #
# TODO: Make window more fitting
###############################################################################################################

###############################################################################################################
# General settings part of this project                                                                       #
###############################################################################################################

PLOT_FIGURE             = True               # Setting whether to plot the animation as the simulation is running
SAVE_FIGURE             = True                # Save the figures to the designated map
MAKE_GIFS               = True                # Choose to make a gif from the resulting images (Save figure must be True) 
DELETE_IMAGES_AFTER_GIF = True                # If set to true, it will remove the images 

IMAGE_COUNTER           = 0                   # Counter for naming the images
PLOT_PAUSE_TIME         = 0.01                # Pause time between each simulation step
FPS                     = 10                  # Frames per second for the gif
PLOT_QUALITY            = 80                  # Image quality (can be changed in order to reduce gif size)
GIF_PLOT_STEPS          = 1                   # Make a gif of each xth plot (1 is every plot, 2 is every second plot etc etc)

GENERAL_SIMULATION_NAME = 'forest_fire'       # General project name
SAVE_FIGURE_FORMAT      = '.jpg'              # Figure format (should stay jpg or perhaps png)
SAVE_FIGURE_LOCATION    = 'plot_images'       # Fill in a (submap) location where the plot images are saved (default = 'plot_images') (necessary for making gifs)
GIFS_LOCATION           = 'simulation_gifs'   # Same goes for gif location (default = 'simulation_gifs')

DATETIME_NOW            = datetime.datetime.now()
DATETIME_STRING         = DATETIME_NOW.strftime("%Y_%m_%d_%H:%M")
max_steps               = 100000

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
        print "Starting program to generate %s"%str(GIF_NAME)

###############################################################################################################
#Simulation specific settings:  (User can change these values as they wish (debug before making gifs though!))#
###############################################################################################################

width = 10              # Integer representing width
height = 40             # Integer represention height
ratio = 0.6             # Fraction representing percentage of burnable forest tiles
mode = "moore"          # 'neumann' or 'moore'
plot = False            # Whether to plot the graph of total tile values
print_info = True       # Whether to print statements of reaching the other side 


###############################################################################################################
#Simulation itself                                                                                            #
###############################################################################################################

# Creating a room object 
room = RectangularRoom(width, height, ratio)

# Print some information
if print_info:
    print "Simulating a very basic model of a forest fire in a %d by %d (width,height) grid."%(width,height)
    if mode == "neumann":
        mode_string = 'Neumann (only horizontal and vertical direct neighbours)'
    elif mode == 'moore':
        mode_string = '"Moore" (horizontal, vertical and diagonal direct neighbours)'
    else:
        print "WARNING:\tAn invalid mode setting has been chosen."
    print "Selected mode is: %s"%mode_string

# Initializing the animate function, if preferred. While actually simulating this value is turned off
if PLOT_FIGURE == True:
    anim = fire_visualize.FireVisualization(width, height, room, mode, 0.5)

# Makes the object which actually saves the images. Had to be another object, as tk-inter cant handle saving. SO i used the Image module from PIL
if SAVE_FIGURE == True:
    draw_object = fire_visualize.FireToJPG(width, height, room, mode)

# As the first row of the grid is already on fire, t is beginning at t = 1, else the fire is able to reach the other side within less steps as actually possible.
t = 1

# Marker for first fire at other side:
first_fire_other_side = False

# Status list initialized, for saving each step and the details of each step
status_list = []

# End line list initialized, for saving the moment of reaching the other side, or not.
# [0,timestep] means not reaching the other side, and the saved timestep is the time at which the last fire burns out
# [1,timestep] means reaching the other side, and the saved timestep is the time at which the first fire reaches the other side.
end_line = []



# The loop function runs as long as there are tiles burning
while room.getStatusCount(room)[2] > 0:

    #Initializing the update list, which holds all the tiles previously having value 2 (forest tiles) which are going to be value 3 (burning tiles)
    update_list = []

    #The unique update list only holds unique tiles, as quite some tiles will be doubly counted
    unique_update_list = []

    #black_list is the list of tiles which will go from value 2 to value 3(thus from burning to burned)
    black_list = []

    #Looping over the whole room.
    for i in range(0,width):
        for j in range(0,height):

            #If there are burning fires, they are added to the black_list to have them extinguished next round
            if room.getRoomStatus(i,j) == 2:
                black_list.append([[i,j],3])

                update_list = check_if_in_room(room,update_list, not i - 1 < 0, i-1, j)[:]
                update_list = check_if_in_room(room,update_list, not j - 1 < 0, i,j-1)[:]
                update_list = check_if_in_room(room,update_list, not i > width, i+1,j)[:]
                update_list = check_if_in_room(room,update_list, not j > height, i,j+1)[:]

                #Extra checks for the diagonal positions
                if mode == "moore":
                    update_list = check_if_in_room(room,update_list, not (j > height) and not (i > width), i+1, j+1)[:]
                    update_list = check_if_in_room(room,update_list, not (i - 1 < 0) and not (j > height), i-1, j+1)[:]
                    update_list = check_if_in_room(room,update_list, not (i - 1 < 0) and not (j - 1 < 0), i-1, j-1)[:]
                    update_list = check_if_in_room(room,update_list, not (i > width) and not (j - 1 < 0), i+1, j-1)[:]

                        
    # Each element in the update list is filtered as to only keeping the unique elements
    for elem in update_list:
        if elem not in unique_update_list:
            unique_update_list.append(elem)

    # Here we change the tiles from forest tiles to burning tiles
    for pos in unique_update_list:
        # This checks if any of the burning cells reaches the other side( with height value 0)
        if pos[0][1] == 0:
            # Note first end_line encounter for fire cell, value 1 in first element means yes
            if len(end_line) == 0:
                end_line.append([1,t])

            if print_info == True:
                if first_fire_other_side == False:
                    print 'First fire reached the other side at t = %d'%t
                    first_fire_other_side = True

        # Actually updating the room
        room.cleanTileAtPosition(pos[0],pos[1])

    # Changing the burning cells to burned cells
    for pos in black_list:
        room.cleanTileAtPosition(pos[0],3)
        
    # If there is no fire anymore (thus the update list is empty)        
    if len(unique_update_list) == 0:
        # If here already is a element in the list which keeps track of the fact if the fire reached the end,
        # Append the status of the room to that element
        if len(end_line) == 1:
            end_line[0].append(room.getStatusCount(room,t))

        # If not so, registrate when the last fire is out and the status of the room
        elif len(end_line) == 0:
            end_line.append([0,t,room.getStatusCount(room,t)])

        if print_info == True:
            print 'All fires are out at t = %d'%t

    # Update the animation, if the function is set to true
    if PLOT_FIGURE == True:
        anim.update(room,black_list + unique_update_list)

    if SAVE_FIGURE:
        draw_object.update(room,black_list+unique_update_list)

    # Save the figure to the specified directory
    if SAVE_FIGURE:
        short_save_name = make_name(IMAGE_COUNTER,max_steps,SAVE_FIGURE_FORMAT)
        save_name = os.path.join(SAVE_FIGURE_LOCATION,short_save_name)
        draw_object.save_jpg(save_name)
        IMAGE_COUNTER += 1     

    # If the plot function is turned on, the status_list will be filled with statusses of the room with each timestep
    if plot == True:
        status_list.append(room.getStatusCount(room,t))
    
    # Update time iterator
    t += 1


# This plot function will plot the amount of tiles of each tile, dependant on the timestep(t). 
# While calling the simulation function this sub_function can be turned on, but it will be plotted after the animation
if plot == True:
    white_el    =   [el[0] for el in status_list]
    green_el    =   [el[1] for el in status_list]
    red_el      =   [el[2] for el in status_list]
    gray_el     =   [el[3] for el in status_list]
    time        =   [el[4] for el in status_list]

    plt.plot(time,white_el)
    plt.plot(time,green_el)
    plt.plot(time,red_el)
    plt.plot(time,gray_el)

    plt.xlabel("Time (t)")
    plt.ylabel("Number of cells, (N(t))")
    plt.legend(["White","Green","Red","Gray"],loc=0)
    plt.show()

###############################################################################################################
#End of simulation and wrapping up                                                                            #
###############################################################################################################

# End of animation
if PLOT_FIGURE == True:
    anim.done()

print "FINISHED"
if MAKE_GIFS:
    print "GENERATING GIF IMAGE"
    make_gif(SAVE_FIGURE_LOCATION, GIFS_LOCATION, GIF_NAME, FPS, GIF_PLOT_STEPS)
    print "DONE"

if DELETE_IMAGES_AFTER_GIF:
    delete_map_content(SAVE_FIGURE_LOCATION)