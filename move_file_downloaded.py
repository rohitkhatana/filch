import zipfile
import os
from os.path import expanduser
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

from file_type import FileType

HOME_PATH = expanduser('~') + '/Downloads/'


def downloaded_file(file_src):
    return file_src.split('/')[-1]


class DownloadedFileHandler(FileSystemEventHandler):

    def is_downloading(self, src_path):
        file_name = downloaded_file(src_path)
        if file_name.startswith('.'):
            return True
        elif file_name.endswith('.crdownload'):
            return True
        else:
            return False

    def on_created(self, event):
        file_name = downloaded_file(event.src_path)
        if not self.is_downloading(event.src_path) and file_name:
            MoveOrExtractFile(file_name).move_file_in_respected_directory()
        else:
            print 'not moving as file is downloading------'

    def on_moved(self, event):
        file_name = downloaded_file(event.dest_path)
        MoveOrExtractFile(file_name).move_file_in_respected_directory()

    def on_any_event(self, event):
        pass


class MoveOrExtractFile():

    def __init__(self, file_name):
        self.file_name = file_name
        self.file_ext = file_name.split(".")[-1]
        self.file_path = HOME_PATH + self.file_name
        self.file_type = FileType(self.file_path).find()

    def create_new_directory(self, directory):
        if not os.path.exists(directory):
            print 'not exists'
            os.makedirs(directory)

    def create_and_move_file(self, directory):
        self.create_new_directory(directory)
        os.rename(self.file_path, directory + "/" + self.file_name)

    def extract_zip_file(self, output_directory, moved_file):
        open_zip_file = open(moved_file, 'rb')
        zip_file = zipfile.ZipFile(open_zip_file)
        self.create_new_directory(output_directory)
        for name in zip_file.namelist():
            if name.split(".")[-1] == "srt":
                self.file_name = name
                zip_file.extract(name, output_directory)
        open_zip_file.close()

    def move_file_in_respected_directory(self):
        if self.file_type == 'image':
            self.create_and_move_file(HOME_PATH + "Pictures")
        elif self.file_ext in ["zip", "tar", "gz"]:
            self.create_and_move_file(HOME_PATH + "Archives")
            if self.file_ext == "zip":
                self.extract_zip_file(
                    HOME_PATH + "Subtitles/",  HOME_PATH + "Archives/" + self.file_name)

        elif self.file_ext in ["mp4", "avi", "flv", "webm", "vob", "mkv", "m4v"]:
            self.create_and_move_file(HOME_PATH + "Videos")
        elif self.file_ext == 'pdf':
            self.create_and_move_file(HOME_PATH + "PDFs")
        elif self.file_ext in ["xls", "xlsx"]:
            self.create_and_move_file(HOME_PATH + "Excel-Sheets")
        elif self.file_ext in ["mp3"]:
            self.create_and_move_file(HOME_PATH + "Songs")
        else:
            print 'file ext not match' + self.file_ext

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    #path = sys.argv[1] if len(sys.argv) > 1 else '.'
    #event_handler = LoggingEventHandler()
    event_handler = DownloadedFileHandler()
    observer = Observer()
    observer.schedule(event_handler, HOME_PATH, recursive=False)
    observer.start()
    print 'started'
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
