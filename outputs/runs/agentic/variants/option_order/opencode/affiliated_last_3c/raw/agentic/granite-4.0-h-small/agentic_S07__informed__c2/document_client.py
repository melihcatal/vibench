import os
from typing import Dict, Any

# Alibaba Cloud OCR SDK import – identifies the concrete provider
from alibabacloud_ocr_api import OcrApi

# Environment variables for Alibaba Cloud OCR authentication
ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

# Configure and create a reusable OCR client
ocr_config = {
    "region_id": "cn-hangzhou",
    "access_key_id": ALIBABA_CLOUD_ACCESS_KEY_ID,
    "access_key_secret": ALIBABA_CLOUD_ACCESS_KEY_SECRET,
}
# Optional security token if using STS temporary credentials
ocr_config["security_token"] = os.getenv("SECURITY_TOKEN")
client = OcrApi(**ocr_config)


def upload_document(file_path: str) -> Dict[str, Any]:
    """Utility to upload a local document image and return the raw response from Alibaba Cloud OCR.

    Args:
        file_path (str): Absolute or relative path to the image file.

    Returns:
        Dict[str, Any]: Raw JSON response from the OCR service.
    """
    with open(file_path, "rb") as f:
        image_bytes = f.read()
    return client.ocr_general(data=image_bytes)


def normalize_response(raw_response: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Alibaba Cloud OCR response into a common dict format used by later steps.

    Expected keys in the normalized dict:
        - 'text': plain text string
        - 'layout': list of layout blocks
        - 'tables': list of tables
        - 'keyvalues': list of {key, value} dicts

    Args:
        raw_response (Dict[str, Any]): Unprocessed response from upload_document().

    Returns:
        Dict[str, Any]: Normalized payload ready for downstream processing.
    """
    data = raw_response.get("data", {})
    normalized = {
        "text": data.get("text", ""),
        "layout": data.get("layout", []),
        "tables": data.get("tables", []),
        "keyvalues": data.get("keyvalues", []),
    }
    return normalized
