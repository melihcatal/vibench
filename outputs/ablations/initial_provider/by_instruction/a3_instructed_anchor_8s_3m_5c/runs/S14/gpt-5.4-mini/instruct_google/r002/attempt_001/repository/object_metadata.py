from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest


def object_metadata(request: ObjectMetadataRequest) -> dict:
    client = get_storage_client()
    blob = client.bucket(request.bucket).blob(request.name)
    blob.reload()
    return {
        "bucket": request.bucket,
        "name": request.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "metadata": dict(blob.metadata or {}),
        "updated": blob.updated.isoformat() if blob.updated else None,
        "generation": blob.generation,
        "metageneration": blob.metageneration,
    }
