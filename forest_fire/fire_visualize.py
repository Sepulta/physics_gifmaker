#This function is used to visualize the simulation. Not actually part of the asignment but nice to see.
#i wont comment this as nothing has to be done with this script

#This actually is a script from the course Voortgezet programmeren, which i adjusted to my means

import math
import time
import os

from Tkinter import *

from PIL import Image, ImageDraw, ImageFont

class FireVisualization:
    def __init__(self, width, height, room, mode, delay = 0.2):
        "Initializes a visualization with the specified parameters."
        # Number of seconds to pause after each frame
        self.delay = delay
        self.max_dim = max(width, height)
        self.width = width
        self.height = height
        self.mode = mode

        self.canvas_width = 500
        self.canvas_height = 600

        self.tile_width = 1
        self.tile_height = 1

        self.time = 0

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")

        #Parts for saving the image to jpg
#        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
#        self.draw = ImageDraw.Draw(self.image)

        #This color scheme represents the different states of the forest fire simulation, legend will follow
        self.tile_dir = {0:"white",1:"green",2:"red",3:"gray"}

        # Draw gray squares for dirty tiles
        self.tiles = []
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                self.tiles.append(self.w.create_rectangle(x1, y1, x2, y2,fill = self.tile_color(room.getRoomStatus(i,j))))

        # Draw gridlines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)

        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)
 
        # Draw some status text
        self.text = self.w.create_text(25, 0, anchor=NW,
                                       text=self._status_string(0,room.getStatusCount(room)))
        self.master.update()

    def _status_string(self, time, getStatusCount):
        tot_tiles = self.width*self.height
        "Returns an appropriate status string to print."
        percent_white = 100 * getStatusCount[0] / (tot_tiles)
        percent_green = 100 * getStatusCount[1] / (tot_tiles)
        percent_red = 100 * getStatusCount[2] / (tot_tiles)
        percent_gray = 100 * getStatusCount[3] / (tot_tiles)

        length_numbers = len(str(tot_tiles))
        format_number = "{:0%d}"%length_numbers
        info_string = "Time:\t%04d\tMode:\t%s\n"%(time,self.mode)
        info_string += "Width:\t%d\tHeight:\t%d\n"%(self.width,self.height)
        info_string += "White:\t%02d%%\t(%s)\n"%(percent_white, format_number.format(getStatusCount[0]))
        info_string += "Green:\t%02d%%\t(%s)\n"%(percent_green, format_number.format(getStatusCount[1]))
        info_string += "Red\t%02d%%\t(%s)\n"%(percent_red, format_number.format(getStatusCount[2]))
        info_string += "Gray:\t%02d%%\t(%s)"%(percent_gray, format_number.format(getStatusCount[3]))
        return info_string

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                325 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def tile_color(self,val):
        return self.tile_dir[val]

    def update(self, room, update_list, ):
        "Redraws the visualization with the specified room and forest state."
        # Removes a gray square for any tiles have been cleaned.
        for l in update_list:
            x1 = l[0][0]
            y1 = l[0][1]
            val = l[1]
            self.w.create_rectangle(self._map_coords(x1,y1)[0],\
                self._map_coords(x1, y1)[1],\
                self._map_coords(x1 + 1, y1 + 1)[0],\
                self._map_coords(x1 + 1, y1 + 1)[1],\
                fill= self.tile_color(val))
        # Update text
        self.w.delete(self.text)
        self.time += 1
        
        self.text = self.w.create_text(
            25, 0, anchor=NW,
            text=self._status_string(self.time,room.getStatusCount(room)))

        self.master.update()
        time.sleep(self.delay)

    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()
        

