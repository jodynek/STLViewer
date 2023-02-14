import sys

import vtk
from PyQt5 import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MainWindow(Qt.QMainWindow):
    reader = vtk.vtkSTLReader()

    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)

        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        filename = "skull.STL"
        self.loadSTL(filename)
        #self.showFileDialog()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.show()
        self.iren.Initialize()
        self.iren.Start()

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
    def showFileDialog(self):
        fname = Qt.QFileDialog.getOpenFileName(self, 'Open file', '', 'STL (*.stl)')
        f = open(fname[0], 'r')
        with f:
            self.loadSTL(str(fname[0]))


if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
