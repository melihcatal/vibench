# [SAME-SCENARIO] extract_key_values.py

import os
import json
from document_client import DocumentClient


def extract_key_values_from_image(image_path: str) -> dict:
    """Extract key-value pairs from a form-like document using a concrete OCR/key-value provider.

    Args:
        image_path: Local path to the scanned document image file.

    Returns:
        Dictionary mapping extracted keys to their corresponding values.
    """
    # Use Google Document AI form parsing as the concrete provider (replace with any other provider from the list)
    client = DocumentClient(service="google_document_ai")
    response = client.analyze_form(image_path=image_path)
    # Google returns "document" with "pages" containing "keyValuePairs"
    kv_pairs = {}
    for page in response.get("document", {}).get("pages", []):
        for kv in page.get("keyValuePairs", []):
            key = kv.get("key", {}).get("text", "")
            value = kv.get("value", {}).get("text", "")
            kv_pairs[key] = value
    return kv_pairs


def main():
    form_image = "sample_form.jpg"
    kv_data = extract_key_values_from_image(form_image)
    print("Extracted Key-Value Pairs:")
    print(kv_data)


if __name__ == "__main__":
    main()
