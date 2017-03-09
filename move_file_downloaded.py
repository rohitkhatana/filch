import zipfile
import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler


def downloaded_file(file_src):
    return file_src.split('/')[-1]


class DownloadedFileHandler(FileSystemEventHandler):

    def on_modified(self, event):
        print 'Got it modified'
        print event

    def on_created(self, event):
        print 'Got it created'
        file_name = downloaded_file(event.src_path)
        if file_name:
            MoveOrExtractFile(file_name).move_file_in_respected_directory()


class MoveOrExtractFile():

    def __init__(self, file_name):
        self._path = "/Users/rohitkhatana/Downloads/"
        self.file_name = file_name
        self.file_ext = file_name.split(".")[-1]

    def create_new_directory(self, directory):
        if not os.path.exists(directory):
            print 'not exists'
            os.makedirs(directory)

    def create_and_move_file(self, directory):
        self.create_new_directory(directory)
        os.rename(self._path+self.file_name, directory+"/"+self.file_name)

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
        if self.file_ext in ["ico", "svg", "png", "jpeg", "jpg"]:
            self.create_and_move_file(self._path + "Pictures")
            print 'done'
        elif self.file_ext in ["zip", "tar", "gz"]:
            self.create_and_move_file(self._path + "Archives")
            if self.file_ext == "zip":
                self.extract_zip_file(
                    self._path+"Subtitles/",  self._path + "Archives/" + self.file_name)
            print 'done'

        elif self.file_ext in ["mp4", "avi", "flv", "webm", "vob", "mkv", "m4v"]:
            self.create_and_move_file(self._path + "Videos")
        elif self.file_ext in ["pdf"]:
            self.create_and_move_file(self._path + "PDFs")
        elif self.file_ext in ["xls", "xlsx"]:
            self.create_and_move_file(self._path + "Excel-Sheets")
        elif self.file_ext in ["mp3"]:
            self.create_and_move_file(self._path + "Songs")
        else:
            print 'file ext not match' + self.file_ext

if __name__ == "__main__":
    from os.path import expanduser
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = expanduser('~') + '/Downloads/'
    print path
    #path = sys.argv[1] if len(sys.argv) > 1 else '.'
    #event_handler = LoggingEventHandler()
    event_handler = DownloadedFileHandler()
    observer = Observer()
    print observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print 'started'
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    print '--joins--'
    print observer.join()
