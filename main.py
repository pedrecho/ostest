import os
import sys
from dotenv import dotenv_values

# class WrongCommand(Exception):
#     def __init__(self, *args):
#         if args:
#             self.message = args
#         else:
#             self.message = None
#
#     def __str__(self):
#         print('Неверное использование команды')


# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


class Directory:
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

    @path.setter
    def path(self, path):
        # try:
        os.chdir(self.root + path)
        self._path = path.split('/')
        return

    def cd_up(self):
        if len(self._path) != 0:
            self._path.pop()
        else:
            print('Вы находитесь в корневой папке, невозможно подняться выше')
        return

    def format_path(self, path, root=False):
        # print(path)
        if root:
            base = self.root
        else:
            base = '~'
        if path[0] == '~':
            path = path.lstrip('~')
            return base + path
        elif 'C' <= path[0] <= 'F':
            path = path[len(self.root):]
            return base + path
        # print(path)
        return self.make_path(root) + path

    def cd_in(self, path):
        try:
            os.chdir(self.format_path(path, True))
            self._path = self.format_path(path, False).split('\\')[1:]
        except FileNotFoundError:
            print("Директория не найдена")
        return

    def make_path(self, root=False):
        s = '~'
        if root:
            s = self.root
        path = s + '\\' + '\\'.join(self.path)
        if len(self.path) > 0:
            path += '\\'
        return path

    def file_name(self, path):
        return path.split('\\')[-1]


class System:
    def __init__(self, dir):
        self._dir = dir
        self.commands = {
            "list": self.os_listdir,
            "go": self.os_cd,
            "make": self.os_mkdir,
            "remove": self.os_rmdir,
            "create": self.os_mkfile,
            "delete": self.os_rmfile,
            "write": self.os_write,
            "read": self.os_read,
            "copy": self.os_copy,
            "move": self.os_move,
            "rename": self.os_rename,
            "end": self.os_exit,
            "help": self.os_help,
        }

    @property
    def root_dir(self):
        return self._dir.make_path(True)

    @property
    def user_dir(self):
        return self._dir.make_path(False)

    def os_listdir(self, cmd):
        print(' '.join(os.listdir(self.root_dir)))
        return

    def os_mkdir(self, cmd):
        path = self._dir.format_path(cmd[0], True)
        try:
            os.mkdir(path)
        except OSError:
            print('Данная директория уже существует')
        return

    def os_cd(self, cmd):
        if cmd[0] == "..":
            self._dir.cd_up()
        else:
            self._dir.cd_in(cmd[0])
        return

    def os_rmdir(self, cmd):
        try:
            path = self._dir.format_path(cmd[0], True)
            os.rmdir(path)
        except FileNotFoundError:
            print("Директория не существует или не является пустой")
        return

    def os_help(self, cmd):
        for i in self.commands:
            print(i)
        print()
        return

    def os_mkfile(self, cmd):
        path = self._dir.format_path(cmd[0], True)
        try:
            file = open(path, 'w+')
            file.close()
        except IndexError:
            print("Неверное количество аргументов команды")
        except PermissionError:
            print("Некорректное имя для файла")
        except FileNotFoundError:
            print("Неверный путь")
        return

    def os_exit(self, cmd):
        exit()

    def os_rmfile(self, cmd):
        path = self._dir.format_path(cmd[0], True)
        try:
            os.remove(path)
        except FileNotFoundError:
            print("Файл не существует")
        except IndexError:
            print("Неверное количество аргументов команды")
        return

    def os_write(self, cmd):
        path = self._dir.format_path(cmd[0], True)
        try:
            file = open(path, 'a+')
            file.write(cmd[1])
        except IndexError:
            print("Неверное количество аргументов команды")
        finally:
            try:
                file.close()
            except UnboundLocalError:
                pass
        return

    def _read_file(self, path):
        path = self._dir.format_path(path, True)
        try:
            file = open(path, "r")
            text = file.read()
            file.close()
            return text
        except PermissionError:
            print("Можно читать только из файлов")
        except FileNotFoundError:
            print("Файл не найден")
        return ""

    def os_read(self, cmd):
        path = self._dir.format_path(cmd[0], True)
        text = self._read_file(path).split('\\n')
        for i in text:
            print(i)
        return

    def os_copy(self, cmd):
        try:
            path = self._dir.format_path(cmd[0], True)
            text = self._read_file(path)
            if len(cmd) <= 2:
                name = cmd[0]
            else:
                name = cmd[2]
            path2 = self._dir.format_path(cmd[1] + '\\' + name, True)
            self.os_write([path2, text])
        except FileNotFoundError:
            print("Файл не найден")
        except IndexError:
            print("Неверное количество аргументов команды")
        return

    def os_move(self, cmd):
        try:
            filename = self._dir.file_name(cmd[0])
            path = self._dir.format_path(cmd[0], True)
            path2 = self._dir.format_path(cmd[1], True)
            os.rename(path, path2 + '\\' + filename)
        except FileNotFoundError:
            print("Файл не найден")
        except IndexError:
            print("Неверное количество аргументов команды")

    def os_rename(self, cmd):
        try:
            path = self._dir.format_path(cmd[0], True)
            path2 = self._dir.format_path(cmd[1], True)
            os.rename(path, path2)
        except FileNotFoundError:
            print("Файл не найден")
        except IndexError:
            print("Неверное количество аргументов команды")


def main():
    directory = Directory()
    sys = System(directory)
    os.chdir(directory.root)
    while True:
        print(directory.make_path(), end=' ')
        cmd = input().split(' ')
        try:
            sys.commands[cmd[0]](cmd[1:])
        except KeyError:
            print('Неизвестная команда "' + cmd[0] + '"')



main()