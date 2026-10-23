import os


def load_document(file_path: str) -> bytes:
    """
    Load document bytes from local file path for processing.
    """
    with open(file_path, "rb") as file:
        return file.read()
