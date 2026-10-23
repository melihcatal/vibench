# stored_document_ocr.py
# [LATER-STEP] Runs OCR on a stored document object using a managed AI service

import json
from google.cloud import storage, vision
from storage_client import ManagedStorageClient
from storage_models import ObjectMetadataResponse

# Example: use the Google Cloud Vision API for OCR
# The OCR engine is abstracted behind the provider‑specific client (vision.ImageAnnotatorClient)


def ocr_stored_document(bucket_name: str, blob_name: str) -> json:
    """Extract text from a scanned document stored as an object.

    Args:
        bucket_name (str): Bucket containing the document.
        blob_name (str): Object/key of the document (e.g., PDF, image).

    Returns:
        JSON string: Serialized OCR response from the vision service.
    """
    client = ManagedStorageClient().get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Download the raw bytes of the document (streaming for large files)
    doc_bytes = blob.download_as_bytes()

    # Initialize Vision API client (OCR service)
    vision_client = vision.ImageAnnotatorClient(credentials=client._credentials)

    # Prepare image annotation request
    image = vision.Image(content=doc_bytes)
    features = [vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    # Execute OCR and return JSON representation
    response = vision_client.annotate_image(request)
    return json.dumps(response.to_dict(), indent=2)
