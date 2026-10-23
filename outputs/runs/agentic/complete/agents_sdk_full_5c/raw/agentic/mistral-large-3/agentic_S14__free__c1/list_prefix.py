from google.cloud import storage
from storage_client import get_storage_client, get_bucket_name
from storage_models import ListPrefixResponse


def list_prefix(prefix: str, delimiter: str = "/") -> ListPrefixResponse:
    """
    List objects and prefixes under a given prefix in Google Cloud Storage.
    
    Args:
        prefix: Prefix to filter objects.
        delimiter: Delimiter to simulate directory-like behavior.
        
    Returns:
        ListPrefixResponse containing objects and prefixes.
    """
    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    objects = [blob.name for blob in blobs]
    prefixes = blobs.prefixes
    
    return ListPrefixResponse(
        objects=objects,
        prefixes=prefixes
    )