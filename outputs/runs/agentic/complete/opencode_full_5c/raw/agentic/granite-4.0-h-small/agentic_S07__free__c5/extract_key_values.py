import os
import requests

# -------------------------------------------------
# SAME-SCENARIO: extract_key_values.py
# Extracts key-value pairs from a form-like document using AWS Textract
# -------------------------------------------------

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_Textract_URL = f"https://{'textract'}.{AWS_REGION}.amazonaws.com"


def extract_key_values_from_image(image_path: str) -> dict:
    """Calls Textract to extract form fields (key-value pairs) from a scanned image.

    Args:
        image_path: Path to the scanned document image (PNG/JPEG).

    Returns:
        Dict mapping key text to value text extracted from the form.
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    payload = {"Document": {"Bytes": image_bytes}, "FeatureTypes": ["FORMS"]}
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
    kv_map = {}
    for block in result.get("Blocks", []):
        if block.get("BlockType") == "KEY_VALUE_SET":
            key = next(
                (
                    b["Text"]
                    for b in block.get("Relationships", [])
                    if b["Type"] == "KEY"
                ),
                None,
            )
            value = next(
                (
                    b["Text"]
                    for b in block.get("Relationships", [])
                    if b["Type"] == "VALUE"
                ),
                None,
            )
            if key and value:
                kv_map[key] = value
    return kv_map
