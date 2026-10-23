from google.cloud import storage

from storage_client import get_storage_client
from storage_models import UploadRequest, normalize_bytes, normalize_metadata


def upload_object(request: UploadRequest) -> dict:
    client = get_storage_client()
    bucket = client.bucket(request.bucket)
    blob = bucket.blob(request.name)
    blob.metadata = normalize_metadata(request.metadata)
    blob.upload_from_string(normalize_bytes(request.data), content_type=request.content_type)
    return {
        "bucket": request.bucket,
        "name": request.name,
        "generation": blob.generation,
        "metageneration": blob.metageneration,
        "size": blob.size,
    }
