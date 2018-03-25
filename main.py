import sys
import os
import unicodedata
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QLineEdit

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'M3U Generator'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)
        self.textbox.setReadOnly(True)

        self.selectbutton = QPushButton("Select", self)
        self.selectbutton.clicked.connect(self.getDir)
        self.selectbutton.move(20, 80)

        self.gobutton = QPushButton("Go", self)
        self.gobutton.clicked.connect(self.genM3U)
        self.gobutton.move(120, 80)

        self.show()

    def getDir(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)

        if dlg.exec_():
            files = dlg.selectedFiles()
            if len(files) < 1:
                return
            self.textbox.setText(dlg.selectedFiles()[0])

    def genM3U(self):
        selectDir = self.textbox.text()
        if not os.path.isdir(selectDir):
            return

        def isMusic(path):
            supportExtension = ['.mp3', '.m3u', '.wma', '.flac', '.wav', '.mc', '.aac', '.m4a', '.ape', '.dsf', '.dff']
            filename, fileExtension = os.path.splitext(path)
            if fileExtension.lower() in supportExtension:
                return True
            return False

        def createPlayList(selectDir):
            m3uList = []
            for root, subdirs, files in os.walk(selectDir):
                for filename in files:
                    relDir = os.path.relpath(root, selectDir)
                    if relDir == ".":
                        path = filename
                    else:
                        path = os.path.join(relDir, filename)
                    if isMusic(path):
                        m3uList.append(path)
            return m3uList

        m3uPath = os.path.join(selectDir, os.path.basename(selectDir) + ".m3u8")

        if os.path.exists(m3uPath):
            os.remove(m3uPath)

        m3uList = createPlayList(selectDir)

        f = open(m3uPath, 'w', encoding='utf-8')
        for music in m3uList:
            f.write(unicodedata.normalize('NFC', music) + '\n')
        f.close()
        print("finish")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
