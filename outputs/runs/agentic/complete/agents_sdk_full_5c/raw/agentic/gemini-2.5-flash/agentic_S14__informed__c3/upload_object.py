import os
from storage_client import get_s3_client

def upload_object(
    bucket_name: str,
    object_key: str,
    file_path: Optional[str] = None,
    data: Optional[bytes] = None,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None
) -> dict:
    """
    Uploads a file or byte stream to an S3 bucket.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key (path) for the object in the bucket.
        file_path: The local path to the file to upload. (Optional)
        data: The byte stream to upload. (Optional)
        content_type: The content type of the object (e.g., 'image/jpeg', 'application/pdf').
        metadata: A dictionary of user-defined metadata to store with the object.

    Returns:
        A dictionary containing the S3 response (e.g., 'ETag', 'VersionId').
    """
    s3_client = get_s3_client()

    extra_args = {}
    if content_type:
        extra_args['ContentType'] = content_type
    if metadata:
        extra_args['Metadata'] = metadata

    if file_path:
        with open(file_path, 'rb') as f:
            response = s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=f, **extra_args)
    elif data is not None:
        response = s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=data, **extra_args)
    else:
        raise ValueError("Either 'file_path' or 'data' must be provided.")

    return response
