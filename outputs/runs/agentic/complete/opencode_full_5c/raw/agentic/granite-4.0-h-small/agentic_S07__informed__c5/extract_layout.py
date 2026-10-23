# [SAME-SCENARIO] extract_layout.py

import os
import json
from document_client import DocumentClient


def extract_layout_from_image(image_path: str) -> dict:
    """Extract layout elements (blocks, lines, tables) from a scanned document image using a concrete OCR/layout provider.

    Args:
        image_path: Local path to the scanned document image file.

    Returns:
        Dictionary representing the layout hierarchy (blocks -> lines -> text/tables).
    """
    # Use Azure Document Intelligence as the concrete provider (replace with any other provider from the list)
    client = DocumentClient(service="azure_document_intelligence")
    response = client.analyze_layout(image_path=image_path)
    # Azure returns a JSON with "readResults" containing layout information
    layout = response.get("readResults", [])
    return layout


def main():
    image_file = "sample_document.jpg"
    layout = extract_layout_from_image(image_file)
    print("Extracted Layout:")
    print(json.dumps(layout, indent=2))


if __name__ == "__main__":
    main()
