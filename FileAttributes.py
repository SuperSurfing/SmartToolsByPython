# FileAttributes.py
from datetime import datetime
from os import scandir
from win32api import GetFileVersionInfo, LOWORD, HIWORD

def get_version_number(filepath):
    try:
        info = GetFileVersionInfo (filepath, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls)
    except:
        return "Unnown version"


def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%d %b %Y')
    return formated_date

def get_files(root_dir, target):
    dir_entries = scandir(root_dir)
    for entry in dir_entries:
        if entry.is_file() and entry.name == target:
            info = entry.stat()
            version = ".".join([str (i) for i in get_version_number (entry.path)])
            print(f'{entry.path}\t Last Modified: {convert_date(info.st_mtime)}\tVersion: {version}')
        elif entry.is_dir() :
            get_files(entry.path, target)

if __name__ == "__main__":
    root_dir = input("root dir: ")
    target_file = input("target file: ")
    get_files(root_dir, target_file)