#!/usr/bin/python3
from __future__ import division, absolute_import, print_function
from Encoder import gen_honey

import ast
import errno
import hashlib
import math
import os
import os.path
import sqlite3
from shutil import copyfile

from Crypto import Random
from Crypto.PublicKey import RSA
from des import encrypt_file, decrypt_file  # Importing methods encrypt_file, decrypt_file from des.py
from word import return_honey


def pad(pas):
    count = len(pas)
    p = count % 16
    if p != 0:
        s = count / 16
        i = math.ceil(s)
        return pas.ljust(16 * i, '0')
    else:
        return pas


def db_management():
    global username, password, fo, sha, conn
    print("______________Welcome to Honey Encryption______________")
    if os.path.isfile("test.db"):  # Checks whether there is file named test.db
        log_in("vivek", "password")  # log in to account
        exit_update_db()

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

        encrypt_file('privkey', 'privkey.enc', 8192, pad(password), iv)  # Encrypting private key to privkey.enc
        os.remove("privkey")  # Removing unencrypted file privkey

        conn = sqlite3.connect('test.db')
        print("opened database successfully")
        conn.execute(
            '  CREATE TABLE INTERNET (id INTEGER PRIMARY KEY   AUTOINCREMENT,\n'  # Creating new database  test.db and assigning fields
            '                                          title    TEXT    NOT NULL,\n'
            '                                          url      TEXT    NOT NULL,\n'
            '                                          username CHAR(50),\n'
            '                                          password CHAR(50));  ')
        ch = input("Do you want to log in?(y/n)")

        # if ch == 'y':
        #     log_in()
        # else:
        #     conn.close()


