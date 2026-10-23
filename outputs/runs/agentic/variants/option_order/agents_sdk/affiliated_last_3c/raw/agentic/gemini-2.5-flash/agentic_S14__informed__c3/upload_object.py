from typing import Union, BinaryIO
from storage_client import get_s3_client

def upload_object(bucket_name: str, object_key: str, data: Union[bytes, BinaryIO], content_type: str = "application/octet-stream"):
    """
    Uploads a file or byte stream to Amazon S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The key (path) of the object in the bucket.
        data (Union[bytes, BinaryIO]): The data to upload, can be bytes or a file-like object.
        content_type (str): The Content-Type of the object.

    Returns:
        dict: The response from the S3 upload operation.
    """
    s3_client = get_s3_client()
    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=data,
        ContentType=content_type
    )
    return response
