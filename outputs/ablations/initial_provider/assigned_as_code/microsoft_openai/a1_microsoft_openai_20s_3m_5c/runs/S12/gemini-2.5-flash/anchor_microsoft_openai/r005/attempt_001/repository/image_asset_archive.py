from google.cloud import storage
from vision_client import get_storage_client
from vision_models import ArchiveRequest

def image_asset_archive(payload: ArchiveRequest, config: dict = None) -> dict:
    client = get_storage_client()
    bucket = client.bucket(payload.bucket_name)
    blob = bucket.blob(payload.destination_blob_name)

    blob.upload_from_string(payload.data)

    return {"message": f"File {payload.destination_blob_name} uploaded to {payload.bucket_name}."}
