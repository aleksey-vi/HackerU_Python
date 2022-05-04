# напишите программу backuper.py, делающую бэкап указанной директории или файла в архив.
# предусмотрите проверку существования целевой директори и файла, и информирование пользователя о результатах
#
# *предусмотрите возможность предупреждения пльзователя о уже существующем архиве с таким же именем и предложите ему варианты "перезаписать", "переименовать" и т.п. на ваше усмотрение

import os
import sys
import subprocess
from zipfile import ZipFile
from datetime import datetime


# Разобраться как делать бекапы директорий в винде так и не удалось, хотя файлы копирует без проблем.

def create_unix_archive(zip_path, files):
    """функция для создания архива на unix с аргументами: путь где создается архив, и пути с названиями к файлам, которые будут добавлены в архив"""
    # в качестве имени указывается дата и время создания
    zip_name = "{0}.zip".format(datetime.now().strftime("%Y-%m-%d-%H-%I-%S"))
    print(zip_path, zip_name, files)  # выводим путь, имя, и файлы которые были добавлены в архив
    path_file = os.path.join(zip_path, zip_name)
    # создается объект(архив), в котором первым аргументом является путь/имя, а вторым мод на запись
    with ZipFile(path_file, 'w') as zipfile:
        for file_name in files: # перебор элементов file_name из списка files
            zipfile.write(file_name) # записываем в наш архив переданные файлы


def create_win_archive(zip_path, files, path_7z_proc):
    """функция для создания архива на win с аргументами: путь где создается архив, и пути с названиями к файлам, которые будут добавлены в архив"""
    # в качестве имени указывается дата и время создания
    zip_name = "{0}.zip".format(datetime.now().strftime("%Y-%m-%d-%H-%I-%S"))
    print(zip_path, zip_name, files)
    # превращаем путь к файлу в строку, соединяем по пробелу
    path_file = ' '.join(files)
    os.chdir(path_7z_proc)  # переход в директорию 7zip, которую ввел пользователь
    # вызываем дочерний процесс на создание архива с указанием аргументов
    zip_proc = subprocess.Popen(["7z", "a", zip_name, path_file], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = zip_proc.communicate()
    print(out.decode("cp866"))


# переменная типа стринг, в которую пользователь вводит заданные значения, в нижнем регистре
backup_target = str(input("Введите d или f (что будем бэкапить? d - директорию или f - файл): ")).lower()

if backup_target not in ['d', 'f']: # условие: если пользак выбрал что то отличное от d и f
    raise Exception("нет таких аргументов пёс") # прерывание с сообщением

files_to_backup = []  # пустой список для файлов которые нужно забекапить

if backup_target == 'd':  ## если пользователь выбрал бекапить директорию
    storage = input("введи папку для бэкапа пёс: ")  # выводим сообщение
    # если в модуле os в подмодуле path метод isdir вернул false
    if not os.path.isdir(storage):
        raise Exception("Ты че пёс, нет такой дериктории")  # то получаем ошибку
    # создали список отформатированных имен файлов в указанной пользователем директории и поместили в переменную
    files_to_backup = [f"{storage}/{file}" for file in os.listdir(storage)]
elif backup_target == 'f':  # если пользователь выбрал бекапить файлы
    # бесконечный цикл
    while True:
        # вводим путь до файла, который нужно добавить в список для бекапа
        file_to_backup = input("введите путь к файлу (если закончили напишет no или нажмите Enter): ")

        if file_to_backup == "no" or file_to_backup == "":  # условие выхода из цикла
            break
        # если пользак ввел путь к несуществующему файлу то выводим сообщение
        if not os.path.isfile(file_to_backup):
            print('ты чо, нет такого файла пес')
        else:  # иначе добавляем к списку с файлами для бекапа путь введенный пользаком с названием файла
            files_to_backup.append(file_to_backup)
# условие проверки пустого списка
if len(files_to_backup) == 0:
    raise Exception("нечего бэкапить пёс")
# если платформа Linux
if sys.platform in ['linux']:
    backup_dir = input("куда бэкапить: ")
    create_unix_archive(backup_dir, files_to_backup)
# если винда
elif sys.platform == 'win32':
    path_7z_proc = input("Введи путь до 7zip")
    backup_dir = input("куда бэкапить: ")
    create_win_archive(backup_dir, files_to_backup, path_7z_proc)
