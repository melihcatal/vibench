import base64


def plaintext_to_bytes(plaintext: str) -> bytes:
    return plaintext.encode("utf-8")


def encode_ciphertext(ciphertext_bytes: bytes) -> str:
    return base64.b64encode(ciphertext_bytes).decode("utf-8")


def decode_ciphertext(encoded_ciphertext: str) -> bytes:
    return base64.b64decode(encoded_ciphertext)
