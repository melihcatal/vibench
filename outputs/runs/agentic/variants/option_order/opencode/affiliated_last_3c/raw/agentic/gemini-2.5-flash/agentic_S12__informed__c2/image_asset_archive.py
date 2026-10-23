import os
from google.cloud import storage
from vision_models import ArchivedAsset


def archive_image_asset(
    file_content: bytes, file_name: str, content_type: str, bucket_name: str
) -> ArchivedAsset:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_string(file_content, content_type=content_type)

    return ArchivedAsset(
        asset_url=blob.public_url, file_name=file_name, content_type=content_type
    )
