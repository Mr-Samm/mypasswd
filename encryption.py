from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64


class AES256Encryptor:
    def __init__(self, passphrase):
        self.passphrase = passphrase.encode('utf-8')
        self.backend = default_backend()

    def encrypt_text(self, text):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=salt,
            length=32,
            iterations=100000,
            backend=self.backend
        )
        key = kdf.derive(self.passphrase)
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(text.encode('utf-8')) + padder.finalize()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return salt + iv + ciphertext


class AES256Decryptor:
    def __init__(self, passphrase):
        self.passphrase = passphrase.encode('utf-8')
        self.backend = default_backend()

    def decrypt_text(self, ciphertext):
        salt = ciphertext[:16]
        iv = ciphertext[16:32]
        encrypted_data = ciphertext[32:]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=salt,
            length=32,
            iterations=100000,
            backend=self.backend
        )
        key = kdf.derive(self.passphrase)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        return unpadded_data.decode('utf-8')


# decrypt = AES256Decryptor(passphrase="abc@123")
# text = base64.b64decode("g99BsTBlZQHsUjwliCxNNcqddYqgObdAw0POaDLQhkMNtq15qm/I3g8Qdfjdm9Co")
# result = decrypt.decrypt_text(ciphertext=text)
# print(result)
# print(text)
