import os
from storage_client import get_blob_service_client

def upload_object(container_name: str, blob_name: str, data: bytes):
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(data, overwrite=True)
    return {"message": f"Object \'{blob_name}\' uploaded to container \'{container_name}\' successfully."}
