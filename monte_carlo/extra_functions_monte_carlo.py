import random
import os

def gen_func(function, xmin, xmax, steps):
	L_x, L_y = [], []
	y_min,y_max = 10, 0
	dx = (xmax-xmin)/steps
	for i in range(steps):
		x = xmin + i * dx
		y = function(xmin + i *dx)
		L_x.append(x)
		L_y.append(y)
		if y > y_max:
			y_max = y
		if y < y_min: 
			y_min = y
	return [L_x,L_y,y_min,y_max]

def monte_carlo(function, xmin, xmax, ymin, ymax, steps):
    Dx, Dy = (xmax - xmin), (ymax - ymin)

    #Shape of result contents: [[x,y],bool:inside or outside]
    #If the random point is inside the function: value = 1, else 0
    results = []
    for i in range(steps):
        in_or_out = 0
        x_rand = random.random() * Dx + xmin
        y_rand = random.random() * Dy + ymin
        function_value = function(x_rand)
        if 0 < y_rand < function_value:
            in_or_out = 1
        elif function_value < y_rand < 0:
            in_or_out = 1
        results.append([[x_rand, y_rand], in_or_out])
    return results
