from google.cloud import vision

from storage_client import storage_bucket, load_config, vision_client
from storage_models import normalize_object_name


def stored_document_ocr(payload, config=None):
    config = load_config(config)
    blob = storage_bucket(config).blob(normalize_object_name(payload))
    image = vision.Image(source=vision.ImageSource(image_uri=f"gs://{blob.bucket.name}/{blob.name}"))
    response = vision_client(config).document_text_detection(image=image)
    return {"text": response.full_text_annotation.text if response.full_text_annotation else ""}
