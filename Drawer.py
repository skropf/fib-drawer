import Fibonacci as fib
import numpy as np

from PyQt6 import QtWidgets
import pyqtgraph.opengl as gl

# Always start by initializing Qt (only once per application)
app = QtWidgets.QApplication([])

view = QtWidgets.QWidget()
view.setWindowTitle('Fibonacci spiral')
view.setGeometry(0, 110, 1920, 1080)

plot_widget = gl.GLViewWidget()
plot_widget.setBackgroundColor("#FFFFFF")

layout = QtWidgets.QGridLayout()
view.setLayout(layout)
layout.addWidget(plot_widget)

points = []
points.append(fib.get_fibonacci_spiral(13, rotAngle=[0, 0, 0*2*np.pi/360], orientation='r', zFactor=0, segments=16))
points.append(fib.get_fibonacci_spiral(13, rotAngle=[0, 0, 120*2*np.pi/360], orientation='r', zFactor=0, segments=16))
points.append(fib.get_fibonacci_spiral(13, rotAngle=[0, 0, 240*2*np.pi/360], orientation='r', zFactor=0, segments=16))
points.append(fib.get_fibonacci_spiral(13, rotAngle=[0, 0, 0*2*np.pi/360], orientation='l', zFactor=0, segments=16))
points.append(fib.get_fibonacci_spiral(13, rotAngle=[0, 0, 120*2*np.pi/360], orientation='l', zFactor=0, segments=16))
points.append(fib.get_fibonacci_spiral(13, rotAngle=[0, 0, 240*2*np.pi/360], orientation='l', zFactor=0, segments=16))


for i in range(6):
    if i == 0 or i == 4: r, g, b = 1, 0, 0
    if i == 1 or i == 5: r, g, b = 0, 1, 0
    if i == 2 or i == 6: r, g, b = 0, 0, 1
    if i == 3 or i == 7: r, g, b = 0, 0, 0

    plot = gl.GLLinePlotItem()
    plot.setGLOptions('opaque')
    plot.setData(pos=points[i], color=[r, g, b, 1], mode='line_strip', antialias=True)
    plot_widget.addItem(plot)

view.show()
app.exec()

# create the background grids
#gx = gl.GLGridItem()
#gx.rotate(90, 0, 1, 0)
#gx.translate(-10, 0, 0)
#gx.setColor("#000000")
#plot_widget.addItem(gx)
#gy = gl.GLGridItem()
#gy.rotate(90, 1, 0, 0)
#gy.translate(0, -10, 0)
#gy.setColor("#000000")
#plot_widget.addItem(gy)
#gz = gl.GLGridItem()
#gz.translate(0, 0, -10)
#gz.setColor("#000000")
#plot_widget.addItem(gz)