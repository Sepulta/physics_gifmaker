import sys
import math
import random
import datetime
import os
import matplotlib.pyplot as plt


#Insert extra paths to be able to import functions from those directories
sys.path.insert(0, '../gif_maker')
sys.path.insert(0, '../general_functions')


from gif_maker_file import make_gif
from general_functions_file import check_and_make, make_name, delete_map_content
from extra_functions_diffusion import bounceoffeachother, divide_in_grid

#-------------------------------------------------------------------
# Goal:      Animate colliding balls in a box in Python (Matplotlib)
#            Example for course 'Inleiding programmeren' for the
#            University of Amsterdam (UvA) 
# Date:      August 2013, updated march 2017
# Author:    Ivo van Vulpen and David Hendriks
#
# TODO:      Exercises for physics students:
#              a) hole in the box: compute 50%-loss-time
#              b) piston from the right: temperature/pressure 
#-------------------------------------------------------------------


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

Nparticles              = 10     # USER PARAMETERS  number of normal balls
Nspecialparticles       = 4     # USER PARAMETERS  number of special balls
radius_ball             = 0.25  # USER PARAMETERS  [Note: ball 0 has different size and colour]
radius_ball_special     = 0.50  # USER PARAMETERS  (special ball 0)
color_ball              = 'b'   # USER PARAMETERS  Color of the normal balls
color_ball_special      = 'r'   # USER PARAMETERS  Color of the special balls
color_ball_edge         = 'k'   # USER PARAMETERS  Color of the balls' edge
ball_edge_size          = 1
simulation_steps        = 10   # How many simulation time iterations the animation will run
max_steps               = 10000 # For the names of the plots (000001.jpg)

generate_positions_randomly = True    # Setting to generate the positions randomly over the box
generate_positions_grid     = False    # Setting to generate the positions on a grid in the box
grid_setting                = 1       # 0 = line of balls, 1 = square of balls

#--/ define parameters of the box and figure
xmin_box                =  0
xmax_box                = 10
ymin_box                =  0
ymax_box                = 10

###############################################################################################################
#Simulation itself                                                                                            #
###############################################################################################################

Ntotalparticles         = Nparticles + Nspecialparticles
i_time                  = 0   # Initialize time
i_time_overlapping      = 0   # Initialize overlap time counter
start_colliding         = 0   # Set colliding flag to false

if generate_positions_randomly and generate_positions_grid:
  print "\n\nWARNING: YOU MUST CHOOSE ONE OF THE OPTIONS TO GENERATE POSITIONS, NOT BOTH (generate_positions_randomly=%s and generate_positions_grid=%s"%(generate_positions_randomly,generate_positions_grid)

#--------------------------------------------------------------------
# [1] initiate all particles (position, velocity and radius (==mass))
#--------------------------------------------------------------------
x  = []
y  = []
vx = []
vy = []
r  = []
circles = []

#Create figure with set dimensions, and equal axis lengths (this to have the circles remain their shapes)
plt.figure(figsize=(7,7))
ax = plt.gca()
ax.set_aspect('equal')

print ""
print "INITIALISING THE VECTORS: generate_positions_randomly=%s and generate_positions_grid=%s"%(generate_positions_randomly,generate_positions_grid)
print ""

#generate the positions randomly or with a grid function
if generate_positions_randomly:
  for i_particle in range(Ntotalparticles):
     #--/ position
     x_position = 2.50 # xmin_box + (xmax_box-xmin_box)*random() # 2.50 # np.random.uniform()
     y_position = 7.50 # xmin_box + (xmax_box-xmin_box)*random() # 7.50 # np.random.uniform()
     x.append(x_position)
     y.append(y_position)

     #--/ velocity and angle
     start_velocity = 0.05 + 0.05 * random.random() # 0.20                  # USER PARAMETERS
     start_angle    = 2 * math.pi * random.random()      # 2 * pi * float(i_particle)/float(Nparticles) # USER PARAMETERS
     x_velocity = start_velocity * math.cos(start_angle)
     y_velocity = start_velocity * math.sin(start_angle)       

     vx.append(x_velocity)
     vy.append(y_velocity)

     #Position the particles
     if(i_particle  < Nspecialparticles ):
        #First loop the amount of special particles to place them 
        placed = False

        #Try to place the new particle on a position where it doesnt overlap the other particle
        while placed == False:
          new_pos_x = xmin_box + radius_ball_special + random.random() * ((xmax_box - radius_ball_special) - (xmin_box + radius_ball_special))
          new_pos_y = ymin_box + radius_ball_special + random.random() * ((ymax_box - radius_ball_special) - (ymin_box + radius_ball_special))
          special_overlap = False
          
          #Check if the new proposed position overlaps with any other big ball
          for i_specialparticle in range(i_particle):
            if (math.sqrt(pow(x[i_specialparticle] - new_pos_x, 2) + pow(y[i_specialparticle] - new_pos_y, 2)) < 2 * radius_ball_special):
              special_overlap = True
          
          # And if it not overlaps, place it.
          if not special_overlap:
            x[i_particle] = new_pos_x
            y[i_particle] = new_pos_y
            vx[i_particle] = 0.00
            vy[i_particle] = 0.00
            r.append(radius_ball_special)
            placed = True
     else:
         r.append(radius_ball)

     #--/ create a circle
     if( i_particle < Nspecialparticles):
        circles.append(plt.Circle((x[i_particle], y[i_particle]), radius = r[i_particle], fc = color_ball_special))
     else:
        circles.append(plt.Circle((x[i_particle], y[i_particle]), radius = r[i_particle], fc = color_ball))

