import sqlite3
import subprocess
import os
import datetime
import zipfile
import shutil
from xml.dom import minidom

libraryPath = "/home/gianni/.comicOrchard/main/"


def obtainListOfPaths(path):
    listOfFiles = list()
    if path.endswith("cbz"):
        listOfFiles.append(path)
    for (dirpath, dirname, filenames) in os.walk(path, topdown=True):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    return listOfFiles


def copyLibrary(source):
    print("copying from " + source + " to " + libraryPath)
    try:
        shutil.copytree(source, libraryPath)
        print("copying complete")
    except:
        print("file already exists")


def copyComic(source, destination):
    print("copying from " + source + " to " + libraryPath)
    try:
        shutil.copytree(source, destination)
        print("copying complete")
    except:
        print("file already exists")


def addComic(source):
    filename = source.split('/')[-1]
    destination = libraryPath + filename
    copyComic(source, destination)
    populate_database(destination)


def openComicForReading(path):
    subprocess.call(['mcomix', path])


# returns a dictionary with metadata where the filename is the metadata file
def extractMetadata(path, filename):
    metadataDict = {}
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zip_file:
            with zip_file.open(filename) as f:
                xmldoc = minidom.parse(f)

                metadataDict["issueID"] = \
                    xmldoc.getElementsByTagName('Notes')[0].firstChild.data.split('[')[1].split(' ')[2].split(']')[0]
                metadataDict["series"] = xmldoc.getElementsByTagName('Series')[0].firstChild.data
                metadataDict["number"] = xmldoc.getElementsByTagName('Number')[0].firstChild.data
                metadataDict["publisher"] = xmldoc.getElementsByTagName('Publisher')[0].firstChild.data
                metadataDict["metadata source"] = xmldoc.getElementsByTagName('Web')[0].firstChild.data
                metadataDict["page count"] = xmldoc.getElementsByTagName('PageCount')[0].firstChild.data

                if len(xmldoc.getElementsByTagName('Title')) != 0:
                    metadataDict["title"] = xmldoc.getElementsByTagName('Title')[0].firstChild.data

                if len(xmldoc.getElementsByTagName('Writer')) != 0:
                    metadataDict["writer"] = xmldoc.getElementsByTagName('Writer')[0].firstChild.data

                if len(xmldoc.getElementsByTagName('Characters')) != 0:
                    metadataDict["characters"] = xmldoc.getElementsByTagName('Characters')[0].firstChild.data

                if len(xmldoc.getElementsByTagName('Locations')) != 0:
                    metadataDict["locations"] = xmldoc.getElementsByTagName('Locations')[0].firstChild.data

                year = xmldoc.getElementsByTagName('Year')[0].firstChild.data
                month = xmldoc.getElementsByTagName('Month')[0].firstChild.data
                day = xmldoc.getElementsByTagName('Day')[0].firstChild.data

                releaseDate = datetime.datetime(int(year), int(month), int(day))
                metadataDict["date"] = releaseDate.strftime("%Y/%m/%d")

                return metadataDict
    else:
        print(path + " is not a zip file")


# need to find a way to determine type
def populate_database(basePath):
    listOfFiles = obtainListOfPaths(basePath)
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    for path in listOfFiles:
        if path.endswith("cbz"):
            metadataDict = extractMetadata(path, "ComicInfo.xml")

            cursor.execute('''INSERT OR IGNORE INTO Comics(title, type, series, number, issueID,\
                             dateCreated, writer, path) VALUES (?,?,?,?,?,?,?,?)''',
                           (metadataDict.setdefault("title", "NULL"),
                            "issue",
                            metadataDict.setdefault("series", "NULL"),
                            metadataDict.setdefault("number", "NULL"),
                            metadataDict.setdefault("issueID", "NULL"),
                            metadataDict.setdefault("date", "NULL"),
                            metadataDict.setdefault("writer", "NULL"),
                            path))
            con.commit()

    con.close()
    cursor.close()


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
	    'issueID'	    INTEGER UNIQUE, \
	    'dateCreated'   TEXT, \
	    'writer'        TEXT, \
            'path'          TEXT NOT NULL UNIQUE, \
	    PRIMARY KEY('id' AUTOINCREMENT) \
    );")

    con.commit()
    con.close()
    cursor.close()


def query_database(query):
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()
    cursor.execute(query)

    con.commit()
    return cursor.fetchall()


def insert_comic(title, type, series, number, issueID, dateCreated, writer, path):
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    cursor.execute(
        "INSERT INTO comics(title, type, series, number, issueID, dateCreated, writer, path) \
        Values (?, ?, ?, ?, ?, ?, ?, ?)", (title, type, series, number, issueID, dateCreated, writer, path))
    con.commit()
    con.close()
    cursor.close()


def clear_database():
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    cursor.executescript(
        "DELETE FROM comics;\
        UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='comics';"
    )
    con.commit()
    con.close()
    cursor.close()


def get_all_comic_info():
    comicList = query_database(
        'SELECT * FROM comics'
    )
    return comicList


def search(text):
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()
    cursor.execute(
        "SELECT * FROM comics WHERE title LIKE ? OR type LIKE ? OR series LIKE ? OR number LIKE ? OR issueID LIKE "
        "? OR dateCreated LIKE ? OR writer LIKE ? OR path LIKE ?",
        ('%' + str(text) + '%', '%' + str(text) + '%', '%' + str(text) + '%', '%' + str(text) + '%',
         '%' + str(text) + '%', '%' + str(text) + '%', '%' + str(text) + '%', '%' + str(text) + '%')
    )
    return cursor.fetchall()


def main():
    create_database()


if __name__ == "__main__":
    main()
