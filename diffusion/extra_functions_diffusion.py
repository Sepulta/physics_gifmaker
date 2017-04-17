from math import *
import numpy as np

def make_grid(input_amount):
  if input_amount < 4:
    result = list(np.ndindex(2,2))[:input_amount]
  else:
    root = sqrt(input_amount)
    if root%1 == 0:
      result = list(np.ndindex(root,root))
    else:
      floored = floor(root)
      ceiled = ceil(root)
      result_1 = list(np.ndindex(floored,floored))
      result_2 = list(np.ndindex(ceiled,ceiled))
      difference = [el for el in result_2 if not el in result_1]
      result = result_1 + difference[:input_amount -len(result_1)]
  return result


def divide_in_grid(x_min, x_max, y_min, y_max, number_small_particles, size_small_particles, number_big_particles, size_big_particles, spacing, setting):
  #Setting: 0 = square
  #Setting: 1 = line
  if not (setting == 0 or setting == 1):
    print 'Wrong settings'
    return None

  #Make grid_list
  grid_points               = []
  position_big_particles    = []
  position_small_particles  = []

  spacing = size_big_particles
  Dx = (x_max-spacing) - (x_min+spacing)
  Dy = (y_max-spacing) - (y_min+spacing)

  #Put in big particles
  amount_big_x = (Dx-4*spacing/(size_big_particles*2))
  amount_big_x = (Dx-4*spacing/(size_big_particles*2))

  layer_big = 0
  layer_small = 0

  if setting == 0:
 #   spacing = size_big_particles
    Dx = (x_max-spacing) - (x_min+spacing)
    Dy = (y_max-spacing) - (y_min+spacing)
    x_b = 2*spacing
    y_b = y_max - 2*spacing
    for i in range(0,number_big_particles):
      if x_b >= Dx:
        layer_big += 1
        x_b = 2 * spacing
        y_b = y_max - 2*spacing - layer_big*(2*size_big_particles+spacing)
      position_big_particles.append([x_b,y_b])
      x_b += (2*size_big_particles+spacing)

    #Part for the small particles
    spacing = size_small_particles

    x_s = 2 * spacing
    y_s = y_min + 2* spacing
    for j in range(0,number_small_particles):
      if x_s >= Dx:
        layer_small += 1
        x_s = 2 * spacing
        y_s = y_min + 2*spacing + layer_small*(2*size_small_particles+spacing)
      position_small_particles.append([x_s,y_s])
      x_s += (2*size_small_particles+spacing)


  elif setting == 1:

    position_small_particles = make_grid(number_small_particles)
    position_small_particles = [[x_max - 2 * size_small_particles - el[0]*3*size_small_particles,y_min + 2 * size_small_particles + el[1]*3*size_small_particles] for el in position_small_particles]   

    position_big_particles = make_grid(number_big_particles)
    position_big_particles = [[x_min + 2 * size_big_particles + el[0]*3*size_big_particles, y_max - 2 * size_big_particles - el[1] *3* size_big_particles] for el in position_big_particles]

  #Check if any small particle overlaps with big particle:
  overlap = False
  outside = False
  for pos_small in position_small_particles:
    for pos_big in position_big_particles:
      if sqrt(pow(pos_small[0]-pos_big[0],2)+pow(pos_small[1]-pos_big[1],2)) < size_big_particles + size_small_particles:
        overlap = True
  for pos_small in position_small_particles:
    if pos_small[0] > x_max or pos_small[0] < x_min or pos_small[1] > y_max or pos_small[1] < y_min:
      outside = True
  for pos_big in position_big_particles:
    if pos_big[0] > x_max or pos_big[0] < x_min or pos_big[1] > y_max or pos_big[1] < y_min:
      outside = True 


  if overlap == True:
    print 'There is overlap in the generated positions of the particles.\nIt is recommended that you reduce the amount of particles in order to generate a grid with no overlap.\nReturning None.'
    return None
  if outside == True:
    print 'Something went wrong: a particle has been placed outside the box.\nIt is recommended that you reduce the amount of particles in order to generate a correct grid.\nReturning None.'
    return None
  else:
    print 'modifying lists to correct shape.'


  x_list = [el[0] for el in position_big_particles + position_small_particles]
  y_list = [el[1] for el in position_big_particles + position_small_particles]

  return x_list,y_list

