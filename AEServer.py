import logging
import base64
import os
from typing import Tuple
import msgpack

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from pywebio.output import put_text
from names_generator import generate_name
from simple_client import SimpleClient

# Client avec chiffrement/déchiffrement Fernet
class AEClient(SimpleClient):
    def __init__(self, host: str, send_port: int, broadcast_port: int, nick: str, password: str):
        super().__init__(host, send_port, broadcast_port, nick)
        self._password = password
        self._serial_function = msgpack.packb
        self._deserial_function = msgpack.unpackb

    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_message(self, password: str, message: str) -> Tuple[bytes, bytes]:
        salt = os.urandom(16)
        key = self.derive_key_from_password(password, salt)
        f = Fernet(key)
        return f.encrypt(message.encode()), salt

    def decrypt_message(self, password: str, encrypted_message: bytes, salt: bytes, nick: str) -> str:
        key = self.derive_key_from_password(password, salt)
        f = Fernet(key)
        return f.decrypt(encrypted_message).decode()

    def send(self, frame: dict) -> dict:
        return super().send(frame)

    def message(self, message: str):
        encrypted, salt = self.encrypt_message(self._password, message)
        payload = {
            "type": "message",
            "nick": self._nick,
            "message": encrypted,
            "salt": salt,
        }
        self.send(payload)

    def on_recv(self, packet: bytes):
        frame = self._deserial_function(packet)
        if frame["type"] == "message":
            try:
                plaintext = self.decrypt_message(self._password, frame["message"], frame["salt"], frame["nick"])
                put_text(f"{frame['nick']} : {plaintext}", scope='scrollable')
            except Exception:
                self._log.warning("Invalid decryption")
