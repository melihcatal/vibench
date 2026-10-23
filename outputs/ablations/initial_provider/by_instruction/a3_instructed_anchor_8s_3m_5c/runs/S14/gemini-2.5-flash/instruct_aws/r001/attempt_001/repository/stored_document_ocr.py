import os
from google.cloud import vision_v1 as vision
from google.cloud.vision_v1 import types

def run_ocr_on_stored_document(gcs_source_uri: str) -> str:
    """Runs OCR on a document stored in Google Cloud Storage using Google Cloud Vision AI.

    Args:
        gcs_source_uri: The Google Cloud Storage URI of the document (e.g., "gs://bucket_name/object_name").

    Returns:
        The extracted text from the document.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/keyfile.json"

    client = vision.ImageAnnotatorClient()

    image = types.Image(source=types.ImageSource(image_uri=gcs_source_uri))

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    return document.text
