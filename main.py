#!/usr/bin/python3
from __future__ import division, absolute_import, print_function

import errno
import hashlib
import os
import os.path
import sqlite3
import sys
from base64 import b64encode
from binascii import hexlify, unhexlify
from collections import namedtuple
from fractions import gcd
from math import log
from random import randrange

from Crypto import Random
from des import encrypt_file


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
        fo = open("pubkey.txt", "r")
        pubkey = str_to_key(fo.read())
        fo.close()
        pas = encode(pas, pubkey, True)
        pas = b64encode(pas).decode()

        conn.execute('INSERT INTO\n'
                     '                            ENTRIES (title, url, username, password)\n'
                     '                            VALUES(?, ?, ?, ?)', (title, url, user, pas))
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
    id = int(input("Enter Id of row to be deleted"))
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
    sql = (' UPDATE ENTRIES\n'
           '                  SET title = ? ,\n'
           '                      url = ? ,\n'
           '                      username = ?,\n'
           '                      password = ?\n'
           '                  WHERE id = ?')
    cur = conn.cursor()
    cur.execute(sql, (title, url, user, pas, id,))
    conn.commit()


def db_management():
    global username, password, fo, sha, conn
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

        pubkey, privkey = keygen(2 ** 64)
        fo = open("pubkey.txt", "w")
        str_txt = key_to_str(pubkey)
        fo.write(str_txt)
        fo.close()

        fo = open("privkey.txt", "w")
        fo.write(key_to_str(privkey))
        fo.close()

        iv = Random.get_random_bytes(8)
        fo = open("iv", "wb")
        fo.write(iv)
        fo.close()

        encrypt_file('privkey.txt', 'to_enc.enc', 8192, password, iv)
        with open('to_enc.enc', 'r', encoding='utf-8', errors='ignore') as f:
            print('to_enc.enc: %s' % f.read())

        conn = sqlite3.connect('test.db')
        print("opened database successfully")
        conn.execute('  CREATE TABLE ENTRIES (id INTEGER PRIMARY KEY   AUTOINCREMENT,\n'
                     '                                          title    TEXT    NOT NULL,\n'
                     '                                          url      TEXT    NOT NULL,\n'
                     '                                          username CHAR(50),\n'
                     '                                          password CHAR(50));  ')
        ch = input("Do you want to log in?(y/n)")
        if ch == 'y':
            log_in()
        else:
            conn.close()


###############################################################################################################################################################
###############################################################################################################################################################
# coding=utf-8



PY3 = sys.version_info[0] == 3
if PY3:
    binary_type = bytes
    range_func = range
else:
    binary_type = str
    range_func = xrange


def is_prime(n, k=30):
    # http://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    if n <= 3:
        return n == 2 or n == 3
    neg_one = n - 1

    # write n-1 as 2^s*d where d is odd
    s, d = 0, neg_one
    while not d & 1:
        s, d = s + 1, d >> 1
    assert 2 ** s * d == neg_one and d & 1

    for _ in range_func(k):
        a = randrange(2, neg_one)
        x = pow(a, d, n)
        if x in (1, neg_one):
            continue
        for _ in range_func(s - 1):
            x = x ** 2 % n
            if x == 1:
                return False
            if x == neg_one:
                break
        else:
            return False
    return True


def randprime(n=10 ** 8):
    p = 1
    while not is_prime(p):
        p = randrange(n)
    return p


def multinv(modulus, value):
    """
        Multiplicative inverse in a given modulus

        >>> multinv(191, 138)
        18
        >>> multinv(191, 38)
        186
        >>> multinv(120, 23)
        47
    """
    # http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    x, lastx = 0, 1
    a, b = modulus, value
    while b:
        a, q, b = b, a // b, a % b
        x, lastx = lastx - q * x, x
    result = (1 - lastx * modulus) // value
    if result < 0:
        result += modulus
    assert 0 <= result < modulus and value * result % modulus == 1
    return result


KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')


