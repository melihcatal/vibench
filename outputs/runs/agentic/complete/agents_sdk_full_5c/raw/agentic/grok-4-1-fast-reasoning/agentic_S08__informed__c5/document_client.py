import base64
import os

def document_bytes_from_path(path: str) -> bytes:
    """Load document bytes from file path."""
    with open(path, 'rb') as f:
        return f.read()

def document_to_base64(document_input) -> str:
    """Convert document path or bytes to base64 string."""
    if isinstance(document_input, str):
        document_bytes = document_bytes_from_path(document_input)
    else:
        document_bytes = document_input
    return base64.b64encode(document_bytes).decode('utf-8')