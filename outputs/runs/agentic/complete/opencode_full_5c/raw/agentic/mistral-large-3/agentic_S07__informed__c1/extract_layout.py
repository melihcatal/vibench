import os
from typing import Dict, List, Optional

from document_client import get_document_client
from document_models import TextractResponse, normalize_textract_response


def extract_layout(image_path: str) -> Dict:
    """
    Extracts layout elements (blocks, lines, tables) from a document using Amazon Textract.
    """
    client = get_document_client("textract")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES", "FORMS", "LAYOUT"]
    )
    return normalize_textract_response(response)
