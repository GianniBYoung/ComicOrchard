import sqlite3
import os
import shutil
from pathlib import Path

def obtainListOfPaths(path):
    listOfFiles = list()
    for (dirpath, dirname, filenames) in os.walk(path, topdown=True):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    return listOfFiles



#todo optimize this and make sure it checks if the directory needs to be created first
def copyLibrary(source, destination):
    print("copying from "+source+" to "+destination)
    shutil.copytree(source, destination)
    print("copying complete")



tempPath = "/home/gianni/Documents/code/python/comicbooks"
copyLibrary(tempPath, "/home/gianni/.comicOrchard/main")

