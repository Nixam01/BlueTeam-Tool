import os.path
from os import path

ext = ['.pcap', 'txt', '.evtx', '.xml', '.json']


def check_path(filepath):
    if path.exists(filepath):
        if path.isfile(filepath):
            print(filepath)
        elif path.isdir(filepath):
            for paths, currentDirectory, files in os.walk(filepath):
                for file in files:
                    if file.endswith(tuple(ext)):
                        print(os.path.join(paths, file))
    else:
        print('This is not a valid path!')


