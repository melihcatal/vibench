import os

def load_document_image(file_path: str) -> bytes:
    """
    Load a document image from disk as bytes for API calls.
    """
    with open(file_path, 'rb') as f:
        return f.read()
