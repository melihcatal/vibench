import os
from typing import BinaryIO

def load_document_bytes(document_path: str) -> bytes:
    with open(document_path, 'rb') as f:
        return f.read()

def detect_mime_type(document_path: str) -> str:
    ext = os.path.splitext(document_path)[1].lower()
    if ext == '.pdf':
        return 'application/pdf'
    elif ext in ['.jpg', '.jpeg']:
        return 'image/jpeg'
    elif ext == '.png':
        return 'image/png'
    else:
        raise ValueError(f"Unsupported file type: {ext}")