# [SAME-SCENARIO] extract_text.py

import os
from document_client import DocumentOcrClient

def extract_text_from_image(image_path: str) -> str:
    """Extract plain text from a scanned document image using a cloud OCR service.
    
    This implementation uses Amazon Textract (boto3) for OCR.
    Environment variables required:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_REGION
    """
    client = DocumentOcrClient(service=\"textract\")
    response = client.detect_document_text(image_path)
    # Textract returns a list of blocks; we filter for lines and words.
    lines = []
    for item in response.get(\"Blocks\", []):
        if item.get(\"BlockType\") == \"LINE\":
            lines.append(item.get(\"Text\", \"\").strip())
    return \"\
\".join(lines)
