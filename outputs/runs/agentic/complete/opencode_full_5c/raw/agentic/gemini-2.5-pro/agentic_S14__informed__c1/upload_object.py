from storage_client import get_storage_client
from typing import IO


def upload_object(bucket_name: str, object_name: str, file_stream: IO[bytes]):
    """
    Uploads a file stream to an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param object_name: The name of the object in the bucket.
    :param file_stream: A file-like object (bytes) to upload.
    """
    s3_client = get_storage_client()
    s3_client.upload_fileobj(file_stream, bucket_name, object_name)
