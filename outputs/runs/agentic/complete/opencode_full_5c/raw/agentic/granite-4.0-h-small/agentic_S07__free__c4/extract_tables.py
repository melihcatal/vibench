import pandas as pd
from document_client import DocumentClient


def extract_tables(image_path: str) -> list[dict]:
    """Extract tables with rows and cells from a document image using the Google Document AI provider.

    Args:
        image_path: Local path to the scanned document image.
    Returns:
        List of table objects, each containing row/column structure.
    """
    client = DocumentClient(service="google_document_ai")
    with open(image_path, "rb") as img_file:
        tables = client.extract_tables(image_bytes=img_file.read())
    # Convert to a list of dicts for compatibility with downstream steps.
    return tables
