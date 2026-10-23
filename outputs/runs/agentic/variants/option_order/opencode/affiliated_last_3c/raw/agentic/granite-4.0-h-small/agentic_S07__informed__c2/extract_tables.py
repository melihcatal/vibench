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


def extract_tables(image_path: str) -> list:
    """Extract table cells and row structure from a document image using Alibaba Cloud OCR.

    Args:
        image_path (str): Path to the image file.

    Returns:
        list: A list of tables, each containing rows and cells.
    """
    with open(image_path, "rb") as f:
        image_data = f.read()
    response = client.ocr_general(data=image_data)
    # Assuming response contains a 'tables' field with rows and cells
    if "data" in response and "tables" in response["data"]:
        return response["data"]["tables"]
    raise ValueError("Table extraction failed or returned unexpected format")
