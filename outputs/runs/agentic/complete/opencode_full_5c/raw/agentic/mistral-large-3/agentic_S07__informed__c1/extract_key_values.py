import os
from typing import Dict, List

from document_client import get_document_client
from document_models import TextractResponse, normalize_textract_response


def extract_key_values(image_path: str) -> List[Dict]:
    """
    Extracts key-value pairs from a form-like document using Amazon Textract.
    """
    client = get_document_client("textract")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )
    normalized_response = normalize_textract_response(response)
    return normalized_response.get("key_values", [])
