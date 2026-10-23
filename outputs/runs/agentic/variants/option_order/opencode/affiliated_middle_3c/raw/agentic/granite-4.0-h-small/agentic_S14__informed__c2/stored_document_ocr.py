import os
from storage_client import ManagedClient
from storage_models import OCRResult, ObjectInfo
from typing import Optional

from alibabacloud_ocr_api import OcrClient, Profile


def ocr_stored_document(
    bucket_name: str, object_key: str, language: str = "en"
) -> OCRResult:
    """Extract text from a document stored as an object using Alibaba Cloud OCR.

    The function reads the object as bytes, sends it to the Alibaba Cloud Document
    OCR API, and returns a simple result.

    Credentials for Alibaba Cloud are read from:
    - ALIBABA_CLOUD_ACCESS_KEY_ID
    - ALIBABA_CLOUD_ACCESS_KEY_SECRET
    """
    client = ManagedClient()  # Backblaze B2 client (unused directly here)
    alibaba_client = OcrClient(
        Profile(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        )
    )

    # Download the object first (as bytes)
    obj = client.head_object(bucket_name, object_key)
    data = client.download_bytes(bucket_name, object_key)  # simplistic downloader

    response = alibaba_client.recognize_document(image=data, language=language)
    # The SDK returns a JSON dict; map to our model
    result = OCRResult(
        text=response["text"],
        language=response.get("language", "en"),
        confidence=response.get("confidence", 0.0),
    )
    return result
