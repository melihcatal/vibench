from azure.ai.vision import VisionClient

from storage_client import get_blob_client


def stored_document_ocr(bucket: str, object_name: str):
    blob_url = get_blob_client(bucket, object_name).url
    client = VisionClient(endpoint="https://eastus.api.cognitive.microsoft.com", credential=None)
    return client.analyze(blob_url, model_id="ocr")
