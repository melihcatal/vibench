import os
import io
from google.cloud import storage
from google.cloud import vision


def stored_document_ocr(object_name, config=None):
    client = storage.Client(project=config["project_id"])
    blob = client.bucket(config["bucket"]).blob(object_name)
    image = vision.Image(content=blob.download_as_string())
    client = vision.ImageAnnotatorClient()
    response = client.document_text_detection(image=image)
    texts = response.full_text_annotation.text
    return {"text": texts}