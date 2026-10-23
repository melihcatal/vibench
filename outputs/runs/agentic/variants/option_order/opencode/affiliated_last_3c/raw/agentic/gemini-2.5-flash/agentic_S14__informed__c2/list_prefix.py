from typing import List, Dict
from storage_client import StorageClient


def list_objects_with_prefix(
    bucket_name: str, prefix: str = "", delimiter: str | None = None
) -> List[Dict]:
    """Lists objects in a Google Cloud Storage bucket with a given prefix.

    Args:
        bucket_name (str): The name of the Google Cloud Storage bucket.
        prefix (str): The prefix to filter objects by. Only objects whose names begin with this prefix will be returned.
        delimiter (str | None): A delimiter character. Objects whose names contain the delimiter after the prefix
                                  will be grouped. Useful for simulating folders.

    Returns:
        List[Dict]: A list of dictionaries, each representing an object (or common prefix if delimiter is used).
    """
    storage_client = StorageClient.get_storage_client()
    bucket = storage_client.bucket(bucket_name)

    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    object_list = []
    print(f"Blobs in bucket {bucket_name} with prefix {prefix}:")
    for blob in blobs:
        object_list.append(
            {"name": blob.name, "size": blob.size, "content_type": blob.content_type}
        )
        print(f"  {blob.name} ({blob.size} bytes, {blob.content_type})")

    if delimiter:
        print("Prefixes:")
        for prefix_item in blobs.prefixes:
            object_list.append({"prefix": prefix_item})
            print(f"  {prefix_item}")

    return object_list
