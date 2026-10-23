import os
from storage_client import StorageClient, ObjectMetadataResponse
from storage_models import ObjectMetadataResponse

# Explicit provider identification (IBM Cloud Object Storage)
PROVIDER = "IBM Cloud Object Storage"

# Initialise the generic client wrapper
client = StorageClient()


def read_object_metadata(bucket_name: str, key: str) -> ObjectMetadataResponse:
    """
    Retrieve HEAD/metadata information for a stored object.

    Args:
        bucket_name (str): The bucket name.
        key (str): Object path/key.
    Returns:
        ObjectMetadataResponse: Normalized metadata.
    """
    meta = client.get_metadata(bucket_name, key)
    # Normalise the possibly provider‑specific dict to our schema
    normalized = ObjectMetadataResponse(
        bucket=bucket_name,
        key=key,
        size=meta.get("size"),
        last_modified=meta.get("last_modified"),
        etag=meta.get("etag"),
        content_type=meta.get("content_type"),
    )
    print(f"[{PROVIDER}] Metadata for {bucket_name}/{key}: {normalized}")
    return normalized


# Example CLI usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: object_metadata.py <bucket> <key>")
        sys.exit(1)
    read_object_metadata(sys.argv[1], sys.argv[2])
