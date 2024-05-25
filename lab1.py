import argparse
import os
import shutil
import winreg

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--create_file', help='создать файл', action='store_true')
parser.add_argument('-d', '--delete_file', help='удалить файл', action='store_true')
parser.add_argument('-w', '--write_file', help='записать в файл', action='store_true')
parser.add_argument('-r', '--read_file', help='прочитать из файла', action='store_true')
parser.add_argument('-p', '--copy_file', help='скопировать файл из одной директории в другую', action='store_true')
parser.add_argument('-n', '--rename_file', help='переименовать файл', action='store_true')
parser.add_argument('-C', '--create_key', choices=['HKEY_CURRENT_USER',
                                                   'HKEY_LOCAL_MACHINE',
                                                   'HKEY_USERS',
                                                   'HKEY_CLASSES_ROOT',
                                                   'HKEY_CURRENT_CONFIG'], help='создать ключ')
parser.add_argument('-D', '--delete_key', choices=['HKEY_CURRENT_USER',
                                                   'HKEY_LOCAL_MACHINE',
                                                   'HKEY_USERS',
                                                   'HKEY_CLASSES_ROOT',
                                                   'HKEY_CURRENT_CONFIG'], help='удалить ключ')
parser.add_argument('-W', '--write_key',  choices=['HKEY_CURRENT_USER',
                                                   'HKEY_LOCAL_MACHINE',
                                                   'HKEY_USERS',
                                                   'HKEY_CLASSES_ROOT',
                                                   'HKEY_CURRENT_CONFIG'],help='записать значение в ключ')
                                                                                  # ^^^ optional arguments
parser.add_argument('fr_name', help='имя файла или путь реестра', type=str)       # <<< positional argument

args = parser.parse_args()


def func_create_file(name):
    f = open(name, 'x')
    f.close()
    return 0


def func_delete_file(name):
    os.remove(name)
    return 0


def func_write_file(name):
    f = open(name, 'w')
    print("Напишите ваш текст:")
    user_str = input()
    f.write(user_str)
    return 0


def func_read_file(name):
    f = open(name, 'r')
    file_str = f.read()
    print(file_str)
    f.close()
    return 0


def func_copy_file(name):
    print("Напишите место для копирования файла:")
    user_str = input()
    shutil.copy(name, user_str)
    return 0


def func_rename_file(name):
    print("Напишите новое имя файла:")
    user_str = input()
    os.rename(name, user_str)
    return 0


def func_create_key(name):
    if args.create_key == 'HKEY_CURRENT_USER':
        path = winreg.HKEY_CURRENT_USER
    elif args.create_key == 'HKEY_LOCAL_MACHINE':
        path = winreg.HKEY_LOCAL_MACHINE
    elif args.create_key == 'HKEY_USERS':
        path = winreg.HKEY_USERS
    elif args.create_key == 'HKEY_CLASSES_ROOT':
        path = winreg.HKEY_CLASSES_ROOT
    elif args.create_key == 'HKEY_CURRENT_CONFIG':
        path = winreg.HKEY_CURRENT_CONFIG
    software = winreg.OpenKeyEx(path, name)
    if software:
        print("Назовите новую папку:")
        user_str = input()
        new_key = winreg.CreateKey(software, user_str)
        print("Назовите новый ключ:")
        user_name = input()
        print("Укажите новое значение:")
        user_value = input()
        winreg.SetValueEx(new_key, user_name, 0, winreg.REG_SZ, user_value)
        if new_key:
            winreg.CloseKey(new_key)
    return 0


def func_delete_key(name):
    if args.delete_key == 'HKEY_CURRENT_USER':
        path = winreg.HKEY_CURRENT_USER
    elif args.delete_key == 'HKEY_LOCAL_MACHINE':
        path = winreg.HKEY_LOCAL_MACHINE
    elif args.delete_key == 'HKEY_USERS':
        path = winreg.HKEY_USERS
    elif args.delete_key == 'HKEY_CLASSES_ROOT':
        path = winreg.HKEY_CLASSES_ROOT
    elif args.delete_key == 'HKEY_CURRENT_CONFIG':
        path = winreg.HKEY_CURRENT_CONFIG
    software = winreg.OpenKeyEx(path, name)
    if software:
        winreg.DeleteKey(path, name)
    return 0


def func_write_key(name):
    if args.write_key == 'HKEY_CURRENT_USER':
        path = winreg.HKEY_CURRENT_USER
    elif args.write_key == 'HKEY_LOCAL_MACHINE':
        path = winreg.HKEY_LOCAL_MACHINE
    elif args.write_key == 'HKEY_USERS':
        path = winreg.HKEY_USERS
    elif args.write_key == 'HKEY_CLASSES_ROOT':
        path = winreg.HKEY_CLASSES_ROOT
    elif args.write_key == 'HKEY_CURRENT_CONFIG':
        path = winreg.HKEY_CURRENT_CONFIG
    software = winreg.OpenKeyEx(path, name)
    if software:
        print("Укажите новое значение:")
        user_value = input()
        winreg.SetValue(path, name, winreg.REG_SZ, user_value)
        winreg.CloseKey(software)

    return 0


print(args)
if args.create_file:
    func_create_file(args.fr_name)
elif args.delete_file:
    func_delete_file(args.fr_name)
elif args.write_file:
    func_write_file(args.fr_name)
elif args.read_file:
    func_read_file(args.fr_name)
elif args.copy_file:
    func_copy_file(args.fr_name)
elif args.rename_file:
    func_rename_file(args.fr_name)
elif args.create_key:
    func_create_key(args.fr_name)
elif args.delete_key:
    func_delete_key(args.fr_name)
elif args.write_key:
    func_write_key(args.fr_name)
