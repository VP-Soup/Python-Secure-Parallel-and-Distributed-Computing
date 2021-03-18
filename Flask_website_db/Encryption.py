# Note: the following code is adapted from the Module 7 code from COP4521

import base64
from Cryptodome.Cipher import AES


class AESCipher(object):
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv


    def encrypt(self, plaintext):
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        cipher_text = self.cipher.encrypt(plaintext)
        encoded = base64.b64encode(cipher_text)
        return encoded

    def decrypt(self, encoded):
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        decoded = base64.b64decode(encoded)
        plaintext = self.cipher.decrypt(decoded)
        return str(plaintext, 'utf-8')


key = b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'
iv = b'OWFJATh1Zowac2xr'

cipher = AESCipher(key, iv)
