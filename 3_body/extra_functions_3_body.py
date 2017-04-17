import math

def check_total_inside_box(positions_list,x_lower_bound,x_upper_bound,y_lower_bound,y_upper_bound):
	#Loops over a list over positions and tests if any of these is out of bounds.
	for position in positions_list:
		val = check_inside_box(position,x_lower_bound,x_upper_bound,y_lower_bound,y_upper_bound)
		if not val == True:
			return False
	return True

def check_inside_box(position,x_lower_bound,x_upper_bound,y_lower_bound,y_upper_bound):
	#Checks whether the given position lies within the boundaries. 
	x_pos = position[0]
	y_pos = position[1]
	if x_pos < x_lower_bound:
		return  False
	if x_pos > x_upper_bound:
		return  False
	if y_pos < y_lower_bound:
		return  False
	if y_pos > y_upper_bound:
		return  False	 
	return True

def update_location(position_vector,velocity_vector,dt):
    new_position_vector = []
    for i in range(len(position_vector)):
        new_position_vector.append(position_vector[i] + velocity_vector[i] * dt)
    return new_position_vector

def calc_length_vector(vector):
	length_squared = 0
	for i in vector:
		length_squared += i**2
	length = math.sqrt(length_squared)
	return length

def calc_unit_vector(vector,vector_length):
	unit_vector = []
	for i in vector:
		unit_vector.append(float(i)/vector_length)
	return unit_vector

def calc_direction_vector(position_particle_1,position_particle_2):
	direction_vector = []
	for i in range(len(position_particle_1)):
		direction_vector.append(position_particle_1[i] - position_particle_2[i])
	return direction_vector

def calc_force(position_1,position_2,mass_1,mass_2, softening_length, power=2):
	#The power variable enables the user to modify the ..
	#Left the factor out, this is not for specific calculations, but more for general behaviour
	factor = 1
	direction_vector = calc_direction_vector(position_1, position_2)
	length_vector = calc_length_vector(direction_vector)
	unit_vector = calc_unit_vector(direction_vector, length_vector)
	force = factor * ((-mass_1 * mass_2) / pow(length_vector + softening_length, power))
	force_vector = []
	for i in direction_vector:
		force_vector.append(force * i)
	return force_vector
	
def sum_vectors(vector_list):
	result_vector = [0,0]
	for i in range(len(vector_list)):
		result_vector[0] += vector_list[i][0]
		result_vector[1] += vector_list[i][1]
	return result_vector

def calc_new_velocity(force,mass_test_particle,velocity_test_particle,dt):
	new_v = []
	old_v = velocity_test_particle
	accel = [force_el/mass_test_particle for force_el in force]
	for i in range(len(old_v)):
		new_v.append(old_v[i]+accel[i]*dt)

	return new_v

def generate_force_matrix(positions_list,masses_list,softening_length,power=2):
	forces_matrix = [[[0,0] for i in range(len(positions_list))] for i in range(len(positions_list))]
	total_forces_list = []
	for i in range(len(positions_list)):
		for j in range(len(positions_list)):
			if j > i:
				force_ij = calc_force(positions_list[i],positions_list[j],masses_list[i],masses_list[j],softening_length,power)
				force_ji = [-el for el in force_ij]
				forces_matrix[i][j] = force_ij
				forces_matrix[j][i] = force_ji

	for i in range(len(positions_list)):
		total_forces_list.append(sum_vectors(forces_matrix[i]))

	return total_forces_list