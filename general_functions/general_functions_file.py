import os
import sys
import random

def gen_random_color(lower_lim = 0, upper_lim = 1):
    #Generates random color tuple, in RGB: (R,G,B)
    return (random.random() * (upper_lim-lower_lim) + lower_lim,random.random() * (upper_lim-lower_lim) + lower_lim,random.random() * upper_lim-lower_lim + lower_lim)

def delete_map_content(target_directory):
    #Deletes all content of target directory
    cwd = os.getcwd()
    full_target_dir = os.path.join(cwd,target_directory)
    content_image_directory = os.listdir(full_target_dir)    
    print '\nDeleting files from "%s":'%str(full_target_dir)
    for fname in content_image_directory:
        full_path = os.path.join(full_target_dir,fname)
        os.remove(full_path)
        print '\tDeleted %s'%str(full_path)
    print 'Done'

def check_and_make(target_directory):
    #Checks if target directory is present. If not present, it makes the directory
    cwd = os.getcwd()
    new_dir = os.path.join(cwd, target_directory)
    if not os.path.isdir(new_dir):
        print '"%s" does not exist.\n\tMaking directory'%str(new_dir)
        os.makedirs(new_dir, 0755)
        print '\tDone'

def make_name(step,total_steps,formatting):
    #Generates names. Perhaps looks unnecessary but the format will be 0000x.jpg, and the zeros are needed for the sorting of the images
    short_name_string = str(step)
    len_current_step = len(short_name_string)
    len_total_steps = len(str(total_steps))

    missing_zeros = len_total_steps - len_current_step
    extra_string = ""
    for i in range(missing_zeros):
        extra_string = extra_string + "0"
        
    name_string = extra_string + short_name_string
    full_name_string = name_string + formatting

    return full_name_string
