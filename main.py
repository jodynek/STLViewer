#!/usr/bin/env python

import sys

import vtk
from PyQt5 import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MainWindow(Qt.QMainWindow):
    reader = vtk.vtkSTLReader()

    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)

        self.initUI()

    # GUI definition
    def initUI(self):
        # actions definition
        openFile = Qt.QAction(Qt.QIcon('icons/open-24.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open STL File')
        openFile.triggered.connect(self.showSTLFileDialog)

        exitAction = Qt.QAction(Qt.QIcon('icons/close-window-24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        # display statusbar
        self.statusBar()

        # display menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAction)

        # display toolbar
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(openFile)
        toolbar.addAction(exitAction)

        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.iren.Initialize()
        self.iren.Start()

        # load default STL
        filename = "Skull.stl"
        self.loadSTL(filename)

        # set main window
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Simple STL Viewer')
        self.show()

    # load STL file
    def loadSTL(self, filename):
        # Create source
        self.reader.SetFileName(filename)

        transform = vtk.vtkTransform()
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetTransform(transform)
        transformFilter.SetInputConnection(self.reader.GetOutputPort())
        transformFilter.Update()

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.reader.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.ren.AddActor(actor)
        self.ren.ResetCamera()

    # display STL file selection dialog
    def showSTLFileDialog(self):
        filename = Qt.QFileDialog.getOpenFileName(self, 'Open file', '', 'STL (*.stl)')
        if filename[0] != "":
            f = open(filename[0], 'r')
            with f:
                self.loadSTL(str(filename[0]))


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
