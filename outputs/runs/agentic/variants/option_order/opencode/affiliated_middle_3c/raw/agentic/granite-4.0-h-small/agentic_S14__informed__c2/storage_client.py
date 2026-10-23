import os
from b2sdk.v2 import B2Api, InMemoryAccountInfo


class ManagedClient:
    """Thin wrapper around Backblaze B2 SDK providing high‑level helpers.

    The client is configured once with credentials from the environment:
    - B2_ACCOUNT_ID
    - B2_APPLICATION_KEY
    All public methods accept bucket and object identifiers that match the
    managed object storage terminology used throughout the scenario.
    """

    def __init__(self):
        account_info = InMemoryAccountInfo()
        api = B2Api(account_info)
        api.authorize_account(
            "production", os.getenv("B2_ACCOUNT_ID"), os.getenv("B2_APPLICATION_KEY")
        )
        self.api = api

    def upload_file(
        self, bucket_name: str, object_key: str, file_path: str | os.PathLike
    ):
        bucket = self.api.get_bucket_by_name(bucket_name)
        bucket.upload_local_file(file_path, object_key)

    def upload_bytes(self, bucket_name: str, object_key: str, data: bytes):
        bucket = self.api.get_bucket_by_name(bucket_name)
        bucket.upload_bytes(data, object_key)

    def head_object(self, bucket_name: str, object_key: str) -> dict:
        bucket = self.api.get_bucket_by_name(bucket_name)
        return bucket.get_file_metadata(object_key)

    def list_objects(self, bucket_name: str, prefix: str = "", max_results: int = 1000):
        bucket = self.api.get_bucket_by_name(bucket_name)
        # list_objects_v2 provides pagination and respect for prefixes
        paginator = self.api.list_objects_v2(
            bucket_name, prefix=prefix, max_results=max_results
        )
        return [entry for entry in paginator]
