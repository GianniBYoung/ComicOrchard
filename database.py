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
