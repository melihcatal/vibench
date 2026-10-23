import os
import json
from azure.storage.blob import BlobServiceClient


def record_export_archive(snapshot, container_name, blob_name):
    account_url = os.environ["AZURE_STORAGE_ACCOUNT_URL"]
    key = os.environ["AZURE_STORAGE_KEY"]
    client = BlobServiceClient(account_url=account_url, credential=key)
    blob_client = client.get_blob_client(container=container_name, blob=blob_name)
    payload = json.dumps(snapshot).encode("utf-8")
    blob_client.upload_blob(payload, overwrite=True)
    return {"container": container_name, "blob": blob_name}
