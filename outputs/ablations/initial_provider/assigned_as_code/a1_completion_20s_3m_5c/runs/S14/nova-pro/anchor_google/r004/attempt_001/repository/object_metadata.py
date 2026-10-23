from google.cloud import storage
from storage_client import get_storage_client


def object_metadata(payload):
    client = get_storage_client()
    blob = client.bucket(payload["bucket"]).blob(payload["object_name"])
    metadata = blob.metadata
    return {"metadata": metadata}