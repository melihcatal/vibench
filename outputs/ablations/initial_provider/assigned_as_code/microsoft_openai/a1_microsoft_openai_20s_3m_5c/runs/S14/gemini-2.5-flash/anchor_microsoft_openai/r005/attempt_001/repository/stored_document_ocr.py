from google.cloud import vision
from google.cloud import storage
import os

def stored_document_ocr(gcs_uri: str) -> str:
    """
    Performs OCR on a document stored in Google Cloud Storage using Google Cloud Vision AI.
    The GCS URI should be in the format gs://bucket_name/object_name.
    """
    client = vision.ImageAnnotatorClient()

    # The Vision API can directly process GCS URIs.
    image = vision.Image(source=vision.ImageSource(image_uri=gcs_uri))

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    return document.text
