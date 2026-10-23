import os
from alibabacloud_ocr_api import OcrApi

# Alibaba Cloud OCR Authentication
access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
options = {
    "region_id": "cn-hangzhou",
}

options["access_key_id"] = access_key_id
options["access_key_secret"] = access_key_secret
options["security_token"] = os.getenv("SECURITY_TOKEN", None)

client = OcrApi(**options)


def extract_layout(image_path: str) -> dict:
    """Extract blocks, lines, tables, and layout elements from a document image using Alibaba Cloud OCR.

    Args:
        image_path (str): Path to the image file.

    Returns:
        dict: Parsed layout elements.
    """
    with open(image_path, "rb") as f:
        image_data = f.read()
    response = client.ocr_general(data=image_data)
    # Assuming the response includes a structured layout field
    if "data" in response and "layout" in response["data"]:
        return response["data"]["layout"]
    raise ValueError("Layout extraction failed or returned unexpected format")
