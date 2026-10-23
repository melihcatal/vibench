import os
from google.cloud import storage
from google.cloud.storage import Blob


def get_storage_client():
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path:
        return storage.Client.from_service_account_json(credentials_path)
    return storage.Client()


def get_bucket(client, bucket_name):
    return client.bucket(bucket_name)


def create_blob(bucket, object_name):
    return bucket.blob(object_name)


def upload_blob(blob, content, content_type=None, metadata=None):
    if content_type:
        blob.content_type = content_type
    if metadata:
        blob.metadata = metadata
    blob.upload_from_string(content, content_type=content_type)
    return blob


def generate_signed_url(blob, expiration_minutes=60):
    from datetime import timedelta

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
    )
    return url


def get_blob_metadata(blob):
    blob.reload()
    return {
        "name": blob.name,
        "bucket": blob.bucket.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "etag": blob.etag,
        "storage_class": blob.storage_class,
        "updated": blob.updated,
        "metadata": blob.metadata,
    }


def list_objects(bucket, prefix="", delimiter="", max_results=None):
    blobs = bucket.list_blobs(
        prefix=prefix, delimiter=delimiter, max_results=max_results
    )
    return blobs
