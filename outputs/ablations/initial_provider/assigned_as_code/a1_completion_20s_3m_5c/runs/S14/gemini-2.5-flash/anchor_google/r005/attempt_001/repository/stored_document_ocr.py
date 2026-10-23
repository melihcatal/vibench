from google.cloud import vision
from storage_client import get_storage_client

def run_ocr_on_stored_document(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    bucket_name = config.get("bucket")
    object_name = payload.get("object_name")

    if not bucket_name or not object_name:
        raise ValueError("Bucket name and object name must be provided.")

    image = vision.Image({"source": {"image_uri": f"gs://{bucket_name}/{object_name}"}})
    response = client.document_text_detection(image=image)
    
    full_text = response.full_text_annotation.text
    return {"text": full_text}
