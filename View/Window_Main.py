import os.path
import sys
from tempfile import NamedTemporaryFile

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from PyQt5 import QtWidgets
from PySide6.QtCore import Slot

from MainWindow import Ui_MainWindow
from AddWindow import Ui_Form
from SongWidget import Ui_CustomWidget

from View import db
from View.customwidget import CustomWidget


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui_widget = Ui_CustomWidget()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self)

        self.file_song_path = None
        self.file_image_path = "400x400.jfif"
        self.current_css_pushButton_2 = None
        self.id_counter = 0
        self.my_widgets_dict: dict[int, QListWidgetItem] = {}

        self.ui_main.actionAdd.triggered.connect(self.open_AddWindow)
        # self.ui_widget.pushButton_2.clicked.connect(self.delete_widget)

    def open_AddWindow(self):
        self.add_window = QtWidgets.QWidget()
        self.ui_add = Ui_Form()
        self.ui_add.setupUi(self.add_window)
        self.ui_add.pushButton_3.clicked.connect(self.choose_song_file)
        self.ui_add.pushButton.clicked.connect(self.choose_image_file)
        self.ui_add.pushButton_2.clicked.connect(self.add_new_song)

        self.add_window.show()

    def choose_song_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.add_window, "Open File", "", "All Files (*);;MP3 files (*.mp3)")
        if file_path:
            self.file_song_path = file_path
            print("Selected file:", file_path)
            self.ui_add.label_5.setText(os.path.basename(file_path))
            self.ui_add.label_5.setStyleSheet("color: white;")
            self.ui_add.pushButton_2.setStyleSheet(self.current_css_pushButton_2)

    def choose_image_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.add_window, "Open File", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.file_image_path = file_path
            print("Selected file:", file_path)
            self.ui_add.label.setPixmap(QPixmap(file_path))

    def add_new_song(self):
        song_name = self.ui_add.lineEdit.text()
        singer = self.ui_add.lineEdit_2.text()
        album = self.ui_add.lineEdit_3.text()
        self.current_css_pushButton_2 = self.ui_add.pushButton_2.styleSheet()

        if self.file_song_path and self.file_image_path:
            file_image_path = self.file_image_path
            file_song_path = self.file_song_path

            db.insert_song(song_name, singer, album, file_song_path, file_image_path)

            song_widget = CustomWidget(self.id_counter)
            song_widget.set_song_info(song_name, singer, album, file_song_path, file_image_path)

            list_item = QListWidgetItem(self.ui_main.listWidget)
            list_item.setSizeHint(song_widget.sizeHint())

            self.my_widgets_dict[song_widget.my_ID] = list_item
            self.ui_main.listWidget.addItem(list_item)
            self.ui_main.listWidget.setItemWidget(list_item, song_widget)
            # song_widget.delete.connect(lambda: self.delete_widget(song_widget))
            song_widget.delete.connect(self.delete_widget)
            self.add_window.close()
            self.file_song_path = None
            self.id_counter += 1

        else:
            new_css_pushButton_2 = self.current_css_pushButton_2 + "border: 2px solid red;"
            self.ui_add.pushButton_2.setStyleSheet(new_css_pushButton_2)
            self.ui_add.label_5.setText("Надо обязательно загрузить трек")
            self.ui_add.label_5.setStyleSheet("color: red;")

    # def delete_widget(self, widget):
    #     my_item = self.my_widgets_dict[widget.my_ID]
    #     self.ui_main.listWidget.takeItem(self.ui_main.listWidget.row(my_item))
    #     del self.my_widgets_dict[widget.my_ID]

    @pyqtSlot()
    def delete_widget(self):
        widget = self.sender()
        item = self.my_widgets_dict[widget.my_ID]  # Получаем QListWidgetItem по ID виджета
        row = self.ui_main.listWidget.row(item)  # Получаем номер строки элемента в QListWidget
        self.ui_main.listWidget.takeItem(row)  # Удаляем элемент из QListWidget
        del self.my_widgets_dict[widget.my_ID]  # Удаляем элемент из словаря


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec())
