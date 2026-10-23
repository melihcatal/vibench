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


def extract_key_values(form_path: str) -> dict:
    """Extract key-value pairs from a form-like document image using Alibaba Cloud OCR.

    Args:
        form_path (str): Path to the image file.

    Returns:
        dict: Mapping of extracted keys to values.
    """
    with open(form_path, "rb") as f:
        image_data = f.read()
    response = client.ocr_general(data=image_data)
    # Assuming OCR returns a 'keyvalues' field as a list of {key, value} objects
    if "data" in response and "keyvalues" in response["data"]:
        kv_pairs = response["data"]["keyvalues"]
        return {item["key"]: item["value"] for item in kv_pairs}
    raise ValueError("Key-value extraction failed or returned unexpected format")
