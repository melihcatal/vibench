import json
from security_client import KeyManagementClient


def sign_or_verify(key_name: str, message: bytes, sign: bool = True) -> bytes:
    """Sign a message or verify a signature using the managed key.

    If sign=True, returns a digital signature for the message.
    If sign=False, returns True/False indicating whether the signature is valid.
    """
    client = KeyManagementClient()
    if sign:
        signature = client.sign(key_name, message)
        return signature
    else:
        # verification: client typically returns bool or raises on failure
        return client.verify(key_name, message, signature=None)
