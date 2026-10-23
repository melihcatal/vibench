# [SAME-SCENARIO] extract_text.py

import os
import json
from document_client import DocumentClient


def extract_text_from_image(image_path: str) -> str:
    """Extract plain text from a scanned document image using a concrete OCR provider.

    Args:
        image_path: Local path to the scanned document image file.

    Returns:
        Extracted plain text string.
    """
    # Use Mindee Document OCR as the concrete provider (replace with any other provider from the list)
    client = DocumentClient(service="mindee")
    response = client.ocr(image_path=image_path)
    # Normalize response to plain text (Mindee returns JSON with "fields" and "text")
    result = response.get("text", "")
    return result


def main():
    image_file = "sample_document.jpg"
    text = extract_text_from_image(image_file)
    print("Extracted Text:")
    print(text)


if __name__ == "__main__":
    main()
