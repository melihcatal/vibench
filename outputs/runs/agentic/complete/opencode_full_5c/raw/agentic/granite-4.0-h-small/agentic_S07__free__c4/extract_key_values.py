import json
from document_client import DocumentClient


def extract_key_values(form_path: str) -> dict:
    """Extract key-value pairs from a form-like document using the Azure Form Recognizer provider.

    Args:
        form_path: Local path to the form image or PDF.
    Returns:
        Dictionary mapping extracted field names to their values.
    """
    client = DocumentClient(service="azure_form_recognizer")
    with open(form_path, "rb") as doc_file:
        kv_pairs = client.extract_key_values(image_bytes=doc_file.read())
    # Normalize to a plain dict (removing any provider-specific wrappers).
    return {field["key"]: field["value"] for field in kv_pairs}
