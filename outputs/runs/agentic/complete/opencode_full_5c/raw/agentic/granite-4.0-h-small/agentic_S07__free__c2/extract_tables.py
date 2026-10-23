# [SAME-SCENARIO] extract_tables.py
"""Extract table cells and row structure from a document image using a table extraction provider."""

from document_client import TableClient
from document_models import TableResponse


def extract_tables(image_path: str) -> list[dict]:
    """Extract tables from the given image file.

    Args:
        image_path: Path to a local scanned image file.

    Returns:
        A list of table definitions containing cells and row/col information.
    """
    client = (
        TableClient()
    )  # concrete provider (e.g., AWS Textract Tables, Google Document AI Tables)
    response: TableResponse = client.extract_tables(image_path)
    return response.tables
