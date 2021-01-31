import sqlite3
import os
import datetime
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



#returns a dictionary with metadata where the filename is the metadata file
def extractMetadata(path, filename):
    metadataDict ={}
    year = 0
    day = 0
    month = 0
    try:
        with zipfile.ZipFile(path) as zip_file:
            with zip_file.open(filename) as f:
                xmldoc = minidom.parse(f)

                metadataDict["issueID"] = xmldoc.getElementsByTagName('Notes')[0].firstChild.data.split('[')[1].split(' ')[2].split(']')[0]
                metadataDict["series"] = xmldoc.getElementsByTagName('Series')[0].firstChild.data
                metadataDict["number"] = xmldoc.getElementsByTagName('Number')[0].firstChild.data
                metadataDict["title"] = xmldoc.getElementsByTagName('Title')[0].firstChild.data
                year = xmldoc.getElementsByTagName('Year')[0].firstChild.data
                month = xmldoc.getElementsByTagName('Month')[0].firstChild.data
                day = xmldoc.getElementsByTagName('Day')[0].firstChild.data
                metadataDict["writer"] = xmldoc.getElementsByTagName('Writer')[0].firstChild.data
                metadataDict["publisher"] = xmldoc.getElementsByTagName('Publisher')[0].firstChild.data
                metadataDict["metadata source"] = xmldoc.getElementsByTagName('Web')[0].firstChild.data
                metadataDict["page count"] = xmldoc.getElementsByTagName('PageCount')[0].firstChild.data
                metadataDict["characters"] = xmldoc.getElementsByTagName('Characters')[0].firstChild.data
                metadataDict["locations"] = xmldoc.getElementsByTagName('Locations')[0].firstChild.data
 
 
                releaseDate = datetime.datetime(int(year),int(month),int(day))
                metadataDict["date"] = releaseDate.strftime("%Y/%m/%d")
 
                return metadataDict
    except:
            print("unable to open zip file")
    return metadataDict


 # need to find a way to determine type
def populate_database(basePath):
    listOfFiles = obtainListOfPaths(basePath)
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    for path in listOfFiles:
        if path.endswith("cbz"):
           metadataDict = extractMetadata(path,"ComicInfo.xml")
           print(path)
           print(metadataDict)

           cursor.execute('''INSERT OR IGNORE INTO Comics(title, type, series, number, issueID,\
                             dateCreated, writer, path) VALUES (?,?,?,?,?,?,?,?)''',
                             (metadataDict.setdefault("title", "NULL"),
                             "issue",
                             metadataDict.setdefault("series","NULL"),
                             metadataDict.setdefault("number","NULL"),
                             metadataDict.setdefault("issueID","NULL"),
                             metadataDict.setdefault("date","NULL"),
                             metadataDict.setdefault("writer","NULL"),
                             path))
           con.commit()


def create_database():
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    # creates Comics table
    cursor.execute("CREATE TABLE IF NOT EXISTS 'comics' ( \
	    'id'	    INTEGER NOT NULL, \
	    'title'	    TEXT, \
	    'type'	    TEXT, \
	    'series'	    TEXT, \
	    'number'	    INTEGER, \
	    'issueID'	    INTEGER, \
	    'dateCreated'   TEXT, \
	    'writer'   TEXT, \
            'path'          TEXT, \
	    PRIMARY KEY('id' AUTOINCREMENT) \
    );")

    con.commit()


def main():
    create_database()


if __name__ == "__main__":
    main()
