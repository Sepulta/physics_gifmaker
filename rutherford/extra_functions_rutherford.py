import math

def check_inside_box(position,x_lower_bound,x_upper_bound,y_lower_bound,y_upper_bound):
	x_pos = position[0]
	y_pos = position[1]
	if x_pos < x_lower_bound:
		return False
	if x_pos > x_upper_bound:
		return False
	if y_pos < y_lower_bound:
		return False
	if y_pos > y_upper_bound:
		return False
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

def calc_force(position_test_particle,position_fixed_particle,charge_test_particle,charge_fixed_particle,power=2):
	#The power variable enables the user to modify the ..
	#Left the factor out, this is not for specific calculations, but more for general behaviour
#	factor = (1.0/4*math.pi*)
	factor = 1
	direction_vector = calc_direction_vector(position_test_particle,position_fixed_particle)
	length_vector = calc_length_vector(direction_vector)
	unit_vector = calc_unit_vector(direction_vector,length_vector)
	force = factor*((charge_fixed_particle * charge_test_particle) / pow(length_vector, power))
	force_vector = []
	for i in direction_vector:
		force_vector.append(force * i)
	return force_vector

def calc_new_velocity(force,mass_test_particle,velocity_test_particle,dt):
	new_v = []
	old_v = velocity_test_particle
	accel = [force_el / mass_test_particle for force_el in force]
	for i in range(len(old_v)):
		new_v.append(old_v[i] + accel[i] * dt)
	return new_v