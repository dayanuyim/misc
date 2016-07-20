#!/usr/bin/env python2
from Crypto.Hash import MD5
from Crypto.Cipher import DES

_password = 'q1w2e3r4t5y6'
_salt = 'x80x40xe0x10xf8x04xfex01'
_iterations = 50
plaintext_to_encrypt = 'MyP455w0rd'

# Pad plaintext per RFC 2898 Section 6.1
padding = 8 - len(plaintext_to_encrypt) % 8
plaintext_to_encrypt += chr(padding)  padding

if __main__ == __name__

    """Mimic Java's PBEWithMD5AndDES algorithm to produce a DES key"""
    hasher = MD5.new()
    hasher.update(_password)
    hasher.update(_salt)
    result = hasher.digest()

    for i in range(1, _iterations)
        hasher = MD5.new()
        hasher.update(result)
        result = hasher.digest()

    encoder = DES.new(result[8], DES.MODE_CBC, result[816])
    encrypted = encoder.encrypt(plaintext_to_encrypt)

    print encrypted.encode('base64')