def log_in(user, pas):
    global username, password
    global conn, sha, fo
    print("_______Login Database________")  # Logging in to database
    username = user
    password = pas
    conn = sqlite3.connect('test.db')
    print("opened database successfully")
    sha = hashlib.sha3_256(
        (username + password).encode('utf-8')).hexdigest()  # Finding hash of entered username and password
    fo = open("hash.txt", "r")
    if sha == fo.read():  # Comparing calculated hash with hash value stored in file
        print("Logged In successfully!")
        fo = open("iv", "rb")
        iv = fo.read()  # Reading initialization vector for decrypting by using 3 DES
        fo.close()

        decrypt_file('privkey.enc', 'privkey.dec', 8192, pad(password), iv)  # Decrypting private key by using 3 DES

        fo = open('privkey.dec', 'rb')
        privkey = fo.read()  # Reading decrypted private key to variable
        fo.close()

        os.remove("privkey.dec")  # Deleting decrypted key file inorder to prevent key leakage
        privkey = RSA.importKey(privkey)  # Importing key to algorithm

        cursor = conn.execute("SELECT id, title, url, username, password  FROM INTERNET")
        i = 0
        for row in cursor:
            i += 1
            print("ID = ", row[0])
            print("Title = ", row[1])
            print("URL= ", row[2])
            print("Username = ", row[3])
            pas = row[4]

            #    pas = privkey.decrypt(pas)  # Decrypting password using RSA
            pas_tuple = ast.literal_eval(pas)  # Converting encrypted string to tuple
            pas = privkey.decrypt(pas_tuple)  # Decrypting password using RSA
            # pas = privkey.decrypt(pas)  # Decrypting password using RSA
            pas = pas.decode('utf-8')
            print("Password = ", pas, "\n")  # Printing Decrypted password
            # pas_list.append(pas.decode('utf-8'))
            sql = (' UPDATE INTERNET\n'
                   '                  SET password = ?\n'
                   '                  WHERE id = ?')
            cur = conn.cursor()
            cur.execute(sql, (pas, i,))
        ##############################################################################
        cursor = conn.execute("SELECT id, title, url, username, password  FROM EMAILS")
        i = 0
        for row in cursor:
            i += 1
            print("ID = ", row[0])
            print("Title = ", row[1])
            print("URL= ", row[2])
            print("Username = ", row[3])
            pas = row[4]

            #    pas = privkey.decrypt(pas)  # Decrypting password using RSA
            pas_tuple = ast.literal_eval(pas)  # Converting encrypted string to tuple
            pas = privkey.decrypt(pas_tuple)  # Decrypting password using RSA
            # pas = privkey.decrypt(pas)  # Decrypting password using RSA
            pas = pas.decode('utf-8')
            print("Password = ", pas, "\n")  # Printing Decrypted password
            # pas_list.append(pas.decode('utf-8'))
            sql = (' UPDATE EMAILS\n'
                   '                  SET password = ?\n'
                   '                  WHERE id = ?')
            cur = conn.cursor()
            cur.execute(sql, (pas, i,))
        ##############################################################################
        cursor = conn.execute("SELECT id, title, url, password  FROM PINS")
        i = 0
        for row in cursor:
            i += 1
            print("ID = ", row[0])
            print("Title = ", row[1])
            print("URL= ", row[2])
            pas = row[3]

            #    pas = privkey.decrypt(pas)  # Decrypting password using RSA
            pas_tuple = ast.literal_eval(pas)  # Converting encrypted string to tuple
            pas = privkey.decrypt(pas_tuple)  # Decrypting password using RSA
            # pas = privkey.decrypt(pas)  # Decrypting password using RSA
            pas = pas.decode('utf-8')
            print("Password = ", pas, "\n")  # Printing Decrypted password
            # pas_list.append(pas.decode('utf-8'))
            sql = (' UPDATE PINS\n'
                   '                  SET password = ?\n'
                   '                  WHERE id = ?')
            cur = conn.cursor()
            cur.execute(sql, (pas, i,))
            ##############################################################################
        cursor = conn.execute("SELECT id, title, url, username, password  FROM OTHERS")
        i = 0
        for row in cursor:
            i += 1
            print("ID = ", row[0])
            print("Title = ", row[1])
            print("URL= ", row[2])
            print("Username = ", row[3])
            pas = row[4]

            #    pas = privkey.decrypt(pas)  # Decrypting password using RSA
            pas_tuple = ast.literal_eval(pas)  # Converting encrypted string to tuple
            pas = privkey.decrypt(pas_tuple)  # Decrypting password using RSA
            pas = pas.decode('utf-8')
            print("Password = ", pas, "\n")  # Printing Decrypted password
            # pas_list.append(pas.decode('utf-8'))
            sql = (' UPDATE OTHERS\n'
                   '                  SET password = ?\n'
                   '                  WHERE id = ?')
            cur = conn.cursor()
            cur.execute(sql, (pas, i,))
            ##############################################################################

        conn.commit()
        conn.close()
        return 1

    else:  # If enteres  password is wrong deny access by generating honeywords
        print("Access Denied")
        copyfile('test.db', 'fake.db')
        bstring = sha[0:30]
        adder = sha[30:57]
        hex_str = bstring
        hex_int = int(hex_str, 16)
        bstring2 = hex_int + 0x200

        hex_str = adder
        hex_int = int(hex_str, 16)
        adder2 = hex_int + 0x200
        conn = sqlite3.connect('fake.db')
        cursor = conn.execute("SELECT id, password  FROM INTERNET")
        add = bstring2
        i = 0
        for row in cursor:
            i += 1
            pas = gen_honey(add)
            add = add + adder2
            sql = (' UPDATE INTERNET\n'
                   '                  SET password = ?\n'
                   '                  WHERE id = ?')
            cur = conn.cursor()
            cur.execute(sql, (pas, i,))
        ####################################################################################
        cursor = conn.execute("SELECT id, password  FROM EMAILS")
        i = 0
        for row in cursor:
            i += 1
            pas = gen_honey(add)
            add = add + adder2
            sql = (' UPDATE EMAILS\n'
                   '                  SET password = ?\n'
                   '                  WHERE id = ?')
            cur = conn.cursor()
            cur.execute(sql, (pas, i,))
        ####################################################################################
        cursor = conn.execute("SELECT id, password  FROM PINS")
        i = 0
        for row in cursor:
            i += 1
            pas = gen_honey(add)
            add = add + adder2
            sql = (' UPDATE PINS\n'
                   '                  SET password = ?\n'
                   '                  WHERE id = ?')
            cur = conn.cursor()
            cur.execute(sql, (pas, i,))
        ####################################################################################
        cursor = conn.execute("SELECT id,password  FROM OTHERS")
        i = 0
        for row in cursor:
            i += 1
            pas = gen_honey(add)
            add = add + adder2
            sql = (' UPDATE OTHERS\n'
                   '                  SET password = ?\n'
                   '                  WHERE id = ?')
            cur = conn.cursor()
            cur.execute(sql, (pas, i,))
        ####################################################################################

        conn.commit()
        conn.close()
        return 0


