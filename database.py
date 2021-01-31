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
            try:
                with zip_file.open(filename) as f:
                    xmldoc = minidom.parse(f)

                    if len(xmldoc.getElementsByTagName("Notes")) == 0:
                        print("no issueID found")
                        metadataDict["issueID"] = 'NULL'
                    else:
                        metadataDict["issueID"] = xmldoc.getElementsByTagName('Notes')[0].firstChild.data.split('[')[1].split(' ')[2].split(']')[0]

                    if len(xmldoc.getElementsByTagName("Series")) == 0:
                        print("no series found")
                        metadataDict["series"] = 'NULL'
                    else:
                        metadataDict["series"] = xmldoc.getElementsByTagName('Series')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Number")) == 0:
                        print("no issue number found")
                        metadataDict["number"] = 'NULL'
                    else:
                        metadataDict["number"] = xmldoc.getElementsByTagName('Number')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Title")) == 0:
                        print("no title found")
                        metadataDict["title"] = 'NULL'
                    else:
                        metadataDict["title"] = xmldoc.getElementsByTagName('Title')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Year")) == 0:
                        print("no year found")
                    else:
                        year = xmldoc.getElementsByTagName('Year')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Month")) == 0:
                        print("no month found")
                    else:
                        month = xmldoc.getElementsByTagName('Month')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Day")) == 0:
                        print("no day found")
                    else:
                        day = xmldoc.getElementsByTagName('Day')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Writer")) == 0:
                        print("no writer found")
                        metadataDict["writer"] = 'NULL'
                    else:
                        metadataDict["writer"] = xmldoc.getElementsByTagName('Writer')[0].firstChild.data

                    
                    if len(xmldoc.getElementsByTagName("Penciller")) == 0:
                        print("no penciller found")
                        metadataDict["penciller"] = 'NULL'
                    else:
                        metadataDict["penciller"] = xmldoc.getElementsByTagName('Penciller')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Inker")) == 0:
                        print("no inker found")
                        metadataDict["inker"] = 'NULL'
                    else:
                        metadataDict["inker"] = xmldoc.getElementsByTagName('Inker')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Letterer")) == 0:
                        print("no letterer artist found")
                        metadataDict["letterer"] = 'NULL'
                    else:
                        metadataDict["letterer"] = xmldoc.getElementsByTagName('Letterer')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("CoverArtist")) == 0:
                        print("no cover artist found")
                        metadataDict["cover artist"] = 'NULL'
                    else:
                        metadataDict["cover artist"] = xmldoc.getElementsByTagName('CoverArtist')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Editor")) == 0:
                        print("no editor found")
                        metadataDict["editor"] = 'NULL'
                    else:
                        metadataDict["editor"] = xmldoc.getElementsByTagName('Editor')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Publisher")) == 0:
                        print("no publisher found")
                        metadataDict["publisher"] = 'NULL'
                    else:
                        metadataDict["publisher"] = xmldoc.getElementsByTagName('Publisher')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Web")) == 0:
                        print("no metadata source found")
                        metadataDict["metadata source"] = 'NULL'
                    else:
                        metadataDict["metadata source"] = xmldoc.getElementsByTagName('Web')[0].firstChild.data
                        

                    if len(xmldoc.getElementsByTagName("PageCount")) == 0:
                        print("no pageCount found")
                        metadataDict["pagecount"] = 'NULL'
                    else:
                        metadataDict["page count"] = xmldoc.getElementsByTagName('PageCount')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Characters")) == 0:
                        print("no characters found")
                        metadataDict["characters"] = 'NULL'
                    else:
                        metadataDict["characters"] = xmldoc.getElementsByTagName('Characters')[0].firstChild.data


                    if len(xmldoc.getElementsByTagName("Locations")) == 0:
                        print("no locations found")
                        metadataDict["locations"] = 'NULL'
                    else:
                        metadataDict["locations"] = xmldoc.getElementsByTagName('Locations')[0].firstChild.data

                    releaseDate = datetime.datetime(int(year),int(month),int(day))
                    metadataDict["date"] = releaseDate.strftime("%Y/%m/%d")
                    print(metadataDict)
                    return metadataDict
            except:
                print("no ComicInfo.xml found")
    except:
            print("unable to open zip file")
    return metadataDict


 # need to find a way to determine type
 # need to handle dates
 # need to populate creators
 # need to link the tables
def populate_database(basePath):
    listOfFiles = obtainListOfPaths(basePath)    
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    for path in listOfFiles:
        if path.endswith("cbz"):
            metadataDict = extractMetadata(path,"ComicInfo.xml")

            try:
                cursor.execute('''INSERT OR IGNORE INTO Comics(title, type, series, number, issueID, dateCreated, path) VALUES (?,?,?,?,?,?,?)''', (str(metadataDict["title"]), "issue" ,str(metadataDict["series"]),metadataDict["number"], metadataDict["issueID"],str(metadataDict["date"]),str(path)))
            except:
                 print("unable to add "+ path)
    con.commit()



def create_database():
    con = sqlite3.connect('main.db')
    con.execute("PRAGMA foreign_keys = on")
    cursor = con.cursor()

    # add path
    # creates Comics table
    cursor.execute("CREATE TABLE IF NOT EXISTS 'comics' ( \
	    'id'	    INTEGER NOT NULL, \
	    'title'	    TEXT, \
	    'type'	    TEXT, \
	    'series'	    TEXT, \
	    'number'	    INTEGER, \
	    'issueID'	    INTEGER, \
	    'dateCreated'   TEXT, \
            'path'          TEXT, \
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
    cursor.execute("CREATE TABLE IF NOT EXISTS 'creatorComics' ( \
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
    tempPath = "/home/gianni/Documents/code/python/comicbooks/Batman Damned (1-3)/Batman_ Damned #1 - Brian Azzarello.cbz"
    # test  = extractMetadata(tempPath, "ComicInfo.xml")
    # print(test)
    populate_database("/home/gianni/.comicOrchard/main")


if __name__ == "__main__":
    main()
