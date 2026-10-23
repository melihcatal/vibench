import os
from storage_client import ManagedClient


def upload_object(
    bucket_name: str,
    object_key: str,
    file_path: str | os.PathLike | None = None,
    data: bytes | None = None,
):
    """Upload a file or byte stream to managed object storage.

    Uses Backblaze B2 Cloud Storage via b2sdk. Credentials are read from
    environment variables B2_ACCOUNT_ID and B2_APPLICATION_KEY.

    Either `file_path` (local file) or `data` (in‑memory bytes) must be provided.
    """
    client = ManagedClient()  # creates B2 client configured for same‑scenario
    if file_path:
        client.upload_file(bucket_name, object_key, file_path)
    elif data:
        client.upload_bytes(bucket_name, object_key, data)
    else:
        raise ValueError("Either file_path or bytes data must be supplied")
