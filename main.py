#!/usr/bin/python3
import errno
import hashlib
import os
import os.path
import sqlite3


def log_in():
    global username, password, conn, sha, fo
    print("_______Login Database________")
    username = input("Enter Username")
    password = input("Enter Password")
    conn = sqlite3.connect('test.db')
    print("opened database successfully")
    sha = hashlib.sha3_256((password + username).encode('utf-8')).hexdigest()
    fo = open("hash.txt", "r")
    if sha == fo.read():
        print("Logged In successfully!")
        ch = 'l'

        while ch == 'l':
            print("Choose options:")
            print("1 -> Show Entries")
            print("2 -> New Entry")
            print("3 -> Edit Entry")
            print("4 -> Delete Entry")
            print("5 -> Delete Entire Database")
            choice1 = input()

            if choice1 == '1':
                select_db()

            elif choice1 == '2':
                insert_db()

            elif choice1 == '3':
                update_db()

            elif choice1 == '4':
                delete_db()

            elif choice1 == '5':
                delete_all_db()
                exit()

            ch = input("Enter 'l' for options and 'q' to exit ")

        conn.close()

    else:
        print("Access Denied")


def insert_db():
    ch = 'y'
    while ch == 'y':
        # print("Enter row to insert:")
        # id = int(input("Enter id:"))
        title = input("Enter title:")
        url = input("Enter URL:")
        user = input("Enter Username:")
        pas = input("Enter Password:")
        conn.execute('''INSERT INTO
                            ENTRIES (title, url, username, password)
                            VALUES(?, ?, ?, ?)''', (title, url, user, pas))
        print("Item inserted")
        ch = input("Enter 'y' to insert again and 'q' to go back ")
    conn.commit()


def select_db():
    cursor = conn.execute("SELECT id, title, url, username, password  FROM ENTRIES")
    for row in cursor:
        print("ID = ", row[0])
        print("Title = ", row[1])
        print("URL= ", row[2])
        print("Username = ", row[3])
        print("Password = ", row[4], "\n")


def delete_db():
    id = int(input("Enter Id of row to be updated"))
    sql = 'DELETE FROM ENTRIES WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    print("Row ", id, " deleted")
    conn.commit()


def delete_all_db():
    try:
        os.remove("test.db")
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
    conn.close()


def update_db():
    id = int(input("Enter Id of row to be updated"))
    title = input("Enter title:")
    url = input("Enter URL:")
    user = input("Enter Username:")
    pas = input("Enter Password:")
    sql = ''' UPDATE ENTRIES
                  SET title = ? ,
                      url = ? ,
                      username = ?,
                      password = ?
                  WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (title, url, user, pas, id,))
    conn.commit()


print("______________Welcome to Honey Encryption______________")
if os.path.isfile("test.db"):
    log_in()

else:
    print("-------Create Database--------")
    username = input("Enter Username")
    password = input("Enter Password")
    fo = open("hash.txt", "w")
    sha = hashlib.sha3_256((password + username).encode('utf-8')).hexdigest()
    fo.write(sha)
    print("sha:" + sha)
    fo.close()
    conn = sqlite3.connect('test.db')
    print("opened database successfully")
    conn.execute('''  CREATE TABLE ENTRIES (id INTEGER PRIMARY KEY   AUTOINCREMENT,
                                          title    TEXT    NOT NULL,
                                          url      TEXT    NOT NULL,
                                          username CHAR(50),
                                          password CHAR(50));  ''')
    ch = input("Do you want to log in?(y/n)")
    if ch == 'y':
        log_in()
    else:
        conn.close()
