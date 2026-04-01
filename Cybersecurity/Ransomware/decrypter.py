#decrypter.py

import os
import pyaes

## abrir o arquivo criptografado
file_name = "teste.txt.ransomwaretroll"

with open(file_name, "rb") as file:
    file_data = file.read()

## chave para descriptografia
    key = b"wnfdio.me.ransom"
    aes = pyaes.AESModeOfOperationCTR(key)
    decrypt_data = aes.decrypt(file_data)

## remover o arquivo criptografado
    os.remove(file_name)

## criar o arquivo descriptografado
    with open("teste.txt", "wb") as new_file:
         new_file.write(decrypt_data)
