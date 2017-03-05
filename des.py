from Crypto.Cipher import DES3


def encrypt_file(in_filename, out_filename, chunk_size, key, iv):
    des3 = DES3.new(key, DES3.MODE_CFB, iv)

    with open(in_filename, 'r') as in_file:
        with open(out_filename, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                out_file.write((des3.encrypt(chunk)))


def decrypt_file(in_filename, out_filename, chunk_size, key, iv):
    des3 = DES3.new(key, DES3.MODE_CFB, iv)

    with open(in_filename, 'rb') as in_file:
        with open(out_filename, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                out_file.write((des3.decrypt(chunk)))


'''
key = 'passwordpassword'
iv = Random.get_random_bytes(8)
with open('pubkey.txt', 'r') as f:
    print('pubkey.txt: %s' % f.read())
encrypt_file('pubkey.txt', 'to_enc.enc', 8192, key, iv)
with open('to_enc.enc', 'r',encoding='utf-8', errors='ignore') as f:
    print('to_enc.enc: %s' % f.read())


decrypt_file('to_enc.enc', 'to_enc.dec', 8192, key, iv)
with open('to_enc.dec', 'r') as f:
    print('to_enc.dec: %s' % f.read())

'''
