import psycopg2
from psycopg2 import Binary
from io import BytesIO
from PIL import Image


def insert_song(song_name, singer, album, file_song_path, file_image_path):
    conn = psycopg2.connect(database="player", user="postgres", password="monday2000", host="localhost", port="5432")
    cur = conn.cursor()

    with open(file_song_path, 'rb') as f_song, open(file_image_path, 'rb') as f_image:
        file_song_data = f_song.read()
        file_image_data = f_image.read()

    cur.execute("INSERT INTO songs (song_name, singer, album, file_song, file_image) VALUES (%s, %s, %s, %s, %s)",
                (song_name, singer, album, Binary(file_song_data), Binary(file_image_data)))
    conn.commit()

    cur.close()
    conn.close()


def get_track_data_from_database(song_name):
    conn = psycopg2.connect(database="player", user="postgres", password="monday2000", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("SELECT file_song FROM songs WHERE song_name = %s", (song_name,))
    song_data = cur.fetchone()[0]

    cur.close()
    conn.close()
    return song_data



