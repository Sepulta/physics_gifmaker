import images2gif
import os
import warnings
import numpy as np

from PIL import Image

#warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

def make_gif(image_location, gif_location, gif_name, fps, gif_plot_steps):
    print 'Make_gif function output:' 
    fig_dir             = image_location
    cwd                 = os.getcwd()

    images, images_temp                 = [],[]
    images_names, images_names_temp     = [],[]

    full_fig_dir        = os.path.join(cwd,image_location)
    full_gif_dir        = os.path.join(cwd,gif_location)
    
    print '\tReading images from "%s"'%str(full_fig_dir)
    content_image_directory = os.listdir(fig_dir)
    content_image_directory.sort()

    for fname in content_image_directory:
        images_temp.append(np.array(Image.open(os.path.join(fig_dir,fname))))
        images_names_temp.append(os.path.join(fig_dir, fname))

    # The user can choose per how many images the gif animation is made. This can reduce the size of the resulting animation.
    # The code below creates the list of indices to correctly do this.
    begin_indices = range(0, len(images_temp))
    if not gif_plot_steps == 1:
        effective_indices = range(0, len(images_temp), gif_plot_steps)
        if not begin_indices[-1] == effective_indices[-1]:
            effective_indices.append(begin_indices[-1])
    else:
        effective_indices = begin_indices[:]

    for index in effective_indices:
        images.append(images_temp[index])
        images_names.append(images_names_temp[index])

    #Get amount of images, to calculate length of gif
    amt_images = len(images)
    if not amt_images == 0:
        length_gif = float(amt_images)/float(fps)

        #Execute real gif making
        full_gif_file_path = os.path.join(full_gif_dir,gif_name+'.gif')
        print '\tGenerating GIF image: "%s" in directory: "%s"'%(str(full_gif_file_path),str(full_gif_dir))
        images2gif.writeGif(full_gif_file_path, images, duration=1.0/fps)