class FireToJPG:
    """
    This object is the object that saves the canvasses to images
    """
    def __init__(self, width, height, room, mode):
        "Initializes a visualization with the specified parameters."
        self.max_dim = max(width, height)
        self.width = width
        self.height = height
        self.mode = mode
        self.canvas_width = 500
        self.canvas_height = 600

        #Settings for text
        self.font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 16)
        self.textcolor = 'rgb(0,0,0)'
        self.textposition = (10,0)

        #This color scheme represents the different states of the forest fire simulation, legend will follow
        self.tile_dir = {0:"white",1:"green",2:"red",3:"gray"}

        #Parts for saving the image to jpg
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.time = 0

        # Draw gray squares for base color
        self.drawtiles = []
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                self.drawtiles.append(self.draw.rectangle((x1,y1,x2,y2),fill=self.tile_color(room.getRoomStatus(i,j)))) #tiles which are saved to the image

        # Draw gridlines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.draw.line((x1,y1,x2,y2),"black")   #Lines which are saved to the image

        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.draw.line((x1,y1,x2,y2),"black")   #Lines which are saved to the image

        # Draw some status text
        self.draw.text(self.textposition, self._status_string(self.time,room.getStatusCount(room)),fill=self.textcolor,font = self.font)
 
    def _status_string(self, time, getStatusCount):
        tot_tiles = self.width * self.height
        "Returns an appropriate status string to print."
        percent_white = 100 * getStatusCount[0] / (tot_tiles)
        percent_green = 100 * getStatusCount[1] / (tot_tiles)
        percent_red = 100 * getStatusCount[2] / (tot_tiles)
        percent_gray = 100 * getStatusCount[3] / (tot_tiles)

        length_numbers = len(str(tot_tiles))
        format_number = "{:0%d}"%length_numbers
        info_string = "Time:\t%04d\tMode:\t%s\n"%(time,self.mode)
        info_string += "Width:\t%d\tHeight:\t%d\n"%(self.width,self.height)
        info_string += "White:\t%02d%%\t(%s)\n"%(percent_white, format_number.format(getStatusCount[0]))
        info_string += "Green:\t%02d%%\t(%s)\n"%(percent_green, format_number.format(getStatusCount[1]))
        info_string += "Red:\t%02d%%\t(%s)\n"%(percent_red, format_number.format(getStatusCount[2]))
        info_string += "Gray:\t%02d%%\t(%s)"%(percent_gray, format_number.format(getStatusCount[3]))
        return info_string

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        ##NEED TO TWEAK THIS
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                325 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def tile_color(self,val):
        "This color scheme represents the different states of the forest fire simulation, legend will follow"
        return self.tile_dir[val]

    def update(self, room, update_list, ):
        "Redraws the visualization with the specified room and robot state."

        #Delete the draw object, in order to refresh the canvas
        del self.draw

        #Parts for saving the image to jpg
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.drawtiles = []

        for i in range(self.width):
            for j in range(self.height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                self.drawtiles.append(self.draw.rectangle((x1, y1, x2, y2), fill=self.tile_color(room.getRoomStatus(i, j))))

        for l in update_list:
            # Draw gridlines
            for i in range(self.width + 1):
                x1, y1 = self._map_coords(i, 0)
                x2, y2 = self._map_coords(i, self.height)
                self.draw.line((x1,y1,x2,y2),"black")   #Lines which are saved to the image

            for i in range(self.height + 1):
                x1, y1 = self._map_coords(0, i)
                x2, y2 = self._map_coords(self.width, i)
                self.draw.line((x1, y1, x2, y2),"black")   #Lines which are saved to the image

            self.draw.rectangle(
                (
                    self._map_coords(x1, y1)[0], self._map_coords(x1, y1)[1],
                    self._map_coords(x1 + 1, y1 + 1)[0], self._map_coords(x1 + 1, y1 + 1)[1]), 
                fill= self.tile_color(l[1]))

        # Update text
        self.time += 1

        textstringlist = self._status_string(self.time,room.getStatusCount(room)).replace('\t','    ').split('\n')
        for i in range(len(textstringlist)):
            self.draw.text((self.textposition[0],self.textposition[1]+i * 16), 
                textstringlist[i],fill=self.textcolor,font = self.font)

    def save_jpg(self,image_name):
        self.image.save(image_name)

    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()
