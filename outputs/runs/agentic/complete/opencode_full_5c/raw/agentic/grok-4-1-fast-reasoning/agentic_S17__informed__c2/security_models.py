import base64
from typing import Union


def normalize_plaintext(text: str) -> bytes:
    return text.encode("utf-8")


def denormalize_ciphertext(ciphertext: bytes) -> str:
    return base64.b64encode(ciphertext).decode("utf-8")


def parse_envelope(envelope: dict) -> dict:
    return envelope
