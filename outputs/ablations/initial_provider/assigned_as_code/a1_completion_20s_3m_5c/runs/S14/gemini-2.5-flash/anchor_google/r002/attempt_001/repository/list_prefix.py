from typing import Optional

from storage_client import get_storage_client, get_bucket_name
from storage_models import ListPrefixPayload, StorageConfig

def list_prefix(payload: ListPrefixPayload, config: Optional[StorageConfig] = None) -> dict:
    client = get_storage_client(config)
    bucket_name = get_bucket_name(config)
    bucket = client.bucket(bucket_name)

    blobs = client.list_blobs(bucket, prefix=payload.prefix, delimiter=payload.delimiter)
    
    object_names = []
    for blob in blobs:
        object_names.append(blob.name)
    
    prefixes = []
    if payload.delimiter:
        for prefix in blobs.prefixes:
            prefixes.append(prefix)

    return {"object_names": object_names, "prefixes": prefixes}