#--------------------------------------------------------------------------
def bounceoffeachother(x1, y1, v1x, v1y, m1, r1, x2, y2, v2x, v2y, m2, r2):
#--------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    #--/ Goal:      compute new velocity and direction after a collision of 2 balls        
    #
    #--/ Strategy:  http://www.vobarian.com/collisions/2dcollisions2.pdf
    #
    #--/ Extra:     1) try to determine exact time of collision     
    #               2) collide balls at moment and update velocity (directions)
    #               3) move balls by remainder of time-step to new positions
    #------------------------------------------------------------------------------

    #-------------------------------------------------------------
    #--/ [1] try to determine the exact collision point (and time)
    #-------------------------------------------------------------

    #--/ previous position
    x1_old = x1 - v1x
    y1_old = y1 - v1y
    x2_old = x2 - v2x
    y2_old = y2 - v2y
    dx_old = x1_old - x2_old
    dy_old = y1_old - y2_old   
    dr_old = sqrt( pow(dx_old,2) + pow(dy_old,2) )

    #--/ current position
    dx_current = x1 - x2
    dy_current = y1 - y2
    dr_current = sqrt( pow(dx_current,2) + pow(dy_current,2) )

    #--/ time of collision (rough linear guess)
    dr_collision   = r1+r2   
    time_until_collision = (dr_old-dr_collision)/(dr_old-dr_current)
    time_after_collision = 1- time_until_collision    
    if(time_until_collision < 0): print "ERROR in bounceoffeachother() -> time_collision < 0"

    #print "  previous: (%.2f,%.2f) vs (%.2f,%.2f) -> dr = %.2f" % (x1_old,y1_old,x2_old,y2_old,dr_old)
    #print "  current:  (%.2f,%.2f) vs (%.2f,%.2f) -> dr = %.2f" % (x1,y1,x2,y2,dr_current)
    #print "  time until/after collision = %.2f/%.2f" % (time_until_collision, time_after_collision)

    #--/ compute new positions at time of collision
    x1 = x1_old + time_until_collision * v1x  
    y1 = y1_old + time_until_collision * v1y 
    x2 = x2_old + time_until_collision * v2x  
    y2 = y2_old + time_until_collision * v2y  

    #print "  collision:  (%.2f,%.2f) vs (%.2f,%.2f) -> dr = %.2f" % (x1,y1,x2,y2,dr)

    #---------------------------------------------
    #--/ [2] start computation of actual collision
    #---------------------------------------------

    #--/ positions at time of collisions
    dx = x1 - x2
    dy = y1 - y2
    dr = sqrt( pow(dx,2) + pow(dy,2) )

    #--/ compute (normalised) vectors normal and perpendicular to collision direction
    norm_x = (x2-x1) / sqrt(pow(dx,2)+pow(dy,2))
    norm_y = (y2-y1) / sqrt(pow(dx,2)+pow(dy,2))
    perp_x = -1.*norm_y       
    perp_y = norm_x
       
    #--/ project the velocities of each ball onto normal and perpendicular directions
    v1_proj_norm = v1x*norm_x + v1y*norm_y
    v1_proj_perp = v1x*perp_x + v1y*perp_y

    v2_proj_norm = v2x*norm_x + v2y*norm_y
    v2_proj_perp = v2x*perp_x + v2y*perp_y

    #--/ in perpendicular directions velocities stay the same
    v1_proj_perp_new = v1_proj_perp
    v2_proj_perp_new = v2_proj_perp

    #--/ in normal directions change according to 1d formula
    #--/ Note: students should compute this themselves (not difficult, but a bit tedious)
    v1_proj_norm_new = ((m1 - m2) * v1_proj_norm + 2 * m2 * v2_proj_norm) /(m1 + m2)
    v2_proj_norm_new = ((m2 - m1) * v2_proj_norm + 2 * m1 * v1_proj_norm) /(m1 + m2)

    #--/ project the velocities again on the 'normal' x/y-axes
    v1x_new =  v1_proj_norm_new * norm_x + v1_proj_perp_new * perp_x
    v1y_new =  v1_proj_norm_new * norm_y + v1_proj_perp_new * perp_y
    v2x_new =  v2_proj_norm_new * norm_x + v2_proj_perp_new * perp_x
    v2y_new =  v2_proj_norm_new * norm_y + v2_proj_perp_new * perp_y

    #---------------------------------------------
    #--/ [3] compute new positions after collision    
    #---------------------------------------------

    #--/ compute the new positions of the particles after the collision
    x1_new = x1 + time_after_collision * v1x_new  
    y1_new = y1 + time_after_collision * v1y_new 
    x2_new = x2 + time_after_collision * v2x_new
    y2_new = y2 + time_after_collision * v2y_new

    return x1_new, y1_new, v1x_new, v1y_new, x2_new, y2_new, v2x_new, v2y_new