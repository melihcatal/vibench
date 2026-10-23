from google.cloud import vision_v1
from google.cloud.vision_v1 import types

from storage_client import get_storage_client, get_bucket_name


def run_ocr_on_stored_document(object_name: str) -> str:
    """
    Run OCR on a document stored in Google Cloud Storage using Google Cloud Vision API.
    
    Args:
        object_name: Name of the object in the bucket.
        
    Returns:
        Extracted text from the document.
    """
    client = vision_v1.ImageAnnotatorClient()
    bucket_name = get_bucket_name()
    gcs_uri = f"gs://{bucket_name}/{object_name}"

    image = types.Image()
    image.source.image_uri = gcs_uri

    response = client.document_text_detection(image=image)
    texts = response.full_text_annotation.text

    return texts