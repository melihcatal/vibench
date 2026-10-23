from google.cloud import storage
from storage_client import get_storage_client
from google.cloud import vision


def stored_document_ocr(payload):
    client = get_storage_client()
    blob = client.bucket(payload["bucket"]).blob(payload["object_name"])
    content = blob.download_as_bytes()
    image = vision.Image(content=content)
    client = vision.ImageAnnotatorClient()
    response = client.document_text_detection(image=image)
    text = response.full_text_annotation.text
    return {"text": text}