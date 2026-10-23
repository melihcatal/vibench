import os
from storage_client import StorageClient, ListObjectsResult
from storage_models import ListObjectsResult

# Explicit provider identification (IBM Cloud Object Storage)
PROVIDER = "IBM Cloud Object Storage"

# Initialise the generic client wrapper
client = StorageClient()


def list_objects_prefix(
    bucket_name: str, prefix: str = "", delimiter: str = "/"
) -> ListObjectsResult:
    """
    List objects stored under a given prefix.

    Args:
        bucket_name (str): Bucket name.
        prefix (str): Prefix to filter objects (empty string lists all objects).
        delimiter (str): Character used to group keys (e.g., '/' for folder emulation).
    Returns:
        ListObjectsResult: Normalized list result.
    """
    result = client.list_prefix(bucket_name, prefix, delimiter)
    # Normalise the provider‑specific list into our model
    normalized = ListObjectsResult(
        bucket=bucket_name,
        prefix=prefix,
        delimiter=delimiter,
        contents=result,  # assume the placeholder client already returns a list of keys
    )
    print(
        f"[{PROVIDER}] List under bucket '{bucket_name}' prefix '{prefix}': {normalized.contents}"
    )
    return normalized


# Simple CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: list_prefix.py <bucket> [prefix] [delimiter]")
        sys.exit(1)
    bucket = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else ""
    delimiter = sys.argv[3] if len(sys.argv) > 3 else "/"
    list_objects_prefix(bucket, prefix, delimiter=delimiter)
