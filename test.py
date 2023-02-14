#!/usr/bin/env python

import sys
import vtk

from PyQt5 import Qt

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Test(Qt.QMainWindow):
    def __init__(self):
        super(Test, self).__init__()

        self.initUI()

    def initUI(self):

        self.textEdit = Qt.QTextEdit()
        # self.setCentralWidget(self.textEdit)
        self.statusBar()

        # This will be a screenshot button and I need to find a .png for it soon..
        exitAction = Qt.QAction(Qt.QIcon('icons/exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        # exitAction.triggered.connect(Qt.qApp.quit)

        # self.statusBar()
        openFile = Qt.QAction(Qt.QIcon('icons/open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open STL File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openFile)

        # Graphically, toolbars are nice but we don't need them right now..
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        toolbar.addAction(openFile)

        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('STL Viewer')
        self.show()

    def showDialog(self):

        fname = Qt.QFileDialog.getOpenFileName(self, 'Open file', '', 'STL (*.stl)')

        f = open(fname[0], 'r')

        with f:
            data = f.read()
            # self.textEdit.setText(data)
            self.vtkView(str(fname[0]))

    def vtkView(self, filename):
        # filename = "STL_Viewer/motor_mount_v2.STL"

        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)

        polydata = reader.GetOutput()

        # Setup actor and mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(polydata)
        else:
            mapper.SetInputData(polydata)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Setup render window, renderer, and interactor
        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)
        renderer.AddActor(actor)
        renderWindow.Render()
        renderWindowInteractor.Start()


def test():
    app = Qt.QApplication(sys.argv)
    ex = Test()
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
