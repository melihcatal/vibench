from typing import Optional

from storage_client import get_storage_client, get_bucket_name
from storage_models import ObjectMetadataPayload, StorageConfig

def object_metadata(payload: ObjectMetadataPayload, config: Optional[StorageConfig] = None) -> dict:
    client = get_storage_client(config)
    bucket_name = get_bucket_name(config)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(payload.object_name)
    
    blob.reload()
    metadata = {
        "name": blob.name,
        "bucket": blob.bucket.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "crc32c": blob.crc32c,
        "etag": blob.etag,
        "md5_hash": blob.md5_hash,
        "generation": blob.generation,
        "metageneration": blob.metageneration,
        "time_created": blob.time_created.isoformat() if blob.time_created else None,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "storage_class": blob.storage_class,
        "kms_key_name": blob.kms_key_name,
        "cache_control": blob.cache_control,
        "component_count": blob.component_count,
        "content_disposition": blob.content_disposition,
        "content_encoding": blob.content_encoding,
        "content_language": blob.content_language,
        "custom_time": blob.custom_time.isoformat() if blob.custom_time else None,
        "event_based_hold": blob.event_based_hold,
        "retention_expiration_time": blob.retention_expiration_time.isoformat() if blob.retention_expiration_time else None,
        "temporary_hold": blob.temporary_hold,
        "user_metadata": blob.metadata, # User-defined metadata
    }
    
    return {"metadata": metadata}
