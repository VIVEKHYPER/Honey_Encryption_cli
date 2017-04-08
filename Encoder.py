import nltk
import pickle
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
import math


def gen_words(bstring):
    with open('Wordlist/wordlist', 'rb') as fp:
        itemlist = pickle.load(fp)
    fp.close()
    index = []
    temp = bstring

    while temp > 0:
        t = temp % 16384
        t = t % 15546
        temp = int(temp / 16384)
        if t != 0:
            index.append(t)

    result = []

    for x in index:
        if x % 2 == 0:
            result.append(itemlist[x - 1])
        else:
            result.append(itemlist[x - 1].title())
    return result


def gen_sp(bstring):
    special = ['|', '!', '#', '$', '%', '&', '/', '~', '*', '+', '-', ':', '_', '?', '@']
    index = []
    temp = bstring
    while temp > 0:
        t = temp % 16
        temp = int(temp / 16)
        index.append(t)

    result = []
    for x in index:
        result.append(special[x - 1])
    return result
    # print(index)


def makehoney(word_list, wcount, sp_list, spcount):
    # str1 = word_list[0:wcount+1]
    # str1 = str1 + (sp_list[0:spcount+1])
    str1 = word_list[0:wcount + 1]
    if spcount != 0:
        str2 = sp_list[0:spcount + 1]
        str3 = [item for pair in zip(str1, str2) for item in pair]
    else:
        str3 = str1
    result = ''.join(str3)
    while len(result) < 8:
        str3 = (str3 + word_list[wcount:wcount + 1])
        result = ''.join(str3)
    i = 0
    while len(result) > 32:
        del str3[i:i + 1]
        result = ''.join(str3)
        i = i + 2
    return result


def gen_honey(bstring):
    # bstring = int(input("Enter hex"), 16)
    temp1 = int(bstring % (pow(2, 71)))
    bstring = int(bstring / (pow(2, 71)))
    spstring = int(bstring % (pow(2, 41)))
    word_list = gen_words(temp1)
    sp_list = gen_sp(spstring)
    bstring = int(bstring / (pow(2, 41)))
    spcount = int(bstring % 16)
    wcount = int(bstring / 16) % 6
    honeyword = makehoney(word_list, wcount, sp_list, spcount)
    # print(honeyword)
    return honeyword


if __name__ == '__main__':
    bstring = int(input("Enter hex"), 16)
    gen_honey(bstring)
