from aeclient import AEClient
import os
from typing import Tuple
from cryptography.fernet import Fernet

# AEADClient ajoute une vérification du nick dans le message pour lier le contenu à l’émetteur
class AEADClient(AEClient):
    def encrypt_message(self, password: str, message: str) -> Tuple[bytes, bytes]:
        salt = os.urandom(16)
        key = self.derive_key_from_password(password, salt)
        fernet = Fernet(key)
        message_with_nick = f"{self._nick}:{message}"
        encrypted = fernet.encrypt(message_with_nick.encode())
        return encrypted, salt

    def decrypt_message(self, password: str, encrypted_message: bytes, salt: bytes, nick: str) -> str:
        key = self.derive_key_from_password(password, salt)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_message).decode()
        expected_prefix = f"{nick}:"
        if not decrypted.startswith(expected_prefix):
            raise ValueError("Nick mismatch: Message integrity compromised")
        return decrypted[len(expected_prefix):]
