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


def extract_text(image_path: str) -> str:
    """Extract plain text from a scanned document image using Alibaba Cloud OCR.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Extracted plain text.
    """
    # Read image in binary mode
    with open(image_path, "rb") as f:
        image_data = f.read()
    # Call the OCR service
    response = client.ocr_general(data=image_data)
    # Response format may vary; assume JSON with 'data' field containing 'text'
    if "data" in response and "text" in response["data"]:
        return response["data"]["text"]
    raise ValueError("OCR failed or returned unexpected format")
