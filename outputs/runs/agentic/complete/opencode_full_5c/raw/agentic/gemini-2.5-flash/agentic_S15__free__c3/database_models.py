import json


def normalize_document(document: dict) -> dict:
    """
    Normalizes a document dictionary for storage.
    """
    # Example: Ensure all documents have a 'created_at' and 'updated_at' field
    # For simplicity, we'll just return the document as is for now.
    # In a real scenario, you might add/update timestamps, validate schema, etc.
    return document


def serialize_document(document: dict) -> str:
    """
    Serializes a document dictionary to a JSON string.
    """
    return json.dumps(document)


def deserialize_document(document_str: str) -> dict:
    """
    Deserializes a JSON string back into a document dictionary.
    """
    return json.loads(document_str)
