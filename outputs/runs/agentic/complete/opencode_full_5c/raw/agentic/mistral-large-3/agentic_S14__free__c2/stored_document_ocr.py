import os
from typing import BinaryIO

from google.cloud import vision_v1
from google.cloud.vision_v1 import types

from storage_client import StorageClient


def run_ocr_on_stored_document(
    bucket_name: str,
    object_key: str,
) -> str:
    """
    Runs OCR on a stored document in AWS S3 using Google Cloud Vision API.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path of the document in the bucket.

    Returns:
        str: Extracted text from the document.

    Raises:
        Exception: If OCR processing fails.
    """
    storage_client = StorageClient().get_client()
    response = storage_client.get_object(Bucket=bucket_name, Key=object_key)
    document_content = response["Body"].read()

    client = vision_v1.ImageAnnotatorClient(
        credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    image = types.Image(content=document_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return ""
