README:
This project contains a set of scripts to visualize physics and mathematics and turn them into GIF images. 
Most of the code is written by David Hendriks (davidhendriks93@gmail.com). 

This project was executed under the supervision of Ivo van Vulpen, who thought of the idea to make a python based GIF generator for physics based simulations.
These GIFs can be used for educational purposes or just for fun. 

Ivo recieved a GrassRoots grant from the University of Amsterdam, by which this project was made possible. They recognized the educational benefits of simple GIF animations of physics processes, which at times are quite hard to visualize yourself. 

In the simulation_template directory, a template script is present in which the general outline of the files is shown. 

There are ofcourse a lot more simulations that one can think of to visualize, and I'm always open for new ideas, but for now it is limited to a couple of simulations:
- 3-body simulation (can be made N-body): gravitational interaction of particles
- Rutherford scattering: visualization of rutherford scattering with a fixed particle and a test particle. The power to which the acting force is proportional to can be adjusted. 
- Monte carlo simulation: A visual representation of montecarlo integration
- Forest fire simulation: A grid based simulation where tiles represent patches of forest or non-burnable ground. I made this in order to analyze with what percentage of burnable tiles the fire would reach the other side of the grid.
- Diffusion simulation: A simulation in which balls represent molecules which undergo kinetic interaction and visualize the process of diffusion. One can configure the initial positions to either randomly positioned particles, or particles placed in certain formations like lines and squares. 

This project uses a couple of extra python modules apart from the standard included packages. 
The gif maker scripts use the PIL library (http://www.pythonware.com/products/pil/) to process images. 

Necessary imports per simulation project:
- Globally used packages: sys, math, matplotlib, os, time, datetime
- Diffusion: random
- Rutherford: no extra packages
- 3 body: random
- Monte carlo: random
- Forestfire: random, Tkinter, PIL, operator
- Gif maker: warnings, numpy, PIL

For linux users, these packages are easy to install using pip (https://docs.python.org/2/installing/)
The same can be used for MAC systems, and possibly with windows systems (but I haven't tried that)

This code has not been thoroughly tested on operating systems other than Linux Ubuntu 14.04, and I've already noticed that mac d


For the GIF maker, code written by third parties is used, which has the copyright:
Copyright (C) 2012, Almar Klein, Ant1, Marius van Voorden
This code is subject to the (new) BSD license:

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
- Neither the name of the organization nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

For questions, comments or tips regarding the code or the simulations themselves, send me an email (davidhendriks93@gmail.com)