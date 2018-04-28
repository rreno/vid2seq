import sys
import subprocess
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2.QtCore import QFile, QDir
from PySide2.QtUiTools import QUiLoader


DEFAULT_IN_TEXT = 'VIDEO'
DEFAULT_OUT_TEXT = 'OUTPUT'


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = QFile(QFile.symLinkTarget('ui/mainwindow.ui'))
        self.ui.open(QFile.ReadOnly)

        self.loader = QUiLoader()
        self.window = self.loader.load(self.ui)
        self.centralWidget = self.window.centralWidget()
        self.menuExit = self.window.menuBar().children()[0]

        self.children = {}
        for child in self.centralWidget.children()[0].children():
            self.children.update({child.objectName(): child})

        self.btnIn = self.children['btnIn']
        self.lblIn = self.children['lblIn']
        self.btnOut = self.children['btnOut']
        self.lblOut = self.children['lblOut']
        self.btnGo = self.children['btnGo']

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
        video = QFileDialog.getOpenFileName(parent=self.centralWidget,
                                            caption='Input Video',
                                            dir=self.inPath)
        self.inPath = QDir(video[0]).absolutePath()
        self.lblIn.setText(self.inPath)
        self.videoName = self.inPath.split('/')[-1].split('.')[0]

        if self.lblIn.text() != DEFAULT_IN_TEXT and self.lblOut.text() != DEFAULT_OUT_TEXT:
            self.btnGo.setEnabled(True)

    def selectOutputDir(self):
        out = QFileDialog.getExistingDirectory(parent=self.centralWidget,
                                               caption='Output Directory',
                                               dir=self.outPath)
        self.outPath = QDir(out).absolutePath()
        self.lblOut.setText("{}_XXX.png".format(self.videoName))

        if self.lblIn.text() != DEFAULT_IN_TEXT and self.lblOut.text() != DEFAULT_OUT_TEXT:
            self.btnGo.setEnabled(True)

    def convertVideo(self):
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
