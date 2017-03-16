import subprocess


class FileType(object):


    def __init__(self, path):
        self.file_type = self.__file_type(path)
        print self.file_type

    def __file_type(self, path):
        return subprocess.check_output(['file', path]).lower()

    def find(self):
        if 'image' in self.file_type:
            return 'image'
        elif 'pdf' in self.file_type:
            return 'pdf'
        elif 'zip' in self.file_type:
            return 'zip'
