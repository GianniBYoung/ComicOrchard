import sqlite3
import os
import zipfile 
import shutil
from xml.dom import minidom
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



#returns a dictionary with metadata
def extractMetadata(path, filename):
    metadataDict ={}
    with zipfile.ZipFile(path) as zip_file:
        with zip_file.open(filename) as f:
            xmldoc = minidom.parse(f)

            metadataDict["year"] = xmldoc.getElementsByTagName('Year')[0].firstChild.data
            metadataDict["month"] = xmldoc.getElementsByTagName('Month')[0].firstChild.data
            metadataDict["day"] = xmldoc.getElementsByTagName('Day')[0].firstChild.data
            metadataDict["writer"] = xmldoc.getElementsByTagName('Writer')[0].firstChild.data
            metadataDict["penciller"] = xmldoc.getElementsByTagName('Penciller')[0].firstChild.data
            metadataDict["inker"] = xmldoc.getElementsByTagName('Inker')[0].firstChild.data
            metadataDict["letterer"] = xmldoc.getElementsByTagName('Letterer')[0].firstChild.data
            # split on commas
            metadataDict["cover artist"] = xmldoc.getElementsByTagName('CoverArtist')[0].firstChild.data
            # split on commas
            metadataDict["editor"] = xmldoc.getElementsByTagName('Editor')[0].firstChild.data
            metadataDict["publisher"] = xmldoc.getElementsByTagName('Publisher')[0].firstChild.data
            metadataDict["metadata source"] = xmldoc.getElementsByTagName('Web')[0].firstChild.data
            metadataDict["page count"] = xmldoc.getElementsByTagName('PageCount')[0].firstChild.data
            # split on commas
            metadataDict["characters"] = xmldoc.getElementsByTagName('Characters')[0].firstChild.data
            # split on commas
            metadataDict["locations"] = xmldoc.getElementsByTagName('Locations')[0].firstChild.data
            
            return metadataDict

tempPath = "/home/gianni/Documents/code/python/comicbooks/Batman Damned (1-3)/Batman_ Damned #1 - Brian Azzarello.cbz"
test  = extractMetadata(tempPath, "ComicInfo.xml")
print(test)


def create_database():
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    # creates Comics table
    cursor.execute("CREATE TABLE IF NOT EXISTS 'comics' ( \
	    'id'	        INTEGER NOT NULL, \
	    'title'	        TEXT, \
	    'type'	        TEXT, \
	    'series'	    TEXT, \
	    'number'	    INTEGER, \
	    'issueID'	    INTEGER, \
	    'dateCreated'	TEXT, \
	    PRIMARY KEY('id' AUTOINCREMENT) \
    );")

    # creates Creators table
    cursor.execute("CREATE TABLE  IF NOT EXISTS 'creators' ( \
	    'id'	        INTEGER NOT NULL, \
	    'name'	        TEXT, \
	    'position'	    TEXT, \
	    PRIMARY KEY('id' AUTOINCREMENT) \
    );")

    # creates CreatorComics table
    cursor.execute("CREATE TABLE 'creatorComics' ( \
	    'id'	        INTEGER NOT NULL, \
	    'comicID'	    INTEGER, \
	    'creatorID'	    INTEGER, \
	    FOREIGN KEY('comicID') REFERENCES 'comics'('id'), \
	    PRIMARY KEY('id' AUTOINCREMENT), \
	    FOREIGN KEY('creatorID') REFERENCES 'creators'('id') \
    );")

    con.commit()


def main():
    create_database()


if __name__ == "__main__":
    main()
