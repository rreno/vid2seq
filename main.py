import sys
import subprocess
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2.QtCore import QFile, QDir
from PySide2.QtUiTools import QUiLoader


DEFAULT_IN_TEXT = 'VIDEO'
DEFAULT_OUT_TEXT = 'OUTPUT'


class MainWindow(QMainWindow):
    '''
    MainWindow class
    Inherits from PySide2.QtWidgets.QMainWindow
    
    Loads ui file, connects signals and slots to appropriate children widgets
    and handles the logic.

    TODO: Seperate concerns. Manage UI elements and logic in seperate clsases
    '''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = QFile('ui/mainwindow.ui')
        self.ui.open(QFile.ReadOnly)

        self.loader = QUiLoader()
        self.window = self.loader.load(self.ui)
        self.centralWidget = self.window.centralWidget()
        self.menuExit = self.window.menuBar().children()[0]
        
        '''
        Get all of the children of the centralWidget and assign them by name
        '''
        self.children = {}
        for child in self.centralWidget.children()[0].children():
            self.children.update({child.objectName(): child})

        self.btnIn = self.children['btnIn']
        self.lblIn = self.children['lblIn']
        self.btnOut = self.children['btnOut']
        self.lblOut = self.children['lblOut']
        self.btnGo = self.children['btnGo']

        '''
        Set up file path and video name defaults and disable execution of
        ffmpeg until after video and output location have been selected
        '''
        self.inPath = './'
        self.outPath = './'
        self.vidName = ''

        self.lblIn.setText(DEFAULT_IN_TEXT)
        self.lblOut.setText(DEFAULT_OUT_TEXT)
        self.btnGo.setEnabled(False)

        self.btnIn.clicked.connect(self.selectInputVideo)
        self.btnOut.clicked.connect(self.selectOutputDir)
        self.btnGo.clicked.connect(self.convertVideo)

    def show(self):
        self.window.show()

    def selectInputVideo(self):
        '''
        Opens a dialog to allow the user to select a video. Saves the full path to later pass to ffmpeg
        '''
        video = QFileDialog.getOpenFileName(parent=self.centralWidget,
                                            caption='Input Video',
                                            dir=self.inPath)
        # video is a tuple of (filename, selectedFilter). We just need the first element
        self.inPath = QDir(video[0]).absolutePath()
        self.lblIn.setText(self.inPath)
        # remove the path information so we can name our sequence files later.
        self.vidName = self.inPath.split('/')[-1]

        if self.lblIn.text() != DEFAULT_IN_TEXT and self.lblOut.text() != DEFAULT_OUT_TEXT:
            self.btnGo.setEnabled(True)

    def selectOutputDir(self):
        '''
        Opens a dialog so the user can select an output folder for the sequence.
        '''
        out = QFileDialog.getExistingDirectory(parent=self.centralWidget,
                                               caption='Output Directory',
                                               dir=self.outPath)
        self.outPath = QDir(out).absolutePath()
        self.lblOut.setText("{}_XXX.png".format(self.vidName))

        if self.lblIn.text() != DEFAULT_IN_TEXT and self.lblOut.text() != DEFAULT_OUT_TEXT:
            self.btnGo.setEnabled(True)

    def convertVideo(self):
        '''
        Calls ffmpeg with the input and output paths.
        '''
        print("Converting")
        try:
            subprocess.run("ffmpeg -i {} {}/{}_%03d.png".format(self.inPath,
                                                                self.outPath,
                                                                self.vidName),
                           check=True, shell=True)
        except subprocess.CalledProcessError as error:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
