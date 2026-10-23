def load_document(file_path: str) -> bytes:
    """Load a document file as bytes."""
    with open(file_path, 'rb') as f:
        return f.read()
