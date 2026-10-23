from google.cloud import vision

from storage_client import get_blob
from storage_models import normalize_object_name


def stored_document_ocr(payload, config=None):
    blob, _ = get_blob(normalize_object_name(payload), config)
    client = vision.ImageAnnotatorClient()
    image = vision.Image(source=vision.ImageSource(gcs_image_uri=f"gs://{blob.bucket.name}/{blob.name}"))
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text if response.full_text_annotation else ""
    return {"object_name": payload["object_name"], "text": text}