def keygen(n, public=None):
    """ Generate public and private keys from primes up to N.

    Optionally, specify the public key exponent (65537 is popular choice).

        >>> pubkey, privkey = keygen(2**64)
        >>> msg = 123456789012345
        >>> coded = pow(msg, *pubkey)
        >>> plain = pow(coded, *privkey)
        >>> assert msg == plain

    """
    # http://en.wikipedia.org/wiki/RSA
    prime1 = randprime(n)
    prime2 = randprime(n)
    composite = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    if public is None:
        private = None
        while True:
            private = randrange(totient)
            if gcd(private, totient) == 1:
                break
        public = multinv(totient, private)
    else:
        private = multinv(totient, public)
    assert public * private % totient == gcd(public, totient) == gcd(private, totient) == 1
    assert pow(pow(1234567, public, composite), private, composite) == 1234567
    return KeyPair(Key(public, composite), Key(private, composite))


def encode(msg, pubkey, verbose=False):
    chunksize = int(log(pubkey.modulus, 256))
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (outchunk * 2,)
    bmsg = msg if isinstance(msg, binary_type) else msg.encode('utf-8')
    result = []
    for start in range_func(0, len(bmsg), chunksize):
        chunk = bmsg[start:start + chunksize]
        chunk += b'\x00' * (chunksize - len(chunk))
        plain = int(hexlify(chunk), 16)
        coded = pow(plain, *pubkey)
        bcoded = unhexlify((outfmt % coded).encode())
        if verbose:
            print('Encode:', chunksize, chunk, plain, coded, bcoded)
        result.append(bcoded)
    return b''.join(result)


def decode(bcipher, privkey, verbose=False):
    chunksize = int(log(privkey.modulus, 256))
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (chunksize * 2,)
    result = []
    for start in range_func(0, len(bcipher), outchunk):
        bcoded = bcipher[start: start + outchunk]
        coded = int(hexlify(bcoded), 16)
        plain = pow(coded, *privkey)
        chunk = unhexlify((outfmt % plain).encode())
        if verbose:
            print('Decode:', chunksize, chunk, plain, coded, bcoded)
        result.append(chunk)
    return b''.join(result).rstrip(b'\x00').decode('utf-8')


def key_to_str(key):
    """
    Convert `Key` to string representation
    >>> key_to_str(Key(50476910741469568741791652650587163073, 95419691922573224706255222482923256353))
    '25f97fd801214cdc163796f8a43289c1:47c92a08bc374e96c7af66eb141d7a21'
    """
    return ':'.join((('%%0%dx' % ((int(log(number, 256)) + 1) * 2)) % number) for number in key)


def str_to_key(key_str):
    """
    Convert string representation to `Key` (assuming valid input)
    >>> (str_to_key('25f97fd801214cdc163796f8a43289c1:47c92a08bc374e96c7af66eb141d7a21') ==
    ...  Key(exponent=50476910741469568741791652650587163073, modulus=95419691922573224706255222482923256353))
    True
    """
    return Key(*(int(number, 16) for number in key_str.split(':')))


def main():
    # key = 'passwordpassword'
    # iv = Random.get_random_bytes(8)
    # with open('pubkey.txt', 'r') as f:
    #     print('pubkey.txt: %s' % f.read())
    # encrypt_file('pubkey.txt', 'to_enc.enc', 8192, key, iv)
    # with open('to_enc.enc', 'r', encoding='utf-8', errors='ignore') as f:
    #     print('to_enc.enc: %s' % f.read())
    # decrypt_file('to_enc.enc', 'to_enc.dec', 8192, key, iv)
    # with open('to_enc.dec', 'r') as f:
    #     print('to_enc.dec: %s' % f.read())



    # import doctest
    # print(doctest.testmod())
    db_management()
    # msg = "password"
    # h = encode(msg, pubkey, True)
    # p = decode(h, privkey, True)
    # print('-' * 20)
    # print('message:', msg)
    # print('encoded:', b64encode(h).decode())
    # print('decoded:', p)


if __name__ == '__main__':
    main()
