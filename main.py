#!/usr/bin/python3
from __future__ import division, absolute_import, print_function

import ast
import errno
import hashlib
import os
import os.path
import sqlite3

from Crypto import Random
from Crypto.PublicKey import RSA
from des import encrypt_file, decrypt_file  # Importing methods encrypt_file, decrypt_file from des.py


def db_management():
    global username, password, fo, sha, conn
    print("______________Welcome to Honey Encryption______________")
    if os.path.isfile("test.db"):  # Checks whether there is file named test.db
        log_in()  # log in to account

    else:  # If there is no test.db file then Create new Database
        print("-------Create Database--------")
        username = input("Enter Username")
        password = input("Enter Password")

        fo = open("hash.txt", "w")  # Create file called hash.txt for storing password hash of main password
        sha = hashlib.sha3_256(
            (username + password).encode('utf-8')).hexdigest()  # Find hash of (Username+Password) using sha3 algorithm
        fo.write(sha)  # Store Hash
        print("sha:" + sha)
        fo.close()

        random_generator = Random.new().read  # Initialize Random key generator
        key = RSA.generate(1024, random_generator)  # Generate a Random key

        fo = open("pubkey", "wb")
        fo.write(key.publickey().exportKey())  # Storing public key as file after exporting
        fo.close()

        fo = open("privkey", "wb")
        fo.write(key.exportKey())  # Storing private key as file after exporting
        fo.close()

        iv = Random.get_random_bytes(8)  # Generating Initialization vector for 3 DES and storing
        fo = open("iv", "wb")
        fo.write(iv)
        fo.close()

        encrypt_file('privkey', 'privkey.enc', 8192, password, iv)  # Encrypting private key to privkey.enc
        os.remove("privkey")  # Removing unencrypted file privkey

        conn = sqlite3.connect('test.db')
        print("opened database successfully")
        conn.execute(
            '  CREATE TABLE ENTRIES (id INTEGER PRIMARY KEY   AUTOINCREMENT,\n'  # Creating new database  test.db and assigning fields
            '                                          title    TEXT    NOT NULL,\n'
            '                                          url      TEXT    NOT NULL,\n'
            '                                          username CHAR(50),\n'
            '                                          password CHAR(50));  ')
        ch = input("Do you want to log in?(y/n)")
        if ch == 'y':
            log_in()
        else:
            conn.close()


def log_in():
    global username, password, conn, sha, fo
    print("_______Login Database________")  # Logging in to database
    username = input("Enter Username")
    password = input("Enter Password")
    conn = sqlite3.connect('test.db')
    print("opened database successfully")
    sha = hashlib.sha3_256(
        (username + password).encode('utf-8')).hexdigest()  # Finding hash of entered username and password
    fo = open("hash.txt", "r")
    if sha == fo.read():  # Comparing calculated hash with hash value stored in file
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

    else:  # If enteres  password is wrong deny access by generating honeyewords
        print("Access Denied")


def insert_db():
    ch = 'y'
    while ch == 'y':
        title = input("Enter title:")
        url = input("Enter URL:")
        user = input("Enter Username:")
        pas = input("Enter Password:")

        fo = open("pubkey", "rb")
        pubkey = fo.read()  # Reading public key
        pubkey = RSA.importKey(pubkey)  # Importing pubkey to RSA algorithm
        fo.close()

        pas = pubkey.encrypt(pas.encode('utf-8'), 16)  # Encrypting password after encoding it to unicode string
        pas = str(pas)  # Converting type Tuple to string
        conn.execute('INSERT INTO\n'  # Inserting Items
                     '                            ENTRIES (title, url, username, password)\n'
                     '                            VALUES(?, ?, ?, ?)', (title, url, user, pas))
        print("Item inserted")
        ch = input("Enter 'y' to insert again and 'q' to go back ")
    conn.commit()


def update_db():
    id = int(input("Enter Id of row to be updated"))
    title = input("Enter title:")
    url = input("Enter URL:")
    user = input("Enter Username:")
    pas = input("Enter Password:")

    fo = open("pubkey", "rb")
    pubkey = fo.read()
    pubkey = RSA.importKey(pubkey)
    fo.close()

    pas = pubkey.encrypt(pas.encode('utf-8'), 16)
    print(type(pas))
    pas = str(pas)

    sql = (' UPDATE ENTRIES\n'
           '                  SET title = ? ,\n'
           '                      url = ? ,\n'
           '                      username = ?,\n'
           '                      password = ?\n'
           '                  WHERE id = ?')
    cur = conn.cursor()
    cur.execute(sql, (title, url, user, pas, id,))
    conn.commit()


def select_db():  # Viewing data database entries
    fo = open("iv", "rb")
    iv = fo.read()  # Reading initialization vector for decrypting by using 3 DES
    fo.close()

    decrypt_file('privkey.enc', 'privkey.dec', 8192, password, iv)  # Decrypting private key by using 3 DES

    fo = open('privkey.dec', 'rb')
    privkey = fo.read()  # Reading decrypted private key to variable
    fo.close()

    os.remove("privkey.dec")  # Deleting decrypted key file inorder to prevent key leakage
    privkey = RSA.importKey(privkey)  # Importing key to algorithm

    cursor = conn.execute("SELECT id, title, url, username, password  FROM ENTRIES")
    for row in cursor:
        print("ID = ", row[0])
        print("Title = ", row[1])
        print("URL= ", row[2])
        print("Username = ", row[3])
        pas = row[4]
        pas_tuple = ast.literal_eval(pas)  # Converting encrypted string to tuple
        pas = privkey.decrypt(pas_tuple)  # Decrypting password using RSA
        print("Password = ", pas.decode('utf-8'), "\n")  # Printing Decrypted password


def delete_db():
    id = int(input("Enter Id of row to be deleted"))
    sql = 'DELETE FROM ENTRIES WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    print("Row ", id, " deleted")
    conn.commit()


def delete_all_db():  # Deleting entire database
    try:
        os.remove("test.db")  # Removing test.db
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
    conn.close()



def main():
    db_management()


if __name__ == '__main__':
    main()
