# [SAME-SCENARIO] extract_tables.py

import os
import json
from document_client import DocumentClient


def extract_tables_from_image(image_path: str) -> list:
    """Extract tables and cell structure from a scanned document image using a concrete OCR/table provider.

    Args:
        image_path: Local path to the scanned document image file.

    Returns:
        List of table dictionaries, each containing rows and cell data.
    """
    # Use Mindee Invoice OCR as the concrete provider (replace with any other provider from the list)
    client = DocumentClient(service="mindee_invoice")
    response = client.ocr(image_path=image_path)
    # Mindee table extraction returns under "fields" with "table" key
    tables = response.get("fields", {}).get("table", [])
    return tables


def main():
    image_file = "sample_invoice.jpg"
    tables = extract_tables_from_image(image_file)
    print("Extracted Tables:")
    print(json.dumps(tables, indent=2))


if __name__ == "__main__":
    main()
