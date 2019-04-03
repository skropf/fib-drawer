"""
Copyright (C) 2019  Kropf Simon

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details. 

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import matplotlib
import Fibonacci as fib
import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3

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


from threading import Thread

def draw(start, end):
    inc = 1
    zFactor = 0
    alphaCube = 1
    alphaSpiral = 1
    for j in range(start, end):
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

        #if j > 215 and j <= 265:
        #    alphaCube = alphaCube - 0.02
        #    alphaSpiral = alphaSpiral + 0.02
        #if j > 555 and j <= 605:
        #    alphaCube = alphaCube + 0.02
        #    alphaSpiral = alphaSpiral - 0.02


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
        plt.savefig('moviePics/'+'{:04d}'.format(j)+'.png')
        #plt.show()
        plt.close(fig)




######################################
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys
import pyqtgraph as pg



app = QtGui.QApplication(sys.argv)
w = gl.GLViewWidget()
w.opts['distance'] = 40
w.setWindowTitle('pyqtgraph protein plot')
w.setGeometry(0, 110, 1920, 1080)
w.show()

# create the background grids
gx = gl.GLGridItem()
gx.rotate(90, 0, 1, 0)
gx.translate(-10, 0, 0)
w.addItem(gx)
gy = gl.GLGridItem()
gy.rotate(90, 1, 0, 0)
gy.translate(0, -10, 0)
w.addItem(gy)
gz = gl.GLGridItem()
gz.translate(0, 0, -10)
w.addItem(gz)

plot = gl.GLLinePlotItem(pos=np.array([[0,0], [1,1], [2,2]]))
plot.setData(pos=np.array([[1,1],[0,0],[4,3]]))
#data = fib.get_fibonacci_spiral(7, rotAngle=[0, 0, 180*2*np.pi/360], orientation='r', zFactor=100)
#for matrixList in data:
#    pts = [[round(x, 5) for x in matrixList[0]], [round(y, 5) for y in matrixList[1]], [round(z, 5) for z in matrixList[2]]]
#    print(pts)
#    array = np.array(pts)
#    plot.setData(pos=array, color=pg.glColor(1,50,50), mode='lines', antialias=True)

w.addItem(plot)
QtGui.QApplication.instance().exec_()
####################################

#thread1 = Thread(target=lambda: draw(0, 50))
#thread2 = Thread(target=lambda: draw(50, 100))
#thread3 = Thread(target=lambda: draw(100, 150))
#thread4 = Thread(target=lambda: draw(150, 200))
#thread5 = Thread(target=lambda: draw(200, 250))
#thread6 = Thread(target=lambda: draw(250, 300))
#thread7 = Thread(target=lambda: draw(300, 350))
#thread8 = Thread(target=lambda: draw(350, 400))
#thread9 = Thread(target=lambda: draw(400, 450))
#thread10 = Thread(target=lambda: draw(450, 500))
#thread11 = Thread(target=lambda: draw(500, 550))
#thread12 = Thread(target=lambda: draw(550, 600))
#thread13 = Thread(target=lambda: draw(600, 650))
#thread14 = Thread(target=lambda: draw(650, 700))
#thread15 = Thread(target=lambda: draw(700, 750))
#thread16 = Thread(target=lambda: draw(750, 800))
#
#thread1.start()
#thread2.start()
#thread3.start()
#thread4.start()
#thread5.start()
#thread6.start()
#thread7.start()
#thread8.start()
#thread9.start()
#thread10.start()
#thread11.start()
#thread12.start()
#thread13.start()
#thread14.start()
#thread15.start()
#thread16.start()










