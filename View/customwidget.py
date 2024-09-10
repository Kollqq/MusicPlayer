import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from View.SongWidget import Ui_CustomWidget
from tempfile import NamedTemporaryFile
import psycopg2
from View import db


class CustomWidget(QWidget):
    delete = pyqtSignal()  # Добавляем сигнал удаления

    def __init__(self, idw: int):
        super(CustomWidget, self).__init__()
        self.ui = Ui_CustomWidget()
        self.ui.setupUi(self)

        self.my_ID = idw
        self.ui.pushButton_2.clicked.connect(self.delete)  # Подключаем кнопку к сигналу

    def set_song_info(self, song_name, singer, album, file_song_path, file_image_path):
        self.ui.label_3.setText(song_name)
        self.ui.label_4.setText(singer)
        self.ui.label_5.setText(album)
        self.ui.label.setPixmap(QPixmap(file_image_path))
