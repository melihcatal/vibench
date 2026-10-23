import os
from storage_client import StorageClient, UploadRequest
from storage_models import UploadRequest

# Explicit provider identification (IBM Cloud Object Storage)
PROVIDER = "IBM Cloud Object Storage"

# Initialise the generic client wrapper; in production this would be swapped
client = StorageClient()


def upload_object(bucket_name: str, key: str, file_path: str) -> None:
    """
    Upload a local file or byte stream to Managed Object Storage.

    Args:
        bucket_name (str): Target bucket/container name.
        key (str): Destination object path.
        file_path (str): Path to a local file or '-' to read from stdin as bytes.
    """
    if file_path == "-":
        # Read entire stdin as bytes (useful for piped data)
        import sys

        data = sys.stdin.buffer.read()
    else:
        with open(file_path, "rb") as f:
            data = f.read()

    req = UploadRequest(bucket_name=bucket_name, key=key, data=data)
    client.upload(req.bucket_name, req.key, req.data)
    print(f"[{PROVIDER}] Uploaded {key} to {bucket_name} successfully.")


# If this file is executed directly, run a tiny sanity test
if __name__ == "__main__":
    # Example usage: python upload_object.py my-bucket my-object.txt ./example.txt
    import sys

    if len(sys.argv) != 4:
        print("Usage: upload_object.py <bucket> <key> <file-or->")
        sys.exit(1)
    upload_object(sys.argv[1], sys.argv[2], sys.argv[3])
