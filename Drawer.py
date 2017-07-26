"""
Copyright (C) 2016  Kropf Simon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import matplotlib
import Fibonacci as fib
import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
from osgeo._gdal import MajorObject_GetMetadataItem

def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/3
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

def draw_fibonacci_pyramid(level):
    pyramid = fib.get_fibonacci_pyramid(level)

    for level in pyramid:
        print(level)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    xlist = []
    ylist = []
    zlist = []
    data = []

    xlist.append(0.0)
    ylist.append(0.0)
    zlist.append(0.0)

    indentStep = 2

    for level in range(2, pyramid.maxlen + 1):
        for i in range(level):
            for j in range(level):
                if level % 2 == 1:
                    center = math.floor(level / 2)
                if level % 2 == 0:
                    center = (level / 2) - 0.5

                xlist.append((i - center) * indentStep)
                ylist.append((j - center) * indentStep)
                zlist.append(level - 1)

    for level in range(pyramid.maxlen):
        for i in range(level + 1):
            for j in range(level + 1):
                data.append(pyramid[level][i][j])

    ax.scatter(xlist, ylist, zlist, zdir='z', marker=None)

    i = 0
    for x, y, z in zip(xlist, ylist, zlist):
        ax.text(x, y, z, str(data[i]), color="red", fontsize=8)
        i = i + 1

    plt.show()

def draw_fibonacci_spiral(level, rotAngle = [0, 0, 0], orientation = 'r', zFactor = 0, offsetX = 0, offsetY = 0, color='black', alpha=1):
    data = fib.get_fibonacci_spiral(level, rotAngle, orientation, zFactor)
    
    if alpha != 0:
        for matrixList in data:
            ax.plot([x + offsetX for x in matrixList[0]], [y + offsetY for y in matrixList[1]], matrixList[2], color=color, alpha=alpha)


def draw_fibonacci_cubes(level, rotAngle = [0, 0, 0], orientation = 'r', zFactor = 0, offsetX = 0, offsetY = 0, color='black', alpha=1):
    cubes = fib.get_fibonacci_cubes(level, rotAngle, orientation, zFactor)
    
    if alpha != 0:
        for cube in cubes:
            for line in cube:
                ax.plot3D([x + offsetX for x in line[0]], [y + offsetY for y in line[1]], line[2], color=color, alpha=alpha)

##########################



def gen_fibonacci_spiral(level, rotAngle = [0, 0, 0], orientation = 'r', zFactor = 0, offsetX = 0, offsetY = 0, color='black', alpha=1):
    data = fib.get_fibonacci_spiral(level, rotAngle, orientation, zFactor)
    return data






def update_lines(num, index, data, lines):
    lines = [ax.plot(line[0], line[1], line[2], color='black')[0] for line in data[num]]
    return lines

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Fifty lines of random 3-D lines
data = [gen_fibonacci_spiral(7, rotAngle = [0, 0, index*2*2*np.pi/360]) for index in range(360)]

# Creating fifty line objects.
# NOTE: Can't pass empty arrays into 3d version of plot()
#lines = [ax.plot(line[0], line[1], line[2])[0] for line in data[0]]
lines=[]
# Setting the axes properties
ax.set_xlim3d([-23, 23])
ax.set_xlabel('X')

ax.set_ylim3d([-23, 23])
ax.set_ylabel('Y')

ax.set_zlim3d([-20, 20])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, fargs=(0, data, lines),
                                   interval=50, blit=True)

plt.show()



"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

draw_fibonacci_cubes(7, zFactor=100, color="b")
draw_fibonacci_spiral(7, zFactor=100, color="b")
draw_fibonacci_cubes(7, zFactor=100, rotAngle=math.pi/2, color="r")
draw_fibonacci_spiral(7, zFactor=100, rotAngle=math.pi/2, color="r")
draw_fibonacci_cubes(7, zFactor=100, rotAngle=math.pi, color="g")
draw_fibonacci_spiral(7, zFactor=100, rotAngle=math.pi, color="g")
draw_fibonacci_cubes(7, zFactor=100, rotAngle=math.pi/2*3, color="c")
draw_fibonacci_spiral(7, zFactor=100, rotAngle=math.pi/2*3, color="c")


axisEqual3D(ax)
plt.show()
plt.close(fig)
"""
"""
inc = 1
zFactor = 100
for j in range(0, 720):
    print(str(j))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.axis('off')
    ax.set_xlim3d(-23,23)
    ax.set_ylim3d(-23,23)
    ax.set_zlim3d(-20,20)

    zFactor = zFactor + inc
    if zFactor >= 100: inc = -1
    elif zFactor <= -100: inc = 1
    
    draw_fibonacci_cubes(7, zFactor=zFactor, rotAngle=-j*2*np.pi/360, color="blue")
    draw_fibonacci_spiral(7, zFactor=zFactor, rotAngle=-j*2*np.pi/360, color="black")
    #draw_fibonacci_cubes(7, zFactor=zFactor, rotAngle=j*2*np.pi/360+math.pi/2, color="r")
    #draw_fibonacci_spiral(7, zFactor=zFactor, rotAngle=j*2*np.pi/360+math.pi/2, color="r")
    draw_fibonacci_cubes(7, zFactor=-zFactor, rotAngle=j*2*np.pi/360+math.pi, color="red")
    draw_fibonacci_spiral(7, zFactor=-zFactor, rotAngle=j*2*np.pi/360+math.pi, color="black")
    #draw_fibonacci_cubes(7, zFactor=zFactor, rotAngle=j*2*np.pi/360+math.pi/2*3, color="c")
    #draw_fibonacci_spiral(7, zFactor=zFactor, rotAngle=j*2*np.pi/360+math.pi/2*3, color="c")

    #axisEqual3D(ax)
    plt.savefig('moviePics/'+'{:04d}'.format(j)+'.png')
    #plt.show()
    plt.close(fig)

"""
"""
#doublecrossanim-color
zFactor = 0
step = -4.44444444
for i in range(0,720):
    print(str(i) + ": " + str(zFactor) + "(" + str(step) + ")")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.axis('off')
    ax.view_init(elev=45., azim=0)
    ax.set_xlim3d(-13,13)
    ax.set_ylim3d(-13,13)
    ax.set_zlim3d(-32,32)


    if i <= 45 and i % 45 == 0:
        step = step * (-1)
    elif (i + 45) % 90 == 0:
        step = step * (-1)

    zFactor = zFactor + step

    draw_fibonacci_spiral(7, (-i*4+0)*2*np.pi/360, 'r', zFactor, color='#FF0000')
    draw_fibonacci_spiral(7, (-i*4+120)*2*np.pi/360, 'r', zFactor, color='#FF0000')
    draw_fibonacci_spiral(7, (-i*4+240)*2*np.pi/360, 'r', zFactor, color='#FF0000')
    draw_fibonacci_spiral(7, (-i*4+60)*2*np.pi/360, 'r', zFactor, color='#FF0000')
    draw_fibonacci_spiral(7, (-i*4+180)*2*np.pi/360, 'r', zFactor, color='#FF0000')
    draw_fibonacci_spiral(7, (-i*4+300)*2*np.pi/360, 'r', zFactor, color='#FF0000')
    draw_fibonacci_cubes(7, (-i*4+0)*2*np.pi/360, 'r', zFactor, color='#00FFFF')
    draw_fibonacci_cubes(7, (-i*4+120)*2*np.pi/360, 'r', zFactor, color='#00FFFF')
    draw_fibonacci_cubes(7, (-i*4+240)*2*np.pi/360, 'r', zFactor, color='#00FFFF')
    draw_fibonacci_cubes(7, (-i*4+60)*2*np.pi/360, 'r', zFactor, color='#00FFFF')
    draw_fibonacci_cubes(7, (-i*4+180)*2*np.pi/360, 'r', zFactor, color='#00FFFF')
    draw_fibonacci_cubes(7, (-i*4+300)*2*np.pi/360, 'r', zFactor, color='#00FFFF')

    draw_fibonacci_spiral(7, (i*4+0)*2*np.pi/360, 'l', -zFactor, color='#00FF00')
    draw_fibonacci_spiral(7, (i*4+120)*2*np.pi/360, 'l', -zFactor, color='#00FF00')
    draw_fibonacci_spiral(7, (i*4+240)*2*np.pi/360, 'l', -zFactor, color='#00FF00')
    draw_fibonacci_spiral(7, (i*4+60)*2*np.pi/360, 'l', -zFactor, color='#00FF00')
    draw_fibonacci_spiral(7, (i*4+180)*2*np.pi/360, 'l', -zFactor, color='#00FF00')
    draw_fibonacci_spiral(7, (i*4+300)*2*np.pi/360, 'l', -zFactor, color='#00FF00')
    draw_fibonacci_cubes(7, (i*4+0)*2*np.pi/360, 'l', -zFactor, color='#FF00FF')
    draw_fibonacci_cubes(7, (i*4+120)*2*np.pi/360, 'l', -zFactor, color='#FF00FF')
    draw_fibonacci_cubes(7, (i*4+240)*2*np.pi/360, 'l', -zFactor, color='#FF00FF')
    draw_fibonacci_cubes(7, (i*4+60)*2*np.pi/360, 'l', -zFactor, color='#FF00FF')
    draw_fibonacci_cubes(7, (i*4+180)*2*np.pi/360, 'l', -zFactor, color='#FF00FF')
    draw_fibonacci_cubes(7, (i*4+300)*2*np.pi/360, 'l', -zFactor, color='#FF00FF')

    plt.savefig('moviePics/'+'{:04d}'.format(i)+'.png')
    #plt.show()    
    plt.close(fig)

"""
"""flat 2x12 opposite direction anim
for rot in range(360):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.axis('off')

    print(rot)
    
    for i in range(12):
        draw_fibonacci_spiral_offset(4, -rot + i*2*np.pi/12, 'l')
        draw_fibonacci_spiral_offset(4, rot + i*2*np.pi/12, 'r')

    ax.view_init(elev=90., azim=0)
    axisEqual3D(ax)
    plt.savefig('moviePics/'+'{:04d}'.format(rot)+'.png')
    plt.close(fig)
"""
"""
inc = 1
zFactor = 0
alphaCube = 1
alphaSpiral = 0
for j in range(0, 1):
    print(str(j))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.axis('off')
    ax.set_xlim3d(-23,23)
    ax.set_ylim3d(-23,23)
    ax.set_zlim3d(-20,20)

    zFactor = zFactor + inc
    if zFactor >= 100: inc = -1
    elif zFactor <= -100: inc = 1
    
    if j > 215 and j <= 265:
        alphaCube = alphaCube - 0.02
        alphaSpiral = alphaSpiral + 0.02
    if j > 555 and j <= 605:
        alphaCube = alphaCube + 0.02
        alphaSpiral = alphaSpiral - 0.02
    

    draw_fibonacci_spiral(7, zFactor=zFactor, rotAngle=[0, 0, j*2*np.pi/360], color="blue", alpha=alphaSpiral)
    draw_fibonacci_spiral(7, zFactor=zFactor, rotAngle=[math.pi/2, 0, j*2*np.pi/360], color="red", alpha=alphaSpiral)
    draw_fibonacci_spiral(7, zFactor=zFactor, rotAngle=[0, math.pi/2, j*2*np.pi/360], color="green", alpha=alphaSpiral)
        
    draw_fibonacci_spiral(7, zFactor=-zFactor, rotAngle=[0, 0, (j+180)*2*np.pi/360], color="blue", alpha=alphaSpiral)
    draw_fibonacci_spiral(7, zFactor=-zFactor, rotAngle=[math.pi/2, 0, (j+180)*2*np.pi/360], color="red", alpha=alphaSpiral)
    draw_fibonacci_spiral(7, zFactor=-zFactor, rotAngle=[0, math.pi/2, (j+180)*2*np.pi/360], color="green", alpha=alphaSpiral)


    draw_fibonacci_cubes(7, zFactor=zFactor, rotAngle=[0, 0, j*2*np.pi/360], color="blue", alpha=alphaCube)
    draw_fibonacci_cubes(7, zFactor=zFactor, rotAngle=[math.pi/2, 0, j*2*np.pi/360], color="red", alpha=alphaCube)
    draw_fibonacci_cubes(7, zFactor=zFactor, rotAngle=[0, math.pi/2, j*2*np.pi/360], color="green", alpha=alphaCube)
        
    draw_fibonacci_cubes(7, zFactor=-zFactor, rotAngle=[0, 0, (j+180)*2*np.pi/360], color="blue", alpha=alphaCube)
    draw_fibonacci_cubes(7, zFactor=-zFactor, rotAngle=[math.pi/2, 0, (j+180)*2*np.pi/360], color="red", alpha=alphaCube)
    draw_fibonacci_cubes(7, zFactor=-zFactor, rotAngle=[0, math.pi/2, (j+180)*2*np.pi/360], color="green", alpha=alphaCube)
    
    #axisEqual3D(ax)
    #plt.savefig('moviePics/'+'{:04d}'.format(j)+'.png')
    plt.show()
    plt.close(fig)
"""
    
