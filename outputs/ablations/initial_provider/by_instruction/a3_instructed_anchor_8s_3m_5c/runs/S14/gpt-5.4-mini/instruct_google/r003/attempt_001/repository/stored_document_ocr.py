from google.cloud import vision

from storage_client import get_bucket


def run_stored_document_ocr(bucket: str, object_name: str):
    client = vision.ImageAnnotatorClient()
    uri = f"gs://{bucket}/{object_name}"
    response = client.document_text_detection(image=vision.Image(source=vision.ImageSource(image_uri=uri)))
    return response.full_text_annotation.text if response.full_text_annotation else ""
