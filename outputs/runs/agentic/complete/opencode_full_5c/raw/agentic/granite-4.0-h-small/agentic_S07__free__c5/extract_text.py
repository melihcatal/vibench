import os
import requests

# -------------------------------------------------
# SAME-SCENARIO: extract_text.py
# Extracts plain text from a scanned document image using AWS Textract
# -------------------------------------------------

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_Textract_URL = f"https://{'textract'}.{AWS_REGION}.amazonaws.com"


def extract_text_from_image(image_path: str) -> str:
    """Calls Textract to get plain text from a scanned image.

    Args:
        image_path: Path to the scanned document image (PNG/JPEG).

    Returns:
        Plain text extracted from the document.
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    payload = {"Document": {"Bytes": image_bytes}}
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
    # Textract returns text in the "Blocks" field; we extract the text from them
    text = "".join(
        block["Text"]
        for block in result.get("Blocks", [])
        if block.get("BlockType") == "LINE"
    )
    return text
