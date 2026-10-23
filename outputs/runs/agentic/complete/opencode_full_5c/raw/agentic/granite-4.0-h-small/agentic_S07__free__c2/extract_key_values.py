# [SAME-SCENARIO] extract_key_values.py
"""Extract key-value pairs from a form-like document image using a KV extraction provider."""

from document_client import KVClient
from document_models import KVResponse


def extract_key_values(image_path: str) -> dict:
    """Extract key-value pairs from the given image file.

    Args:
        image_path: Path to a local scanned image file.

    Returns:
        A dictionary mapping extracted keys to their corresponding values.
    """
    client = (
        KVClient()
    )  # concrete provider (e.g., AWS Textract Key-Value, Google Form AI KV)
    response: KVResponse = client.extract_key_values(image_path)
    return response.key_values
