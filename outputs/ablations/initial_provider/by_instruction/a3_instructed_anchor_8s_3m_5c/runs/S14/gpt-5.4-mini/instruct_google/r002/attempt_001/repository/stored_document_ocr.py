from google.cloud import storage

from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest


def stored_document_ocr(request: ObjectMetadataRequest) -> dict:
    client = get_storage_client()
    blob = client.bucket(request.bucket).blob(request.name)
    text = blob.download_as_text()
    return {"bucket": request.bucket, "name": request.name, "ocr_text": text}
