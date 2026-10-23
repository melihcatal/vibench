import base64
import os
from cryptography.fernet import Fernet


def decrypt_payload(ciphertext: str) -> str:
    key = os.environ.get("FERNET_KEY")
    if not key:
        raise RuntimeError("FERNET_KEY is required")
    fernet = Fernet(key.encode() if isinstance(key, str) else key)
    plaintext = fernet.decrypt(ciphertext.encode())
    return plaintext.decode()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: decrypt_payload.py <ciphertext>")
    print(decrypt_payload(sys.argv[1]))
