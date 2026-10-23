from google.cloud import storage
from storage_client import get_storage_client


def list_prefix(payload):
    client = get_storage_client()
    blobs = client.list_blobs(payload["bucket"], prefix=payload["prefix"])
    objects = [blob.name for blob in blobs]
    return {"objects": objects}