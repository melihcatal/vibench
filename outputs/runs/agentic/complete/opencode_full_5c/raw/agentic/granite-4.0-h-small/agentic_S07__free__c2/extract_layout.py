# [SAME-SCENARIO] extract_layout.py
"""Extract blocks, lines, tables, or other layout elements from a document image using a layout extraction provider."""

from document_client import LayoutClient
from document_models import LayoutResponse


def extract_layout(image_path: str) -> list[dict]:
    """Extract layout blocks from the given image file.

    Args:
        image_path: Path to a local scanned image file.

    Returns:
        A list of layout element dictionaries representing blocks, lines, tables, etc.
    """
    client = (
        LayoutClient()
    )  # concrete provider (e.g., AWS Layout, Azure Form Recognizer)
    response: LayoutResponse = client.extract_layout(image_path)
    return response.elements
