from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):
    toggle = pyqtSignal()

    def __init__(self, parent=None, width=50, height=50, dpi=100):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')

        self.axes.set_position([0, 0, 1, 1])
        self.fig.set_frameon = False
        self.axes.set_frameon = False

        self.fig.canvas.mpl_connect('button_press_event', self.click)

        super(MplCanvas, self).__init__(self.fig)
        super(MplCanvas, self).setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        super(MplCanvas, self).updateGeometry()

    def click(self, event):
        if event.dblclick:
            self.toggle.emit()


# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MplWidget, self).__init__(parent)   # Inherit from QWidget
        self.canvas = MplCanvas(parent, self.width(), self.height())  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.setAutoFillBackground(True)

        self.setParent(parent)

    def set_background(self, color):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(color))
        self.setPalette(p)
        self.canvas.fig.set_facecolor(color)
        self.canvas.axes.set_facecolor(color)

        self.canvas.draw()

    def open_fullscreen(self):
        manager = self.canvas.fig.canvas.manager
        manager.frame.Maximize(True)

    def draw_plot(self, data, legend, background, z_lim=None):
        for row in data:
            self.canvas.axes.scatter(row[0], row[1], row[2], c=row[3], marker=row[4])

        self.canvas.axes.set_xlabel('X')
        self.canvas.axes.set_ylabel('Y')
        self.canvas.axes.set_zlabel('Z')

        self.set_background(background)

        if z_lim:
            self.canvas.axes.set_zlim(*z_lim)

        if legend:
            self.canvas.axes.legend(handles=legend, loc='upper right')
        self.canvas.draw()
