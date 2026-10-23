import os
from typing import Dict, List

from document_client import get_document_client
from document_models import TextractResponse, normalize_textract_response


def extract_tables(image_path: str) -> List[Dict]:
    """
    Extracts table cells and row structure from a document using Amazon Textract.
    """
    client = get_document_client("textract")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )
    normalized_response = normalize_textract_response(response)
    return normalized_response.get("tables", [])
