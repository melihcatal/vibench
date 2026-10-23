import os

# IBM Cloud Object Storage example (can be swapped for other providers)

# Configuration values expected in the environment
ENDPOINT = os.getenv("IBM_COS_ENDPOINT")
API_KEY = os.getenv("IBM_COS_APIKEY")


# Simple client wrapper that can be extended for other services
class StorageClient:
    """High‑level wrapper around the managed object storage SDK.
    Currently implements the IBM Cloud Object Storage SDK (ibm-cos-sdk) but the
    interface is provider‑agnostic; other providers can subclass and override.
    """

    def __init__(self):
        # The underlying SDK client would be instantiated here.
        # For demonstration we keep the raw credentials.
        self.endpoint = ENDPOINT
        self.api_key = API_KEY
        # placeholder for real SDK client
        self._client = None

    def upload(self, bucket_name, key, data: bytes):
        """Upload a byte stream or file to the bucket/key.
        Args:
            bucket_name (str): Target bucket.
            key (str): Object path.
            data (bytes): Content to store.
        """
        # Placeholder – real implementation would use the SDK ‘put_object’ call.
        print(f"[IBM COS] Uploading to {bucket_name}/{key} ({len(data)} bytes)")

    def get_presigned_url(self, bucket_name, key, expires_in_seconds=3600):
        """Create a time‑limited signed download URL.
        Args:
            bucket_name (str): Target bucket.
            key (str): Object path.
            expires_in_seconds (int): URL validity period.
        Returns:
            str: Signed URL.
        """
        # Placeholder – real implementation uses SDK’s generate_presigned_url.
        print(
            f"[IBM COS] Generating signed URL for {bucket_name}/{key} (expires in {expires_in_seconds}s)"
        )
        return f"https://example.com/presigned/{bucket_name}/{key}"

    def get_metadata(self, bucket_name, key):
        """Retrieve object metadata / HEAD information.
        Args:
            bucket_name (str): Target bucket.
            key (str): Object path.
        Returns:
            dict: Metadata returned by the provider.
        """
        # Placeholder implementation.
        print(f"[IBM COS] Fetching metadata for {bucket_name}/{key}")
        return {"size": "unknown", "last_modified": "N/A"}

    def list_prefix(self, bucket_name, prefix="", delimiter="/"):
        """List objects under a given prefix.
        Args:
            bucket_name (str): Target bucket.
            prefix (str): Prefix to filter objects (empty string lists everything).
            delimiter (str): Character used to delimit object names.
        Returns:
            list: Object keys that match the prefix.
        """
        # Placeholder implementation.
        print(f"[IBM COS] Listing objects under {bucket_name} with prefix '{prefix}'")
        return ["obj1.txt", "obj2.txt"]


# Simple factory (swap in other providers by changing the class)
def get_storage_client():
    return StorageClient()
