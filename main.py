import os
import sys
from dotenv import dotenv_values


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Directory(metaclass=Singleton):
    def __init__(self):
        config = dotenv_values(".env")
        if not config:
            print("Не найден файл конфигурации")
            sys.exit(1)
        self._root = config["ROOT"]
        self._path = []

    @property
    def path(self):
        return self._path

    @property
    def root(self):
        return self._root

    def make_path(self, root=False):
        s = '~'
        if root:
            s = self.root
        return s + '\\' + '\\'.join(self.path)


def os_listdir(cmd, directory):
    print(os.listdir(directory.make_path(True)))
    return

# def os_cd(cmd, directory):



def main():
    directory = Directory()
    commands = {
        "ls": os_listdir,
        # "cd": os_cd,
    }
    os.chdir(directory.root)
    while True:
        print(directory.make_path(), end=' ')
        cmd = input().split(' ')
        try:
            commands[cmd[0]](cmd[1:], directory)
        except KeyError:
            print('Неизвестная команда "' + cmd[0] + '"')



main()