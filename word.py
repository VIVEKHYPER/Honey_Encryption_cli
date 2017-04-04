import random


def return_honey():
    words = [line.strip() for line in
             open('/home/vivek/HoneyEncryption/docs/source codes/diceware-master/diceware/wordlists/wordlist_en.txt')]
    h = random.randint(2, 5)
    a = []
    length = 0
    sp_char = ["@", "|", "/", "#", '/', ".", "$", "*", "&", "_"]
    for i in range(h):
        str1 = random.choice(words)
        str1.title()
        a.insert(i, str1)
        choice = random.randint(0, 1)
        if choice == 1:
            str2 = random.choice(sp_char)
            a.insert(i, str2)
        e = ("".join(str(x) for x in set(a)))
        length = len(e)
    if length < 8:
        str1 = random.choice(words)
        str1.title()
        # print(e + str1)
        return (e + str1)
    else:
        # print((e).title())
        return ((e).title())


if __name__ == '__main__':
    print(return_honey())
