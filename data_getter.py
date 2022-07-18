import os
from bs4 import BeautifulSoup
from utilites import get_platform


class DataGetter:
    def __init__(self, folder):
        self.folder = folder
        self.platform = get_platform(folder)
        self.files = sorted(os.listdir(folder))
        self.soup = None

    def run(self):
        for filename in self.files:
            with open(f'{self.folder}/{filename}', 'r', encoding='utf8') as read_file:
                if read_file == '.DS_Store':
                    continue
                src = read_file.read()
            self.soup = BeautifulSoup(src, 'lxml')
            self.get_data()

    def get_data(self):
        pass