def exit_update_db():
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT id, password  FROM INTERNET")
    fo = open("pubkey", "rb")
    pubkey = fo.read()
    pubkey = RSA.importKey(pubkey)
    fo.close()
    i = 0
    for row in cursor:
        i += 1
        pas = row[1]
        # pas_list.append(pas.decode('utf-8'))
        pas = str(pas)
        pas = pubkey.encrypt(pas.encode('utf-8'), 16)
        print(pas)
        sql = (' UPDATE INTERNET\n'
               '                  SET password = ?\n'
               '                  WHERE id = ?')
        cur = conn.cursor()
        pas = str(pas)
        cur.execute(sql, (pas, i,))
    #############################################################################################
    cursor = conn.execute("SELECT id, password  FROM EMAILS")
    i = 0
    for row in cursor:
        i += 1
        pas = row[1]
        # pas_list.append(pas.decode('utf-8'))
        pas = str(pas)
        pas = pubkey.encrypt(pas.encode('utf-8'), 16)
        print(pas)
        sql = (' UPDATE EMAILS\n'
               '                  SET password = ?\n'
               '                  WHERE id = ?')
        cur = conn.cursor()
        pas = str(pas)
        cur.execute(sql, (pas, i,))
    #############################################################################################
    cursor = conn.execute("SELECT id, password  FROM PINS")
    i = 0
    for row in cursor:
        i += 1
        pas = row[1]
        # pas_list.append(pas.decode('utf-8'))
        pas = str(pas)
        pas = pubkey.encrypt(pas.encode('utf-8'), 16)
        print(pas)
        sql = (' UPDATE PINS\n'
               '                  SET password = ?\n'
               '                  WHERE id = ?')
        cur = conn.cursor()
        pas = str(pas)
        cur.execute(sql, (pas, i,))
    #############################################################################################
    cursor = conn.execute("SELECT id, password  FROM OTHERS")

    i = 0
    for row in cursor:
        i += 1
        pas = row[1]
        # pas_list.append(pas.decode('utf-8'))
        pas = str(pas)
        pas = pubkey.encrypt(pas.encode('utf-8'), 16)
        print(pas)
        sql = (' UPDATE OTHERS\n'
               '                  SET password = ?\n'
               '                  WHERE id = ?')
        cur = conn.cursor()
        pas = str(pas)
        cur.execute(sql, (pas, i,))
    conn.commit()
    conn.close()


#################################################################################################


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
                     '                            INTERNET (title, url, username, password)\n'
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

    sql = (' UPDATE INTERNET\n'
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

    decrypt_file('privkey.enc', 'privkey.dec', 8192, pad(password), iv)  # Decrypting private key by using 3 DES

    fo = open('privkey.dec', 'rb')
    privkey = fo.read()  # Reading decrypted private key to variable
    fo.close()

    os.remove("privkey.dec")  # Deleting decrypted key file inorder to prevent key leakage
    privkey = RSA.importKey(privkey)  # Importing key to algorithm

    cursor = conn.execute("SELECT id, title, url, username, password  FROM INTERNET")
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
    sql = 'DELETE FROM INTERNET WHERE id=?'
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


def delete_fake_db():  # Deleting entire database
    try:
        os.remove("fake.db")  # Removing test.db
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred
    conn.close()


def create_db(username, password):
    print("-------Create Database--------")
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

    encrypt_file('privkey', 'privkey.enc', 8192, pad(password), iv)  # Encrypting private key to privkey.enc
    os.remove("privkey")  # Removing unencrypted file privkey

    conn = sqlite3.connect('test.db')
    print("opened database successfully")
    conn.execute(
        '  CREATE TABLE INTERNET (id INTEGER PRIMARY KEY   AUTOINCREMENT,\n'  # Creating new database  test.db and assigning fields
        '                                          title    TEXT    NOT NULL,\n'
        '                                          url      TEXT    NOT NULL,\n'
        '                                          username CHAR(50),\n'
        '                                          password CHAR(50));  ')
    conn.execute(
        '  CREATE TABLE EMAILS (id INTEGER PRIMARY KEY   AUTOINCREMENT,\n'  # Creating new database  test.db and assigning fields
        '                                          title    TEXT    NOT NULL,\n'
        '                                          url      TEXT    NOT NULL,\n'
        '                                          username CHAR(50),\n'
        '                                          password CHAR(50));  ')
    conn.execute(
        '  CREATE TABLE PINS (id INTEGER PRIMARY KEY   AUTOINCREMENT,\n'  # Creating new database  test.db and assigning fields
        '                                          title    TEXT    NOT NULL,\n'
        '                                          url      TEXT    NOT NULL,\n'
        '                                          password CHAR(50));  ')
    conn.execute(
        '  CREATE TABLE OTHERS (id INTEGER PRIMARY KEY   AUTOINCREMENT,\n'  # Creating new database  test.db and assigning fields
        '                                          title    TEXT    NOT NULL,\n'
        '                                          url      TEXT    NOT NULL,\n'
        '                                          username CHAR(50),\n'
        '                                          password CHAR(50));  ')
    conn.close()


def main():
    # log_in("vivek", "password")
    exit_update_db()
    # select_db()


if __name__ == '__main__':
    main()
