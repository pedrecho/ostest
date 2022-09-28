import os
from dotenv import dotenv_values


def main():
    config = dotenv_values(".env")
    if not config:
        print("Не найден файл конфигурации")
        return



main()