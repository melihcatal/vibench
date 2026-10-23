import os
from typing import Dict, List, Optional

from document_client import get_document_client
from document_models import TextractResponse, TextractBlock, normalize_textract_response


def extract_text(image_path: str, language_code: Optional[str] = None) -> str:
    """
    Extracts plain text from a scanned document image using Amazon Textract.
    """
    client = get_document_client("textract")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    response = client.detect_document_text(Document={"Bytes": image_bytes})
    normalized_response = normalize_textract_response(response)
    return normalized_response.get("text", "")
