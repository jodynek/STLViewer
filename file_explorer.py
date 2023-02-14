#!/usr/bin/env python

from PyQt5 import Qt, QtWidgets


# MainWindow class
class MainWindow(Qt.QMainWindow):
    def __init__(self):
        Qt.QMainWindow.__init__(self)

        widget = Qt.QWidget()
        self.setCentralWidget(widget)

        self.setWindowTitle("File Explorer")
        self.setMinimumSize(160, 160)
        self.resize(700, 600)

        # create File System tree
        self.treeView = QtWidgets.QTreeView()
        self.fileSystemModel = QtWidgets.QFileSystemModel(self.treeView)
        self.fileSystemModel.setReadOnly(False)
        root = self.fileSystemModel.setRootPath("/")
        self.treeView.setModel(self.fileSystemModel)
        self.treeView.setRootIndex(root)
        # Create Layout
        Layout = Qt.QVBoxLayout()
        Layout.addWidget(self.treeView)
        widget.setLayout(Layout)

        self.createActions()
        self.createMenus()
        self.createStatusBar()

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def about(self):
        Qt.QMessageBox.about(self, "About File Explorer",
                             "Version 1.0\n"
                             "Copyright 2014 Korben Carreno\n"
                             "Example of a File Explorer")

    # Actions for menu buttons
    def createActions(self):
        self.newAct = Qt.QAction("&New", self, shortcut=Qt.QKeySequence.New, statusTip="Create a new file")
        self.exitAct = Qt.QAction("E&xit", self, shortcut="Ctrl+Q", statusTip="Exit the application",
                                  triggered=self.close)
        self.aboutAct = Qt.QAction("&About", self, statusTip="About File Explorer", triggered=self.about)
        self.aboutQtAct = Qt.QAction("About &Qt", self, statusTip="About Qt library", triggered=Qt.qApp.aboutQt)

    # Menus
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)


# main
if __name__ == '__main__':
    import sys

    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