if generate_positions_grid:
  x,y = divide_in_grid(xmin_box, xmax_box, ymin_box, ymax_box, Nparticles, radius_ball, Nspecialparticles, radius_ball_special, 0.5, grid_setting)
  r = [radius_ball_special for i in range(Nspecialparticles)] + [radius_ball for j in range(Nparticles)]
  vx = [0 for i in range(Nspecialparticles)] + [(0.05 + 0.05 * random()) * math.cos(2 * math.pi * random()) for i in range(Nparticles)]
  vy = [0 for i in range(Nspecialparticles)] + [(0.05 + 0.05 * random()) * math.sin(2 * math.pi * random()) for i in range(Nparticles)]

  for i_particle in range(Ntotalparticles):
   #--/ create a circle
   if(i_particle < Nspecialparticles):
      circles.append(plt.Circle((x[i_particle], y[i_particle]), radius = r[i_particle], fc = color_ball_special))
   else:
      circles.append(plt.Circle((x[i_particle], y[i_particle]), radius = r[i_particle], fc = color_ball))

#Main loop, the first logical statement stops the simulation of the planned amount of real simulation steps are finished
#The second logical statement ensures that the simulations stops if it takes too long to place particles without overlap
while (i_time < simulation_steps) and (i_time + i_time_overlapping < max_steps):
    #--/ at time 0 initiate all circles on the screen at their locations
    if(i_time == 0):
      for i_particle in range(Ntotalparticles):
        circles[i_particle].center = (x[i_particle], y[i_particle])
    
    if start_colliding:
      #--/ printout for user to follow progress
      if(i_time%20 == 0):
        print "\tAnimation time-step %d\n" % i_time

    #-------------------------------------------------------------
    #--/ see when you can start colliding (no overlapping circles)
    #-------------------------------------------------------------
    if(start_colliding == 0): 
        overlaps = 0
        for i_particle in range(Ntotalparticles-1):
            xi, yi = circles[i_particle].center
            ri = r[i_particle]
            for j_particle in range(i_particle+1,Ntotalparticles):
                xj, yj = circles[j_particle].center
                rj = r[j_particle]
                dr = math.sqrt( math.pow(xi-xj,2) + math.pow(yi-yj,2) )
                if(dr < (ri+rj)):
                   overlaps += 1

        if(overlaps == 0):
           start_colliding = 1
           #print "\n  START COLLIDING\n"
        print "  overlap time = %d -> Number of overlaps = %d" % (i_time_overlapping,overlaps)
        
  
    #-----------------------------------------------------------
    #--/ [STEP 1] compute new position and velocity of the balls
    #-----------------------------------------------------------

    for i_particle in range(Ntotalparticles):
      #--/ get positions of the circle
      xi, yi = circles[i_particle].center
