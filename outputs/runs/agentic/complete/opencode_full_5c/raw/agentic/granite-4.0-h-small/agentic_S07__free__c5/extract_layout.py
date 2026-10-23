import os
import requests

# -------------------------------------------------
# SAME-SCENARIO: extract_layout.py
# Extracts blocks, lines, tables, and layout elements from a document using AWS Textract
# -------------------------------------------------

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_Textract_URL = f"https://{'textract'}.{AWS_REGION}.amazonaws.com"


def extract_layout_from_image(image_path: str) -> dict:
    """Calls Textract to get layout blocks (text, tables, form fields) from a scanned image.

    Args:
        image_path: Path to the scanned document image (PNG/JPEG).

    Returns:
        Dict containing layout information with keys like 'Blocks'.
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    payload = {"Document": {"Bytes": image_bytes}, "FeatureTypes": ["FORMS", "TABLES"]}
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "Textract.AnalyzeDocument",
        "X-Amz-Client-Request-Token": os.getenv("AWS_REQUEST_ID", "").strip(),
    }
    response = requests.post(
        f"{AWS_Textract_URL}/AnalyzeDocument", json=payload, headers=headers, timeout=30
    )
    response.raise_for_status()
    result = response.json()
    return result
