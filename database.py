import sqlite3


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
