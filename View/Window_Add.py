import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PyQt5 import QtWidgets

from MainWindow import Ui_MainWindow
from AddWindow import Ui_Form


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_3.clicked.connect(self.choose_track_file)

    def choose_track_file(self):
        track = QFileDialog.getOpenFileName(self, "Open File", "", "All Files")

    def choose_picture_file(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())