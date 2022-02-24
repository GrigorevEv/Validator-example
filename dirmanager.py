from pathlib import Path
from abc import ABC, abstractmethod
from os.path import getmtime
import os
import re

from validators import regex_validator


def catch_file_not_found_err(fn):
    def wrapper(*args):
        try:
            fn(*args)
        except FileNotFoundError:
            print('Данной директории не существует')
    return wrapper

        
class Storage(ABC):
    """ Абстрактный класс для создания файлов и директорий.
    """
    def __init__(self, path: str, name: str):
        self.path = path
        self.name = name
        self.full_path = Path(f'{self.path}/{self.name}')
        if not Path(self.path).exists():
            raise Exception('Данной директории не существует!')

    @abstractmethod
    def create(self): ...

    @abstractmethod
    def remove(self): ...

    def __str__(self):
        return str(self.full_path)


@regex_validator
class Directory(Storage):
    """ Класс для создания директорий.
    """
    regexes = {
        'path': r'^[\w/]+$',
        'name': r'^\w+$',
    }

    def create(self):
        if not self.full_path.exists():
            self.full_path.mkdir()
            self.created = getmtime(str(self.full_path))

    def remove(self):
        self.full_path.rmdir()

    def sort(self):
        arr = os.listdir(str(self.full_path))
        print(arr)


@regex_validator
class File(Storage): 
    """ Класс для создания файлов.
    """
    regexes = Directory.regexes

    def __init__(self, text: str = '', *args, **kwargs):
        self.text = text
        Storage.__init__(self, *args, **kwargs)

    @catch_file_not_found_err
    def create(self):
        with self.full_path.open('w', encoding='utf-8') as f:
            f.write(self.text)
        self.created = getmtime(str(self.full_path))

    @catch_file_not_found_err
    def remove(self):
        self.full_path.unlink()


dir1 = Directory('/Users/eugene/code/grade', 'dir1')
dir1.create()
print(dir1.__dict__)

file1 = File(text='hello', path='/Users/eugene/code/grade/', name='file1')
file1.create()
print(file1.__dict__)

