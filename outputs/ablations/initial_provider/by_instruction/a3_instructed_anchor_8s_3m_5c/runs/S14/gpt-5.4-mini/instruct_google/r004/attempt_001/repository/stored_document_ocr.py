from google.cloud import storage
from google.cloud import vision

from storage_client import get_bucket
from storage_models import DocumentInsight, normalize_object_name


def stored_document_ocr(bucket_name: str, object_name: str) -> dict:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(normalize_object_name(object_name))
    image = vision.Image(source=vision.ImageSource(image_uri=f"gs://{bucket_name}/{blob.name}"))
    client = vision.ImageAnnotatorClient()
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text if response.full_text_annotation else None
    return DocumentInsight(bucket=bucket_name, name=blob.name, text=text).to_dict()
