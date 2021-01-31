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
        'writer'        TEXT, \
	    PRIMARY KEY('id' AUTOINCREMENT) \
    );")

    con.commit()


def query_database(query):
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()
    cursor.execute(query)
    con.commit()
    return cursor.fetchall()


def insert_comic(title, type, series, number, issueID, dateCreated, writer):
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    cursor.execute(
        "INSERT INTO comics(title, type, series, number, issueID, dateCreated, writer) \
        Values (?, ?, ?, ?, ?, ?, ?)", (title, type, series, number, issueID, dateCreated, writer))
    con.commit()


def clear_database():
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    cursor.executescript(
        "DELETE FROM comics;\
        UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='comics';"
    )
    con.commit()


def get_all_comic_info():
    comicList = query_database(
        'SELECT * FROM comics'
    )
    return comicList


def main():
    create_database()
    clear_database()
    insert_comic('title', 'type', 'series', 'number', 'issueID', 'dateCreated', 'writer')
    insert_comic('title2', 'type2', 'series2', 'number2', 'issueID2', 'dateCreated2', 'writer2')
    insert_comic('title3', 'type3', 'series3', 'number3', 'issueID3', 'dateCreated3', 'writer3')


if __name__ == "__main__":
    main()
