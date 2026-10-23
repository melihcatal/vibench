from azure.storage.blob import BlobServiceClient
from storage_client import get_blob_service_client
from storage_models import StorageObjectListing
from typing import List

def list_prefix(prefix: str, config: dict) -> List[StorageObjectListing]:
    account_url = config['account_url']
    container_name = config['container']

    client: BlobServiceClient = get_blob_service_client(account_url)
    container_client = client.get_container_client(container=container_name)

    blob_list = container_client.list_blobs(name_starts_with=prefix)
    
    results = []
    for blob in blob_list:
        results.append(StorageObjectListing(
            object_name=blob.name,
            size=blob.size,
            last_modified_time=blob.last_modified.isoformat(),
            etag=blob.etag
        ))
    return results
