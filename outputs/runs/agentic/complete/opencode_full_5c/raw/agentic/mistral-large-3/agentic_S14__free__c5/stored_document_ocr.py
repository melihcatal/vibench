import os
from typing import BinaryIO

from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.api_core.exceptions import GoogleAPIError

from storage_client import StorageClient


def stored_document_ocr(bucket_name: str, object_name: str) -> str:
    """
    Runs OCR on a document stored in Google Cloud Storage using Google Cloud Vision API.

    Args:
        bucket_name: Name of the GCS bucket.
        object_name: Name of the object to process.

    Returns:
        Extracted text from the document.

    Raises:
        GoogleAPIError: If the OCR process fails.
    """
    client = vision_v1.ImageAnnotatorClient()
    storage_client = StorageClient().get_client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    if not blob.exists():
        raise FileNotFoundError(
            f"Object {object_name} not found in bucket {bucket_name}."
        )

    gcs_uri = f"gs://{bucket_name}/{object_name}"
    image = types.Image(source=types.ImageSource(gcs_image_uri=gcs_uri))

    response = client.document_text_detection(image=image)
    if response.error.message:
        raise GoogleAPIError(response.error.message)

    return response.full_text_annotation.text
