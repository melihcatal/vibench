from google.cloud import vision

from storage_client import get_blob_client


def stored_document_ocr(payload, config=None):
    config = config or {}
    blob = get_blob_client(config, payload["object_name"])
    content = blob.download_as_bytes()
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    return {"text": response.full_text_annotation.text if response.full_text_annotation.text else ""}