#      xi, yi = x[i_particle], y[i_particle]
      ri = r[i_particle]

      #------------------------------------------------------
      #--/ [A] compute new position and velocity of the balls
      #------------------------------------------------------
      x_new  =  x[i_particle] + vx[i_particle]
      y_new  =  y[i_particle] + vy[i_particle]
      vx_new =  vx[i_particle]
      vy_new =  vy[i_particle]

      #-------------------------------------------------------------
      #--/ [B] bounce off the walls
      #--/     correct the new positions if they move out of the box
      #-------------------------------------------------------------

      if(y_new+ri>  ymax_box):        # y_new+r = ymax - dr  => y_new = ymax - r - dr
          dr = y_new + ri - ymax_box          
          y_new = ymax_box - ri - dr
          vy_new = -1.*vy_new
      if(y_new-ri < ymin_box):        # y_new-r = ymin + dr  => y_new = ymin + r + dr        
          dr = ymin_box - (y_new - ri)
          y_new  = ymin_box + ri +dr
          vy_new = -1.*vy_new
      if(x_new+ri >  xmax_box):       # x_new+r = xmax - dr  => x_new = xmax - r - dr        
          dr = (x_new + ri) - xmax_box 
          x_new  =  xmax_box - ri - dr        
          vx_new = -1.*vx_new
      if(x_new-ri < xmin_box):        # x_new-r = xmin + dr  => x_new = xmin + r + dr        
          dr = xmin_box - (x_new - ri)        
          x_new  =  xmin_box + ri + dr        
          vx_new = -1.*vx_new

      #--/ update the positions and velocities of all particles
      x[i_particle]  = x_new
      y[i_particle]  = y_new
      vx[i_particle] = vx_new
      vy[i_particle] = vy_new


    #---------------------------------
    #--/ [STEP 2] bounce off eachother          
    #---------------------------------
    collided_particles = []

    if( start_colliding == 1 ):
      x_new = x
      y_new = y
      vx_new = vx
      vy_new = vy
    
      for i_particle in range(Ntotalparticles):
          x1 = x[i_particle] 
          y1 = y[i_particle] 
          r1 = r[i_particle] 

          for j_particle in range(i_particle+1,Ntotalparticles):
              x2 = x[j_particle] 
              y2 = y[j_particle] 
              r2 = r[j_particle] 

              #--/ check if they are close together
              dx = x1 - x2
              dy = y1 - y2
              dr = math.sqrt(math.pow(dx,2) + math.pow(dy,2) )

              #--/ compute new positions and velocities after collision
              if(dr < (r1+r2)):

                 #--/ save collided particles
                 collided_particles.append(i_particle)
                 collided_particles.append(j_particle)

                 m1  = math.pi*math.pow(r[i_particle],2)
                 v1x = vx[i_particle] 
                 v1y = vy[i_particle] 
                 m2  = math.pi*math.pow(r[j_particle],2)
                 v2x = vx[j_particle] 
                 v2y = vy[j_particle] 

                 x1_new, y1_new, v1x_new, v1y_new, x2_new, y2_new, v2x_new, v2y_new = \
                         bounceoffeachother(x1, y1, v1x, v1y, m1, r1, x2, y2, v2x, v2y, m2, r2)

                 #--/ save all values (particle 1 and particle 2)
                 x_new[i_particle]  = x1_new
                 y_new[i_particle]  = y1_new
                 vx_new[i_particle] = v1x_new
                 vy_new[i_particle] = v1y_new

                 x_new[j_particle]  = x2_new
                 y_new[j_particle]  = y2_new
                 vx_new[j_particle] = v2x_new
                 vy_new[j_particle] = v2y_new


      #----------------------------------------------------------------
      #--/ [STEP 3] copy new values of positions for collided particles
      #--/          update circle-centers
      #----------------------------------------------------------------
      Ncollided = len(collided_particles)
      for i_item in range(Ncollided):
          i_particle = int(collided_particles[i_item])
          x[i_particle] = x_new[i_particle]
          y[i_particle] = y_new[i_particle]
          vx[i_particle] = vx_new[i_particle]
          vy[i_particle] = vy_new[i_particle]
        
    #Initiate some plot settings
    if start_colliding:
      ax = plt.gca()
      ax.set_aspect('equal')
      plt.xlim(xmin_box,xmax_box)
      plt.ylim(ymin_box,ymax_box)

    #--/ update circle position
    for i_particle in range(Ntotalparticles):
        circles[i_particle].center = (x[i_particle], y[i_particle])
        if start_colliding:
          if i_particle < Nspecialparticles:
            circle=plt.Circle((x[i_particle],y[i_particle]),r[i_particle],fc=color_ball_special,ec=color_ball_edge)
            plt.gcf().gca().add_artist(circle)

          else:
            circle=plt.Circle((x[i_particle],y[i_particle]),r[i_particle],fc=color_ball,ec=color_ball_edge)
            plt.gcf().gca().add_artist(circle)

    # Draw textbox and text
    if start_colliding:
      if PLOT_FIGURE:
        plt.draw()
        plt.pause(PLOT_PAUSE_TIME)

    if start_colliding:
      if SAVE_FIGURE:
        short_save_name = make_name(IMAGE_COUNTER,max_steps,SAVE_FIGURE_FORMAT)
        save_name = os.path.join(SAVE_FIGURE_LOCATION,short_save_name)
        plt.savefig(save_name,bbox_inches='tight', quality = PLOT_QUALITY)
        IMAGE_COUNTER += 1
    if start_colliding:
      #Clear canvas
      plt.clf()


    #Only really increase time if the 'start_colliding' settings is True, else increase the time for which there are overlaps
    if start_colliding:
      i_time += 1
    else:
      i_time_overlapping += 1

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