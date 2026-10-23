import os
from storage_client import get_storage_client, get_bucket_name
from typing import Union

def upload_object_to_gcs(object_name: str, data: Union[str, bytes]):
    """Uploads a file or byte stream to the bucket."""
    # The ID of your GCS object
    # object_name = "your-object-name"

    client = get_storage_client()
    bucket_name = get_bucket_name()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    if isinstance(data, str):
        blob.upload_from_string(data)
    else:
        blob.upload_from_string(data, content_type='application/octet-stream')

    print(f"Data uploaded to gs://{bucket_name}/{object_name}.")
    return f"gs://{bucket_name}/{object_name}"

