import os
from typing import BinaryIO


def load_document_bytes(document_path: str) -> bytes:
    with open(document_path, "rb") as f:
        return f.read()
