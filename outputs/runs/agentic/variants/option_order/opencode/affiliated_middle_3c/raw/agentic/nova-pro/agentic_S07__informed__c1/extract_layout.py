import os
from alibabacloud_ocr_api import OcrClient


client = DocumentClient(
    os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
    os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
)


def extract_layout(image_path):
    response = client.extract_layout(image_path)
    return DocumentResponse(response).normalize()
